import logging
import time
from typing import Union, List, Tuple
from collections import namedtuple
from datetime import datetime

import pygsheets

logger = logging.getLogger('A.GC')
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    pageResult = namedtuple(
        typename='pageResult',
        field_names=DATA_HEADER,
        rename=False,
        defaults=None,
    )


class CFG():
    SPREADSHEET_PREFIX = 'wbmon-log-'
    MAX_SPREADSHEETS_PERDAY = 10
    HEADER_RANGE_NAME = 'headerRange'
    HEADER_LEFT_CORNER = (1, 1)
    LINKS_RANGE_NAME = 'linksRange'
    LINKS_SPREADSHEET_NAME = 'links'
    OAUTH_CREDENTIALS_FILE = 'client_secret.json'
    SCRAPER_INTERPARSE_MAX = 20
    SCRAPER_INTERPARSE_MIN = 10
    SCRAPER_BEFOREQUIT_MAX = 20
    SCRAPER_BEFOREQUIT_MIN = 10
    DATA_HEADER = [
        'Date',
        'Link',
        'Shop_Name',
        'Set',
        'Customer_Price_BYN',
        'Seller_Price_BYN',
        'Customer_price_RUB',
        'Seller_Price_RUB',
    ]


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
    gc = pygsheets.authorize(client_secret=CFG.OAUTH_CREDENTIALS_FILE)
    logger.info('Client authorized at start')
    lnks = get_links(gc)
    sh = gc.open(create_new_sheet(gc))
    logger.debug('Spreadsheet loaded')
    wks = sh.sheet1
    logger.debug('Worksheet loaded')
    if create_header(wks):
        return (lnks, gc, sh, wks)
    else:
        return None


def pgAuthorize(sheet_id: str) -> Tuple[pygsheets.client.Client,
                                        pygsheets.Spreadsheet,
                                        pygsheets.Worksheet]:
    """
    Renews connection with Google Sheets.
    Returns:
    Client, Spreadsheet №1, Worksheet with scrobbler data
    """
    gc = pygsheets.authorize(client_secret=CFG.OAUTH_CREDENTIALS_FILE)
    logger.info('Client authorized again')
    sh = gc.open_by_key(sh_id)
    wks = sh.sheet1
    logger.info('Spreadsheet and Worksheet loaded again')
    return gc, sh, wks


def post_values(sh_id,
                gc,
                sh,
                wks,
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
    # gc, sh, wks = pgAuthorize(sheet_id=sheet_id)
    logger.debug('Start posting values')
    headRange = wks.get_named_range(name=CFG.HEADER_RANGE_NAME)
    rn, cn = headRange.start_addr
    post_position = (rn+1, cn)

    logger.debug('headRange address loaded, prepared to unlink')
    wks.unlink()
    for result in full_result:
        wks.insert_rows(row=1,
                        number=1,
                        values=None,
                        inherit=False)
        result_list = [result._asdict()[name] for name in CFG.DATA_HEADER]
        wks.update_values(
            crange=post_position,
            values=[result_list],
            cell_list=None,
            extend=False,
            majordim='ROWS',
            parse=None)
    wks.link()
    logger.debug('Worksheed linked again')

    return True

def dummy_post_values(
                sh_id,
                gc,
                sh,
                wks,
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
    logger.debug(' FINISH POSTING' + f' DONE in {round(end_time - start_time,0)} sec')