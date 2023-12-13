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
"""This file contains high-level scheduling functns, running interval_scraper() job."""

import logging
import os
import time
from datetime import datetime, timedelta
from typing import List

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from tzlocal import get_localzone

from config import Cfg
from parsing.scraper import interval_scraper
from services.gconnect import Gc, post_values, start_gsheets

CFG = Cfg(test=os.getenv('TEST') == 'true')
logger = logging.getLogger('A.GC')
logger.setLevel(logging.DEBUG)


def get_scheduler() -> BlockingScheduler:
    """
    Runs parsing process once at start: connect GSheets, load links, set schedule jobs.
    Returns:
        the only scheduler
    """

    lnks, gc = start_gsheets()
    #  From doc: «A scheduler that runs in the foreground (start() will block)».
    scheduler = BlockingScheduler()
    trigger = CronTrigger(**CFG.CRON_ARGS)
    kwargs = {'lnks': lnks[0 : CFG.MAX_LINK_QUANTITY], 'gc': gc, 'trigger': trigger}

    scheduler.add_job(
        func=interval_job,
        trigger=trigger,
        kwargs=kwargs,
        name='My job for interval scraping',
        misfire_grace_time=CFG.MISFIRE_TIME,
        coalesce=True,
    )
    if CFG.ASAP and (calc_delay(trigger).total_seconds() > CFG.ASAPTRIGGER):
        for job in scheduler.get_jobs():
            job.modify(next_run_time=datetime.now() + timedelta(seconds=CFG.ASAPDELAY))
            logger.info('TIME OF NEXT JOB CHANGED. %s sec to run', CFG.ASAPDELAY)

    return scheduler


def interval_job(lnks: List[str], gc: Gc, trigger: CronTrigger) -> None:
    """
    Function executed by the BlockingScheduler: logging + sending links to scraper.
    Args:
        lnks: list of links to load in single job
        gc: Gc class instance with active google sheets connection
        trigger: Active apscheduler trigger to write info about next run
    """
    start_time = time.time()
    logger.info('=' * 20 + ' JOBSTARTED')
    post_values(gc=gc, full_result=interval_scraper(lnks))
    end_time = time.time()
    logger.info('=' * 20 + ' JOBDONE in %s sec', round(end_time - start_time, 0))
    calc_delay(trigger)


def calc_delay(trigger: CronTrigger) -> timedelta:
    """
    Obtain next time job running and calculates waiting interval.
    Args:
        trigger: jobtrigger.
    Returns:
        datetime.timedelta(), i.e. time to wait. If no interval exist, zero timedelta.
    """
    now = datetime.now(tz=get_localzone())
    next_time = trigger.get_next_fire_time(None, now)
    if not next_time:
        logger.warning('NEXT JOB RUN CAN NOT BE CALCULATED')
        return timedelta(days=0)
    delay = next_time - now
    logger.info(
        '\n\nNEXT JOB RUN @ %s WAIT %s hr %s min\n',
        next_time.strftime('%d/%m/%Y %H:%M:%S'),
        delay.seconds // 3600,
        (delay.seconds // 60) % 60,
    )
    return delay
