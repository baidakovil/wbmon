# wbmon — Wildberries marketplace price monitor with Google Sheets publishing.
# Copyright (C) 2023 Ilia Baidakov <baidakovil@gmail.com>

# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <https://www.gnu.org/licenses/>.
"""This file contains Class and functions to publish parsed results to Google Sheets."""

import logging
import os
import time
from datetime import datetime
from typing import List, Optional, Tuple

import pygsheets
from pygsheets import Cell
from pygsheets.client import Client
from pygsheets.datarange import DataRange

from config import Cfg
from parsing.wbparser import PageResult

CFG = Cfg(test=os.getenv('TEST') == 'true')

logger = logging.getLogger('A.GC')
logger.setLevel(logging.DEBUG)


class Gc:
    """
    Represent continuous connection to google.sheets. Aims of the class creating is:
    1. Provide smart reconnect google sheets connection after long delay (controls with
       CFG. PYGSHEET_RECONNECT_TIME).
    2. Put into a single variable with Client, Spreadsheet, Worksheet, Spreadsh.id.
    """

    def __init__(self) -> None:
        self.client = pygsheets.authorize(client_secret=CFG.OAUTH_CREDENTIALS_FILE)
        self.started = time.monotonic()
        logger.debug('Client authorized at start')

    def open_by_name(self, spreadsheet: str) -> pygsheets.Spreadsheet:
        """
        Connect, i.e. load spreadsheet with given name to the Gc() and returns it.
        Args:
            spreadsheet: name of spreadsheet to connect/return
        Returns:
            spreadsheet instance, also add .sh property to Gc().
        """
        self.sh = self.client.open(spreadsheet)
        self.started = time.monotonic()
        return self.sh

    def open_wks(self) -> pygsheets.Worksheet:
        """
        Function to open worksheet 'sheet1' in previously opened spreadsheet sh. So with
        it, current implementation supported only 1 opened spreasheet 1 worksheet (first
        worksheet!).
        Returns:
            worksheet, also add .wks property to Gc()
        """
        self.wks = self.sh.sheet1
        self.started = time.monotonic()
        return self.wks

    def reconnect(self, soft: bool) -> None:
        """
        Reconnect Gc() instance to google before send data to gsheets.
        #TODO review. Is it really needed? May be I wrong and pygsheets do it...Catch ex
        Args:
            soft: if true, look config and decides on time of last conn, otherwise force
        """
        last_connect = time.monotonic() - self.started
        if (soft and (last_connect > CFG.SEC_PYGSHEET_RECONNECT_TIME)) or (not soft):
            logger.debug(
                f'Will reconnect. Last connection was {round(last_connect/60,1)}'
                f'min ago, more than {round(CFG.SEC_PYGSHEET_RECONNECT_TIME/60, 1)}'
            )
            self.client = pygsheets.authorize(client_secret=CFG.OAUTH_CREDENTIALS_FILE)
            self.sh = self.client.open_by_key(self.sh.id)
            self.wks = self.sh.sheet1
            self.started = time.monotonic()
            logger.debug('Client re-authorized, Spreadsheet and Worksheet reloaded')
        else:
            logger.debug(
                f'Wont reconnect. Last connection was {round(last_connect/60,1)}'
                f'min ago, LESS than {round(CFG.SEC_PYGSHEET_RECONNECT_TIME/60, 1)}'
            )
            pass


