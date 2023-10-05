import os
import re
import time
import random
import logging
from datetime import datetime
from collections import namedtuple

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException

from dotenv import load_dotenv
from config import Cfg

BOT_FOLDER = os.path.dirname(os.path.realpath(__file__))

load_dotenv(os.path.join(BOT_FOLDER, '.env'))
CFG = Cfg(test=os.getenv('TEST') == 'true')

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
    shop_name = 'My Shop 2 Sample'
    Shop_Name = 'Not my Shop'
    nomenclature = str(pow(2, (dummyArg+4)))+' power sample'
    Customer_Price_BYN = 3.1
    Seller_Price_BYN = False
    Customer_price_RUB = 1,
    Seller_Price_RUB = dummyArg*750

    pageResultDummy = pageResult(
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


def ppage_parser(
    driver,
    Link,
                ) -> pageResult:
    """
    Product Page Parser
    """
    logger.debug(f'Parser prepare to get link {Link}')
    driver.get(Link)
    logger.debug(f'Parser wait for price')
    
    try:
        price = WebDriverWait(driver, CFG.PAGELOAD_MAXTIME).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[@class='price-block__final-price']")
            ))
        price = int(re.sub(r'[^0-9]', '', price.text))
        nc = str(driver.find_element(
            By.XPATH, "//*[@class='product-page__header']").text)
    except TimeoutException:
        price = 'TimeoutException'
        nc = 'TimeoutException'

    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

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
        logger.info(f'Scrape link №{i+1} of {len(lnks)}. Sleep: {interparse_sleep} sec')
        time.sleep(interparse_sleep)

        start_time = time.time()
        full_result.append(
            ppage_parser(
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
