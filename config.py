# wbmon — Wildberries marketplace price monitor with Google Sheets publishing.
# Copyright (C) 2021-2023 Ilia Baidakov <baidakovil@gmail.com>

# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <https://www.gnu.org/licenses/>.
"""This file contains class with configuration parameters."""

import logging
import os

from dotenv import load_dotenv

logger = logging.getLogger('A.CFG')
logger.setLevel(logging.DEBUG)
load_dotenv('.env')


class Cfg:
    """
    Class for simple obtaining configs.
    Test/Working settings are SPLITTED and DUPLICATED, it is like experiment.
    In the beginning of __init__() there is common settings for testing and working.
    After, settings loaded on base of ENVIRONMENT VARIABLE 'TEST'. It should be exactly
    'true' to load test settings and any other for working.
    """

    def __init__(self, test=os.getenv('TEST') == 'true'):
        # GOOGLE SHEETS

        #  Spreadsheet name to publish in case of CREATE_NEW_SPREADSHEET = False
        self.OLD_SHEET_TITLE = 'wbmon-log-13-Dec'

        #  Spreadsheet prefix for new creating spreadsheet
        self.SPREADSHEET_PREFIX = 'wbmon-log-'

        #  List of fields which will be published. This connects to program logic
        self.DATA_HEADER = [
            'Date',
            'Link',
            'Brand_Name',
            'Goods_Name',
            'Seller_Info',
            'Nm_ID',
            'Cus_RUB',
            'Sel_RUB',
        ]

        #  Name of the named range in spreadsheet LINKS_SPREADSHEET_NAME
        self.HEADER_RANGE_NAME = 'headerRange'

        #  Position of header. Right under it program will publish data
        self.HEADER_LEFT_CORNER = (1, 1)

        #  Name of named range in LINKS_SPREADSHEET_NAME
        self.LINKS_RANGE_NAME = 'linksRange'

        #  Name of the file where links to load are stored
        self.LINKS_SPREADSHEET_NAME = 'links'

        #  Name of the google credentials file
        self.OAUTH_CREDENTIALS_FILE = 'client_secret.json'

        #  Time delay for pygsheet to reconnect
        self.SEC_PYGSHEET_RECONNECT_TIME = 600

        #  Maximum possible autocreated spreadsheets quantity in single day
        self.MAX_SPREADSHEETS_PERDAY = 27

        # USER INTERFACE

        #  Width of fields to pretty log results in console logger
        self.HEADER_WIDTHS = [19, 24, 17, 17, 17, 11, 9, 9]

        #  Constant line to publish when there is no parsed results
        self.ERROR_PARSE_STRING = 'ERR'

        #  Time format to publish results
        self.FORMAT_TIMESTAMP_PARSED = '%d/%m/%Y %H:%M:%S'

        #  Special string for filtering log messages (paste->wont appear in console)
        self.LOGGER_FILTER_MSG = 'LOGGER_FILTER_MSG'

        #  Time between loads in dummyscraper
        self.SEC_WAIT_DUMMYSCRAPER = 2

        # LOGGER

        #  Path to logger files
        self.PATH_LOGGER = '.'

        #  Filename for rotating logger (logging all runs)
        self.FILE_ROTATING_LOGGER = 'logger.log'

        #  Max filesize for rotating logger
        self.BYTES_MAX_ROTATING_LOGGER = 1024 * 1024 * 20

        #  Quantity of files, keeping by rotating logger.
        self.QTY_BACKUPS_ROTATING_LOGGER = 5

        if test:
            logger.info(f'Cfg Class says: TEST CONFIG LOADING')
            # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # TEST  # # # CONFIG  # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # #

            #  Cron scheduler arguments. 'minute':'*/3' mean load every 3 min
            self.CRON_ARGS = {
                'minute': '*/3',
                'jitter': 10,
            }

            #  Whether create new spreadsheet at start or use former
            self.CREATE_NEW_SPREADSHEET = False

            #  Maximum timeout in seconds to wait for page to load
            self.PAGELOAD_MAXTIME = 120

            #  Min and max intervals between parsing, real will be random
            self.SCRAPER_INTERPARSE_MAX = 10
            self.SCRAPER_INTERPARSE_MIN = 5

            #  Min and max intervals befor close driver, real will be random
            self.SCRAPER_BEFOREQUIT_MAX = 10
            self.SCRAPER_BEFOREQUIT_MIN = 5

            #  Does program should load links as soon as possible
            self.ASAP = True

            #  If next job close than this (in seconds), than program will wait for it
            self.ASAPTRIGGER = 30

            #  Delay before start to load ASAP
            self.ASAPDELAY = 2

            #  How many links maximum will be managed
            self.MAX_LINK_QUANTITY = 2

            #  Parameter misfire_grace_time for scheduler, time to delete overdue jobs
            self.MISFIRE_TIME = 30

            #  Arguments to pass to Chrome driver. Better not to touch
            self.CHROME_DRIVER_ARGS = ['--headless', '--no-sandbox']

        else:
            logger.info(f'Cfg Class says: WORKING CONFIG LOADING')
            # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # WORKING # # # CONFIG  # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            self.CRON_ARGS = {
                'hour': '*/8',
                'jitter': 1800,
            }
            self.CREATE_NEW_SPREADSHEET = True
            self.PAGELOAD_MAXTIME = 300
            self.SCRAPER_INTERPARSE_MAX = 120
            self.SCRAPER_INTERPARSE_MIN = 30
            self.SCRAPER_BEFOREQUIT_MAX = 20
            self.SCRAPER_BEFOREQUIT_MIN = 10
            self.ASAP = True
            self.ASAPTRIGGER = 60
            self.ASAPDELAY = 5
            self.MAX_LINK_QUANTITY = 100
            self.MISFIRE_TIME = 3600
            self.CHROME_DRIVER_ARGS = ['--headless', '--no-sandbox']
