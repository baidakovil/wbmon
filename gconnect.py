import os
import logging
import time
from typing import Union, List, Tuple
from collections import namedtuple
from datetime import datetime

import pygsheets

from dotenv import load_dotenv
from config import Cfg

BOT_FOLDER = os.path.dirname(os.path.realpath(__file__))

load_dotenv(os.path.join(BOT_FOLDER, '.env'))
CFG = Cfg(test=os.getenv('TEST') == 'true')

logger = logging.getLogger('A.GC')
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    pageResult = namedtuple(
        typename='pageResult',
        field_names=CFG.DATA_HEADER,
        rename=False,
        defaults=None,
    )

class Gc():
    """
    Class represented continuous connection to google.sheets
    """
    def __init__(self):
        self.client = pygsheets.authorize(client_secret=CFG.OAUTH_CREDENTIALS_FILE)
        self.started = time.time()
        print('Client authorized at start')

    def open_by_name(self, spreadsheet):
        self.sh = self.client.open(spreadsheet)
        self.started = time.time()
        return self.sh

    def open_wks(self, spreadsheet):
        self.wks = self.sh.sheet1
        self.started = time.time()
        return self.wks

    def reconnect(self, soft):
        last_connect = time.time() - self.started
        if (soft and (last_connect > CFG.PYGSHEET_RECONNECT_TIME)) or (not soft):
            print(f'Will reconnect. Last connection was {round(last_connect/60,1)}'\
                    f'min ago, more than {round(CFG.PYGSHEET_RECONNECT_TIME/60, 1)}')
            self.client = pygsheets.authorize(client_secret=CFG.OAUTH_CREDENTIALS_FILE)
            self.sh = self.client.open_by_key(self.sh.id)
            self.wks = self.sh.sheet1
            self.started = time.time()
            print('Client re-authorized, Spreadsheet and Worksheet reloaded')
        else:
            print(f'Wont reconnect. Last connection was {round(last_connect/60,1)}'\
                    f'min ago, LESS than {round(CFG.PYGSHEET_RECONNECT_TIME/60, 1)}')
            pass

def create_new_sheet(gc: pygsheets.client.Client) -> str:
    """
    This functions create new spreadsheet with correct name.
    Returns:
    - name of created sheet if OK
    - Raise exception if cant create with 10th try
    """
    count = 0
    gsheet_name = CFG.SPREADSHEET_PREFIX + datetime.now().strftime('%d-%b')
    while count < CFG.MAX_SPREADSHEETS_PERDAY:
        try:
            gc.open(gsheet_name)
        except pygsheets.SpreadsheetNotFound:
            gc.create(gsheet_name)
            logger.info(f'Google Spreadsheet created: {gsheet_name}')
            break
        count += 1
        if gsheet_name[-4:-1] != 'rev':
            gsheet_name = gsheet_name + '_rev' + str(count)
        else:
            gsheet_name = gsheet_name[:-1] + str(count)
        if count == CFG.MAX_SPREADSHEETS_PERDAY:
            logger.exception(
                f'Can not create more than {CFG.MAX_SPREADSHEETS_PERDAY} Spreadsheets per day')
            raise Exception
    return gsheet_name


def get_links(gc: pygsheets.client.Client) -> List[str]:
    """
    Load links from Named range "linksRange" on Sheet1 of special Spreadsheet
    Returns:
    - List of links if OK;
    - None if spreadsheet nof found.    
    """
    logger.debug('Prepare to open links spreadsheet')
    try:
        sh_links = gc.open(CFG.LINKS_SPREADSHEET_NAME)
        logger.debug('Links spreadsheet opened')
    except pygsheets.SpreadsheetNotFound:
        logger.exception(f'Cant load links from spreadsheet')
        raise Exception
    wks_links = sh_links.sheet1
    lnkrange = wks_links.get_named_range(name=CFG.LINKS_RANGE_NAME)
    lnkrange_values = wks_links.get_values(
        start=lnkrange.start_addr,
        end=lnkrange.end_addr)
    wks_links.unlink()
    logger.debug('Links values downloaded')
    lnks = []
    for cell in lnkrange_values:
        if cell[0]:
            lnks.append(cell[0])

    return lnks


