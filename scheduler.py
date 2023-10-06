import os
import logging
import time
from datetime import datetime, timedelta
from tzlocal import get_localzone

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from config import Cfg
from gconnect import start_gsheets, post_values, dummy_post_values
from scraper import interval_scraper, dum_interval_scraper

BOT_FOLDER = os.path.dirname(os.path.realpath(__file__))
CFG = Cfg()


logger = logging.getLogger('A.GC')
logger.setLevel(logging.DEBUG)


def get_scheduler():

    lnks, gc = start_gsheets()

    scheduler = BlockingScheduler()
    trigger = CronTrigger(
        **CFG.CRON_ARGS
    )

    kwargs = {'lnks': lnks[:CFG.MAX_LINK_QUANTITY],
              'gc': gc,
              'trigger': trigger}

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
            job.modify(next_run_time=datetime.now() +
                       timedelta(seconds=CFG.ASAPDELAY))
            logger.info(
                f'TIME OF NEXT JOB CHANGED. {CFG.ASAPDELAY} sec to run')

    return scheduler


def interval_job(lnks, gc, trigger):
    start_time = time.time()
    logger.debug('='*20+' JOBSTARTED')

    post_values(
        gc=gc,
        full_result=interval_scraper(lnks),
    )
    end_time = time.time()
    logger.debug('='*20+f' JOBDONE in {round(end_time - start_time,0)} sec')
    calc_delay(trigger)


def get_dum_scheduler(asap, kwargs):

    scheduler = BlockingScheduler()
    trigger = CronTrigger(
        second="*/30",
        jitter=5,
    )
    kwargs['trigger'] = trigger
    scheduler.add_job(
        func=dummy_interval_job,
        trigger=trigger,
        kwargs=kwargs,
        name='My dummy job for interval scraping',
        misfire_grace_time=300,
        coalesce=True,
    )
    if asap and (calc_delay(trigger).total_seconds() > CFG.ASAPTRIGGER):
        for job in scheduler.get_jobs():
            job.modify(next_run_time=datetime.now() +
                       timedelta(seconds=CFG.ASAPDELAY))
            logger.info(
                f'TIME OF NEXT JOB CHANGED. {CFG.ASAPDELAY} sec to run')
    return scheduler


def dummy_interval_job(lnks, sh_id, gc, sh, wks, trigger):
    start_time = time.time()
    logger.debug('='*20+' JOBSTARTED')
    dummy_post_values(
        gc=gc,
        full_result=dum_interval_scraper(lnks),
    )
    end_time = time.time()
    logger.debug('='*20+f' JOBDONE in {round(end_time - start_time,0)} sec')
    calc_delay(trigger)


def calc_delay(trigger):
    now = datetime.now(tz=get_localzone())
    next_time = trigger.get_next_fire_time(None, now)
    delay = next_time-now
    logger.info(
        f"\nNEXT JOB RUN @ {next_time.strftime('%d/%m/%Y %H:%M:%S')} WAIT {delay} sec\n")
    return delay
