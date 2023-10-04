import logging
import time
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from gconnect import post_values, dummy_post_values
from scraper import interval_scraper, dum_interval_scraper

logger = logging.getLogger('A.GC')
logger.setLevel(logging.DEBUG)


def interval_job(lnks):
    lnks, gc, sh, wks = start_gsheets()
    post_values(
                sh_id=sh.id,
                gc=gc,
                sh=sh,
                wks=wks,
                full_result=interval_scraper(lnks),
                )
    print(f'Count of Links: {len(lnks)}\nSpreadsheet Title: {sh.title}')

def get_dum_scheduler(kwargs):
    scheduler = BlockingScheduler()
    trigger = CronTrigger(
                        hour="*",
                        second="*/30",
                        jitter=5,
                        )
    kwargs['trigger']=trigger
    scheduler.add_job(
                    func=dummy_interval_job,
                    trigger=trigger,
                    kwargs=kwargs,
                    name='My job for interval scraping',
                    misfire_grace_time=300,
                    coalesce=True,
                    )
    print("NEXT JOB RUN @ ", trigger.get_next_fire_time(None, datetime.now()))
    return scheduler

def dummy_interval_job(lnks,sh_id,gc,sh,wks,trigger):
    start_time = time.time()
    logger.debug('='*20+' JOBSTARTED')
    dummy_post_values(
                sh_id=sh_id,
                gc=gc,
                sh=sh,
                wks=wks,
                full_result=dum_interval_scraper(lnks),
                )
    end_time = time.time()  
    logger.debug('='*20+f' JOBDONE in {round(end_time - start_time,0)} sec')
    print('\n')
    print("NEXT JOB RUN @ ", trigger.get_next_fire_time(None, datetime.now()))
    print('\n')