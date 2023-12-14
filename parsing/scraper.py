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
"""This file contains low-level scheduling funcs, i.e. pauses & running wb_parser()."""

import logging
import os
import random
import time
from typing import List

from selenium import webdriver

from config import Cfg
from parsing.wbparser import PageResult, dummy_parser, wb_parser

CFG = Cfg(test=os.getenv('TEST') == 'true')

logger = logging.getLogger('A.SC')
logger.setLevel(logging.DEBUG)


def interval_scraper(lnks: List[str]) -> List[PageResult]:
    """
    main()-> get_scheduler()-> interval_job(lnks, gc, trigger)-> interval_scraper(lnks)
    Scraper. Almost like just loop for parser.
    Args:
        lnks: list of links for single job
    Returns:
        list of PageResult instances it had obtain
    """
    logger.info('Interval scraper started. Have %s links', len(lnks))
    logger.debug('-' * 20)

    options = webdriver.ChromeOptions()
    for arg in CFG.CHROME_DRIVER_ARGS:
        options.add_argument(arg)
    driver = webdriver.Chrome(options=options)

    full_result = []
    for i, link in enumerate(lnks):
        interparse_sleep = random.randint(
            CFG.SCRAPER_INTERPARSE_MIN, CFG.SCRAPER_INTERPARSE_MAX
        )
        logger.info(
            'Scrape link №%s of %s. Sleep: %s sec', i + 1, len(lnks), interparse_sleep
        )
        time.sleep(interparse_sleep)
        start_time = time.time()
        ##########################
        # LINE BELOW RUNS PARSER #
        ##########################
        full_result.append(wb_parser(driver=driver, link=link))
        end_time = time.time()
        logger.debug(  #  pylint: disable=logging-not-lazy
            '-' * 20 + ' PARSED in %s sec', round(end_time - start_time, 0)
        )
    beforequit_sleep = random.randint(
        CFG.SCRAPER_BEFOREQUIT_MIN, CFG.SCRAPER_BEFOREQUIT_MAX
    )
    logger.info('Driver will quit() after sleep: %s sec', beforequit_sleep)
    time.sleep(beforequit_sleep)
    driver.quit()
    return full_result


def dum_interval_scraper(lnks: List[str]) -> List[PageResult]:
    """
    Like interval_scraper(), but no requests to WB. Used for debugging of scheduler.
    Args:
        lnks: same as interval_scraper()
    Returns:
        list of PageResult instances it had obtain, same interval_scraper()
    """
    logger.info('Dummy interval scraper started. Have %s links', len(lnks))
    logger.debug('-' * 20)
    full_result = []
    for i, link in enumerate(lnks):
        logger.info('Scrape link №%s of %s', i + 1, len(lnks))
        start_time = time.time()
        full_result.append(dummy_parser(i, link))
        time.sleep(CFG.SEC_WAIT_DUMMYSCRAPER)
        end_time = time.time()
        logger.debug(  #  pylint: disable=logging-not-lazy
            '-' * 20 + ' DONE in %s sec', round(end_time - start_time, 0)
        )
    return full_result
