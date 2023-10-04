import os
import re
import time
import random
import logging
from datetime import datetime
from collections import namedtuple

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from gconnect import CFG

BOT_FOLDER = os.path.dirname(os.path.realpath(__file__))

logger = logging.getLogger('A.SC')
logger.setLevel(logging.DEBUG)

pageResult = namedtuple(
    typename='pageResult',
    field_names=CFG.DATA_HEADER,
    rename=False,
    defaults=None,
)


def tick():
    # print('Tick! The time is: %s' % datetime.now())
    logger.info('Tick.')
    # logger.debug('Tick.')

def dummy_parser(
        dummyArg: int,
        Link: str):
    """
    Simulate parser
    """

    Link = Link
    shop_name = 'My Shop 2'
    Shop_Name = 'Not my Shop'
    nomenclature = pow(2, (dummyArg+4))
    Customer_Price_BYN = 3.1
    Seller_Price_BYN = False
    Customer_price_RUB = 1,
    Seller_Price_RUB = dummyArg

    pageResultDummy = pageResult(
        Date=str(datetime.now()),
        Link=Link,
        Shop_Name=shop_name,
        Set=nomenclature,
        Customer_Price_BYN=Customer_Price_BYN,
        Seller_Price_BYN=Seller_Price_BYN,
        Customer_price_RUB='Не работает',
        Seller_Price_RUB='-'
    )

    return pageResultDummy


def dummy_scraper(lnks):
    """
    Simulate scraper
    """
    full_result = []
    for i in range(0, len(lnks)):
        logger.info(f'Scrape link №{i+1} of {len(lnks)}')
        full_result.append(parser(i, lnks[i]))
        time.sleep(1)
    return full_result


def ppage_parser(
    driver: selenium.webdriver,
    Link: str,
                ) -> pageResult:
    """
    Simplest parser
    """
    logger.debug(f'Parser prepare to get link {Link}')
    driver.get(Link)
    logger.debug(f'Parser wait for price')
    price = WebDriverWait(driver, 60).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[@class='price-block__final-price']")
        ))
    logger.debug(f'Parser got price')
    price = int(re.sub(r'[^0-9]', '', price.text))
    nc = str(driver.find_element(
        By.XPATH, "//*[@class='product-page__header']").text)
    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    logger.debug(f'Parsed. Price: {price}, Time: {dt_string}')
    pageResultParser = pageResult(
        Date=str(dt_string),
        Link=Link,
        Shop_Name='Не работает',
        Set=nc,
        Customer_Price_BYN='Не работает',
        Seller_Price_BYN='Не работает',
        Customer_price_RUB=price,
        Seller_Price_RUB='Не работает'
    )
    return pageResultParser


def interval_scraper(lnks):
    """
    Simulate scraper
    """
    logger.info(f'Interval scraper started. Have {len(lnks)} links')
    driver = webdriver.Chrome()
    full_result = []
    for i in range(0, len(lnks)):
        logger.debug('='*20)
        time.sleep(random.randint(
            CFG.SCRAPER_INTERPARSE_MIN, CFG.SCRAPER_INTERPARSE_MIN))
        logger.info(f'Scrape link №{i+1} of {len(lnks)}')
        full_result.append(
            ppage_parser(
                driver=driver,
                Link=lnks[i])
        )
        logger.debug('='*20)

    time.sleep(random.randint(
        CFG.SCRAPER_BEFOREQUIT_MIN, CFG.SCRAPER_BEFOREQUIT_MAX))
    driver.quit()

    return full_result