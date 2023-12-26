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
"""This file contains parser func itself. Also storing dataclass and dummy parser."""

import collections
import logging
import os
import re
from datetime import datetime
from typing import Tuple

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import Cfg

CFG = Cfg(test=os.getenv('TEST') == 'true')
logger = logging.getLogger('A.SC')
logger.setLevel(logging.DEBUG)


class PageResult(  # pylint: disable=too-few-public-methods
    collections.namedtuple(
        typename='pageResult',
        field_names=[name.lower() for name in CFG.DATA_HEADER],
        rename=False,
        defaults=None,
    )
):
    """
    Store for results obtained from parsing.
    """


def wb_parser(driver: Chrome, link: str) -> PageResult:
    """
    The only parser function for WB-Product-page.
    Args:
        driver: web-driver; Chrome is unarguemented choice
        Link: link to parse
    """
    driver.get(link)
    driver = wait_driver(driver)

    brand_name, goods_name = parse_goods_name(driver)
    seller_info = parse_shop_name(driver)
    nm_id = parse_id(driver)
    cus_rub, sel_rub = parse_price(driver)
    date = datetime.now().strftime(CFG.FORMAT_TIMESTAMP_PARSED)

    return PageResult(
        date, link, brand_name, goods_name, seller_info, nm_id, cus_rub, sel_rub
    )


def wait_driver(driver: Chrome) -> Chrome:
    """Waits until page will be loaded. XPATH changed once."""
    try:
        WebDriverWait(driver, CFG.PAGELOAD_MAXTIME).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[@class='product-page__aside']")
            )
        )
    except TimeoutException:
        logger.warning('TimeoutException when waited for main page to load')
    return driver


def parse_shop_name(driver: Chrome) -> str:
    """Get seller name. Sometimes it is missed on the page."""
    try:
        elem = driver.find_element(
            By.XPATH, "//*[@class='seller-info__name']"
        ).get_attribute('textContent')
    except NoSuchElementException:
        elem = CFG.ERROR_PARSE_STRING
    if isinstance(elem, str):
        return elem.strip()
    return CFG.ERROR_PARSE_STRING


def retain_num(elem: WebElement) -> int:
    """Filters all characters except digits."""
    return int(re.sub(r'[^0-9]', '', elem.text))


def parse_price(driver: Chrome) -> Tuple[str, str]:
    """Get 'customer' (real) and 'seller' (striked) prices."""

    soldout = 'Нет в наличии'

    try:
        e12 = driver.find_element(
            By.XPATH,
            "//div[contains(@class, 'product-page__price-block product-page__price-block--common')]",  #  pylint: disable=line-too-long
        ).text
    except NoSuchElementException:
        logger.warning('Cannot find neither prices nor soldout')
        return CFG.ERROR_PARSE_STRING, CFG.ERROR_PARSE_STRING

    if soldout in e12:
        return soldout, soldout

    try:
        e1 = driver.find_element(By.XPATH, "//*[@class='price-block__final-price']")
        e1 = str(retain_num(e1))
    except NoSuchElementException:
        logger.warning('Undocumented case e_1: %s', e12)
        e1 = CFG.ERROR_PARSE_STRING

    try:
        e2 = driver.find_element(By.XPATH, "//*[@class='price-block__old-price']")
        e2 = str(retain_num(e2))
    except NoSuchElementException:
        logger.warning('No seller price parsed')
        e2 = CFG.ERROR_PARSE_STRING

    return e1, e2


def parse_goods_name(driver: Chrome) -> Tuple[str, str]:
    """Get brand name and thing name, that are in same string."""
    try:
        elem = driver.find_element(By.XPATH, "//*[@class='product-page__header']")
    except NoSuchElementException:
        logger.warning('Can not find brand/good name')
        return CFG.ERROR_PARSE_STRING, CFG.ERROR_PARSE_STRING
    try:
        brand_name, goods_name = elem.text.split('\n')
    except ValueError:
        logger.warning('Find product name, but can not parse it to brand and good')
        return CFG.ERROR_PARSE_STRING, CFG.ERROR_PARSE_STRING
    return brand_name, goods_name


def parse_id(driver: Chrome) -> str:
    """Get nomenclature ID number of goods."""
    try:
        elem = driver.find_element(
            By.XPATH, "//*[@class='product-params__cell product-params__cell--copy']"
        ).get_attribute('textContent')
    except NoSuchElementException:
        logger.warning('Can not find product ID')
        return CFG.ERROR_PARSE_STRING
    try:
        assert isinstance(elem, str)
        int(elem)
    except TypeError:
        logger.warning('Find product ID, but it is not a numeric')
        return CFG.ERROR_PARSE_STRING
    except IndexError:
        logger.warning('Find product ID, but it is not iterates properly')
        return CFG.ERROR_PARSE_STRING
    return elem


def dummy_parser(dummydriver: int, link: str) -> PageResult:
    """
    Simulate parser for debugging. Returns PageResult class instance.
    """
    date = datetime.now().strftime(CFG.FORMAT_TIMESTAMP_PARSED)
    seller_info = 'My Shop 2Sample'
    goods_name = 'Confety'
    brand_name = 'Brandy'
    seller_info = 'Whosell'
    nm_id = str(pow(2, (dummydriver + 4)))
    cus_rub = 1023
    sel_rub = dummydriver * 750

    return PageResult(
        date, link, brand_name, goods_name, seller_info, nm_id, cus_rub, sel_rub
    )
