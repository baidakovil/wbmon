import os
import re
from datetime import datetime
import collections
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from config import Cfg

BOT_FOLDER = os.path.dirname('/home/eva/git/wbmon/')
CFG = Cfg(test=os.getenv('TEST') == 'true')

logger = logging.getLogger('A.SC')
logger.setLevel(logging.DEBUG)


class PageResult(collections.namedtuple(
    typename='pageResult',
    field_names=CFG.DATA_HEADER,
    rename=False,
    defaults=None,
)):
    pass


def wb_parser(driver, Link):

    def wait_driver(driver):
        try:
            some = WebDriverWait(driver, CFG.PAGELOAD_MAXTIME).until(
                EC.visibility_of_element_located(
                    # (By.XPATH,"//div[contains(@class, 'product-page__price-block product-page__price-block--common')]")
                    (By.XPATH, "//*[@class='seller-info__name seller-info__name--link']")
                ))
        except TimeoutException:
            logger.warning('TimeoutException')
        return driver

    def parse_shop_name(driver):
        try:
            elem = driver.find_element(
                By.XPATH, "//*[@class='seller-info__name seller-info__name--link']").text
        except NoSuchElementException:
            print('Cant find shop name')
            elem = 'ERR'
        return str(elem)

    def retain_num(elem):
        return int(re.sub(r'[^0-9]', '', elem.text))

    def parse_price(driver):
        soldout = 'Нет в наличии'
        try:
            e12 = driver.find_element(
                By.XPATH, "//div[contains(@class, 'product-page__price-block product-page__price-block--common')]").text
            if soldout in e12:
                print('Soldout case')
                e1, e2 = soldout, soldout
                return e1, e2
            else:
                try:
                    e1 = driver.find_element(
                        By.XPATH, "//*[@class='price-block__final-price']")
                    e1 = retain_num(e1)
                except NoSuchElementException:
                    print(f'Undoc case e_1: {e1}')
                    e1 = 'ERR'
                try:
                    e2 = driver.find_element(
                        By.XPATH, "//*[@class='price-block__old-price j-wba-card-item-show']")
                    e2 = retain_num(e2)
                except NoSuchElementException:
                    print(f'No seller price case')
                    e2 = 'ERR'
                return e1, e2
        except NoSuchElementException:
            print('Cannot find any of prices or soldout')
            e1, e2 = 'ERR', 'ERR'
            return e1, e2

    def parse_goods_name(driver):
        try:
            elem = driver.find_element(
                By.XPATH, "//*[@class='product-page__header']")
            Brand_Name, Goods_Name = elem.text.split('\n')
            return Brand_Name, Goods_Name 
        except NoSuchElementException:
            print('Cant find product name')
            return None, None

    def parse_id(driver):
        try:
            elem = driver.find_elements(
                By.CSS_SELECTOR, "button.product-article__copy[type='button']")
            return int(elem[1].text)
        except NoSuchElementException:
            print('Cant find product name')
            return None

    driver.get(Link)
    driver = wait_driver(driver)
    
    Brand_Name, Goods_Name = parse_goods_name(driver)
    Seller_Info = parse_shop_name(driver)
    NmID = parse_id(driver)
    Customer_price_RUB, Seller_Price_RUB = parse_price(driver)
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    pageResultParser = PageResult(
                                    Date=str(date),
                                    Link=str(Link),
                                    Brand_Name=Brand_Name,
                                    Goods_Name=Goods_Name,
                                    Seller_Info=Seller_Info,
                                    NmID=NmID,
                                    Customer_Price_BYN='LATER',
                                    Seller_Price_BYN='LATER',
                                    Customer_price_RUB=Customer_price_RUB,
                                    Seller_Price_RUB=Seller_Price_RUB
                                )
    return pageResultParser