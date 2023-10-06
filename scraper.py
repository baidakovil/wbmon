import os
import re
import time
import random
import logging
from datetime import datetime
from collections import namedtuple

from selenium import webdriver

from config import Cfg
from wbparser import wb_parser
from wbparser import PageResult

BOT_FOLDER = os.path.dirname(os.path.realpath(__file__))
CFG = Cfg()

logger = logging.getLogger('A.SC')
logger.setLevel(logging.DEBUG)


def interval_scraper(lnks):
    """
    Scraper.
    """
    logger.info(f'Interval scraper started. Have {len(lnks)} links')
    logger.debug('-'*20)

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)

    full_result = []
    for i in range(0, len(lnks)):

        interparse_sleep = random.randint(
            CFG.SCRAPER_INTERPARSE_MIN, CFG.SCRAPER_INTERPARSE_MAX)
        logger.info(
            f'Scrape link №{i+1} of {len(lnks)}. Sleep: {interparse_sleep} sec')
        time.sleep(interparse_sleep)

        start_time = time.time()
        full_result.append(
            wb_parser(
                driver=driver,
                Link=lnks[i])
        )
        end_time = time.time()

        logger.debug('-'*20 + f' DONE in {round(end_time - start_time,0)} sec')

    beforequit_sleep = random.randint(
        CFG.SCRAPER_BEFOREQUIT_MIN, CFG.SCRAPER_BEFOREQUIT_MAX)
    logger.info(f'Driver will quit() after sleep: {interparse_sleep} sec')
    time.sleep(interparse_sleep)

    driver.quit()

    return full_result


def dummy_parser(
        dummyArg: int,
        Link: str):
    """
    Simulate parser
    """

    Link = Link
    shop_name = 'My Shop 2 Sample'
    Shop_Name = 'Not my Shop'
    nomenclature = str(pow(2, (dummyArg+4)))+' power sample'
    Customer_Price_BYN = 3.1
    Seller_Price_BYN = False
    Customer_price_RUB = 1,
    Seller_Price_RUB = dummyArg*750

    pageResultDummy = PageResult(
        Date=str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
        Link=Link,
        Shop_Name=shop_name,
        Set=nomenclature,
        Customer_Price_BYN='-',
        Seller_Price_BYN='-',
        Customer_price_RUB=2637.5,
        Seller_Price_RUB='-'
    )

    return pageResultDummy


def dum_interval_scraper(lnks):
    """
    Simulate scraper
    """
    logger.info(f'Dummy interval scraper started. Have {len(lnks)} links')
    logger.debug('-'*20)
    full_result = []
    for i in range(len(lnks)):
        logger.info(f'Scrape link №{i+1} of {len(lnks)}')
        start_time = time.time()
        full_result.append(dummy_parser(i, lnks[i]))
        time.sleep(2)
        end_time = time.time()
        logger.debug('-'*20 + f' DONE in {round(end_time - start_time,0)} sec')
    return full_result


def tick():
    # print('Tick! The time is: %s' % datetime.now())
    logger.info('Tick.')
    # logger.debug('Tick.')