def create_header(wks: pygsheets.Worksheet) -> bool:
    """
    Function to create static text header.
    Returns:
    - True if header-creating-checking passed
    - False other way
    """
    header_row, _ = CFG.HEADER_LEFT_CORNER
    wks.create_named_range(name=CFG.HEADER_RANGE_NAME,
                           start=CFG.HEADER_LEFT_CORNER,
                           end=(header_row, len(CFG.DATA_HEADER)),
                           returnas='json')
    headerRange = wks.get_named_range(name=CFG.HEADER_RANGE_NAME)
    logger.debug('Header namedRange loaded')
    headerRange.update_values([CFG.DATA_HEADER])
    logger.debug('Header values updated')
    mcell = wks.cell(CFG.HEADER_LEFT_CORNER)
    mcell.text_format['bold'] = True
    headerRange.apply_format(cell=mcell)
    if mcell.value == CFG.DATA_HEADER[0]:  # I call it "soundcheck".
        logger.debug('Header created and checked')
        return True
    else:
        logger.warning('Mistake with header creating')
        return False


def start_gsheets() -> Union[Tuple[List[str],
                                   pygsheets.Spreadsheet,
                                   pygsheets.client.Client,
                                   pygsheets.Spreadsheet,
                                   pygsheets.Worksheet
                                         ], None]:
    """
    Function to start work with googlesheets. 
    Establish connection, create new list, create header.
    Returns:
    - tuple with links to load and spreadsheet to write if OK
    - None otherway
    """
    gc = Gc()
    client = gc.client
    logger.info('Client authorized at start')

    lnks = get_links(client)
    logger.info(f"TEST MODE: {os.getenv('TEST') == 'true'}")
    if CFG.CREATE_NEW_SPREADSHEET:
        spreadsheet = create_new_sheet(client)
    else:
        spreadsheet = CFG.OLD_SHEET_TITLE
        logger.info(f'Old Spreadsheet will be loaded: {CFG.OLD_SHEET_TITLE}')
    sh = gc.open_by_name(spreadsheet)
    # sh = gc.open(create_new_sheet(gc))
    wks = gc.open_wks(sh)
    # wks = sh.sheet1
    if CFG.CREATE_NEW_SPREADSHEET:
        create_header(wks)

    return lnks, gc


def post_values(
    gc,
    full_result,
) -> bool:
    """
    Finds actual header position and post all rows below it.
    Args:
    - sh_id is spreadsheet id to reconnect FUTURE FUNCTION
    - full_result is namedtuple, with
        field_names: DATA_HEADER str values,
        fields values: arbitrary type values
    Returns:
    - True if posted
    """
    gc.reconnect(soft=True)
    wks = gc.wks
    logger.debug(' START POSTING')
    logger.info(' | '.join(CFG.DATA_HEADER))
    start_time = time.time()
    headRange = wks.get_named_range(name=CFG.HEADER_RANGE_NAME)
    rn, cn = headRange.start_addr
    post_position = (rn+1, cn)
    wks.unlink()
    for result in full_result:
        wks.insert_rows(row=1,
                        number=1,
                        values=None,
                        inherit=False)
        result_list = [str(result._asdict()[name]) for name in CFG.DATA_HEADER]
        wks.update_values(
            crange=post_position,
            values=[result_list],
            cell_list=None,
            extend=False,
            majordim='ROWS',
            parse=None)
        logger.info(' | '.join(result_list))
    wks.link()
    end_time = time.time()
    logger.debug(' FINISH POSTING' +
                 f' DONE in {round(end_time - start_time,0)} sec')

    return True


def dummy_post_values(
    gc,
    full_result,
) -> bool:
    logger.debug(' START POSTING')
    logger.info(' | '.join(CFG.DATA_HEADER))
    start_time = time.time()
    for result in full_result:
        result_list = [str(result._asdict()[name]) for name in CFG.DATA_HEADER]
        logger.info(' | '.join(result_list))
        time.sleep(1)
    end_time = time.time()
    logger.debug(' FINISH POSTING' +
                 f' DONE in {round(end_time - start_time,0)} sec')