def create_new_sheet(gc: Client) -> str:
    """
    This functions create new spreadsheet with correct name.
    Args:
        client: Client pygsheets instance
    Returns:
        name of created sheet if ok, Raise exception if cant create
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
                f'Can not create more than {CFG.MAX_SPREADSHEETS_PERDAY} Spreadsheets per day'
            )
            raise Exception
    return gsheet_name


def get_links(client: Client) -> Optional[List[str]]:
    """
    Load links from Named range "linksRange" on Sheet1 of special Spreadsheet named
    LINKS_SPREADSHEET_NAME. Raises Exception, should be moderated by admin every launch.
    Args:
        client: Client pygsheets instance
    Returns:
        list of links if OK, None if spreadsheet nof found
    """
    logger.debug('Prepare to open links spreadsheet')
    try:
        sh_links = client.open(CFG.LINKS_SPREADSHEET_NAME)
        logger.debug('Links spreadsheet opened: %s', CFG.LINKS_SPREADSHEET_NAME)
    except pygsheets.SpreadsheetNotFound:
        logger.exception(f'Cant load links from spreadsheet')
        raise pygsheets.SpreadsheetNotFound
    wks_links = sh_links.sheet1
    lnkrange = wks_links.get_named_range(name=CFG.LINKS_RANGE_NAME)
    lnkrange_values = wks_links.get_values(
        start=lnkrange.start_addr, end=lnkrange.end_addr
    )
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
    Args:
        wks: worksheet where create header
    Returns:
        True if header-creating-checking passed, False other way
    """
    header_row, _ = CFG.HEADER_LEFT_CORNER
    wks.create_named_range(
        name=CFG.HEADER_RANGE_NAME,
        start=CFG.HEADER_LEFT_CORNER,
        end=(header_row, len(CFG.DATA_HEADER)),
        returnas='json',
    )
    header_range = wks.get_named_range(name=CFG.HEADER_RANGE_NAME)
    if not isinstance(header_range, DataRange):
        logger.warning('Can not get named range %s', CFG.HEADER_RANGE_NAME)
        return False
    logger.debug('Header namedRange loaded')
    header_range.update_values([CFG.DATA_HEADER])
    logger.debug('Header values updated')
    mcell = wks.cell(CFG.HEADER_LEFT_CORNER)
    if not isinstance(mcell, Cell):
        logger.warning('Can not get cells %s', CFG.HEADER_LEFT_CORNER)
        return False
    mcell.text_format['bold'] = True
    header_range.apply_format(cell=mcell)
    if mcell.value == CFG.DATA_HEADER[0]:  # I call it "soundcheck".
        logger.debug('Header created and checked')
        return True
    else:
        logger.warning('Mistake with header creating')
        return False


def start_gsheets() -> Tuple[List[str], Gc]:
    """
    Starts work with googlesheets. Establish connection, create new list, create header.
    Returns:
        links to load and spreadsheet to write
    """
    gc = Gc()
    client = gc.client
    logger.info('Client authorized at start')

    lnks = get_links(client)
    assert isinstance(lnks, list)

    logger.info(
        "TEST MODE: %s, MAX_LINK_QUANTITY: %s",
        os.getenv('TEST') == 'true',
        CFG.MAX_LINK_QUANTITY,
    )

    if CFG.CREATE_NEW_SPREADSHEET:
        spreadsheet = create_new_sheet(client)
    else:
        spreadsheet = CFG.OLD_SHEET_TITLE
        logger.info(f'Old Spreadsheet will be loaded: {CFG.OLD_SHEET_TITLE}')
    gc.open_by_name(spreadsheet)
    wks = gc.open_wks()
    if CFG.CREATE_NEW_SPREADSHEET:
        create_header(wks)

    return lnks, gc


def post_values(gc: Gc, full_result: PageResult) -> bool:
    """
    Finds actual header position and post all rows below it. Print beautiful logs.
    Args:
        gc: Gc() instance with connection
        full_result: namedtuple with data to publish
    Returns:
        True
    """
    gc.reconnect(soft=True)
    wks = gc.wks
    logger.debug(' START POSTING')
    logger.info('|' + ' | '.join(logresult_prepare(header=True)))
    start_time = time.time()
    headRange = wks.get_named_range(name=CFG.HEADER_RANGE_NAME)
    rn, cn = headRange.start_addr
    post_position = (rn + 1, cn)
    wks.unlink()
    header_vars = [name.lower() for name in CFG.DATA_HEADER]
    for result in full_result:
        wks.insert_rows(row=1, number=1, values=None, inherit=False)
        result_list = [str(result._asdict()[name]) for name in header_vars]
        wks.update_values(
            crange=post_position,
            values=[result_list],
            cell_list=None,
            extend=False,
            majordim='ROWS',
            parse=None,
        )
        logger.info(' | '.join(result_list) + ' | ' + CFG.LOGGER_FILTER_MSG)
        logger.info('|' + ' | '.join(logresult_prepare(data=result_list)))
    wks.link()
    end_time = time.time()
    logger.debug(' FINISH POSTING' + f' DONE in {round(end_time - start_time,0)} sec')
    return True


def logresult_prepare(
    data: Optional[List[str]] = None, header: Optional[bool] = None
) -> List[str]:
    """
    Prepares smooth log message, trimming and pagging header or data.
    Args:
        data: parsed data to trim or pad with trim(). If passed, header should be None
        header: if True, returns padded header
    """

    def trim(word, width):
        """Inner function. Trim, pad, deletes strin beginning if 'http' in beginning."""
        if word.startswith('http'):
            return '..' + word[-width + 2 :]
        return word[: width - 3] + '...' if len(word) > width else word.ljust(width)

    widths = CFG.HEADER_WIDTHS
    if header:
        return [word.ljust(width) for word, width in zip(CFG.DATA_HEADER, widths)]
    assert data
    return [trim(word, width) for word, width in zip(data, widths)]
