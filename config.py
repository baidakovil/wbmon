import os
import logging

logger = logging.getLogger('A.CFG')
logger.setLevel(logging.DEBUG)

class Cfg():
    def __init__(self, test):
        if test:
            logger.info(f'Cfg Class says: TEST CONFIG LOADING')
                 # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
                 # # # # # # TEST  # # # CONFIG  # # # # # # # # # # # #
                 # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
            self.OLD_SHEET_TITLE = 'wbmon-log-05-Oct'
            self.SPREADSHEET_PREFIX = 'wbmon-log-'
            self.DATA_HEADER = [
                                'Date',
                                'Link',
                                'Shop_Name',
                                'Set',
                                'Customer_Price_BYN',
                                'Seller_Price_BYN',
                                'Customer_price_RUB',
                                'Seller_Price_RUB',
                                        ]
            self.HEADER_RANGE_NAME = 'headerRange'
            self.HEADER_LEFT_CORNER = (1, 1)
            self.LINKS_RANGE_NAME = 'linksRange'
            self.LINKS_SPREADSHEET_NAME = 'links'
            self.OAUTH_CREDENTIALS_FILE = 'client_secret.json'
            self.PYGSHEET_RECONNECT_TIME = 120
                 # TEST and WORKING: COMMON ABOVE, NOT COMMON BELOW
            self.CREATE_NEW_SPREADSHEET = False
            self.MAX_SPREADSHEETS_PERDAY = 27
            self.PAGELOAD_MAXTIME = 120
            self.SCRAPER_INTERPARSE_MAX = 8
            self.SCRAPER_INTERPARSE_MIN = 2
            self.SCRAPER_BEFOREQUIT_MAX = 4
            self.SCRAPER_BEFOREQUIT_MIN = 2
            self.ASAP = True
            self.ASAPTRIGGER = 30
            self.ASAPDELAY = 2
            self.CRON_ARGS = {
                            'minute': '*/3',
                                    'jitter': 10,
                                                }
            self.MAX_LINK_QUANTITY = 2
            self.MISFIRE_TIME = 30
        else:
            logger.info(f'Cfg Class says: WORKING CONFIG LOADING')
                 # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
                 # # # # # # # WORKING # # # CONFIG  # # # # # # # # # #
                 # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
            self.OLD_SHEET_TITLE = 'wbmon-log-05-Oct_rev1'
            self.SPREADSHEET_PREFIX = 'wbmon-log-'
            self.DATA_HEADER = [
                                'Date',
                                'Link',
                                'Shop_Name',
                                'Set',
                                'Customer_Price_BYN',
                                'Seller_Price_BYN',
                                'Customer_price_RUB',
                                'Seller_Price_RUB',
                                                        ]
            self.HEADER_RANGE_NAME = 'headerRange'
            self.HEADER_LEFT_CORNER = (1, 1)
            self.LINKS_RANGE_NAME = 'linksRange'
            self.LINKS_SPREADSHEET_NAME = 'links'
            self.OAUTH_CREDENTIALS_FILE = 'client_secret.json'
            self.PYGSHEET_RECONNECT_TIME = 600
                 # TEST and WORKING: COMMON ABOVE, NOT COMMON BELOW
            self.CREATE_NEW_SPREADSHEET = True
            self.MAX_SPREADSHEETS_PERDAY = 10
            self.PAGELOAD_MAXTIME = 300
            self.SCRAPER_INTERPARSE_MAX = 120
            self.SCRAPER_INTERPARSE_MIN = 30
            self.SCRAPER_BEFOREQUIT_MAX = 20
            self.SCRAPER_BEFOREQUIT_MIN = 10
            self.ASAP = True
            self.ASAPTRIGGER = 60
            self.ASAPDELAY = 1
            self.CRON_ARGS = {
                            'hour': '*/6',
                                    'jitter': 1800,
                                                }
            self.MAX_LINK_QUANTITY = 100
            self.MISFIRE_TIME = 3600