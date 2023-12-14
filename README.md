# wbmon  
[![Pylint](https://github.com/baidakovil/wbmon/actions/workflows/pylint.yml/badge.svg)](https://github.com/baidakovil/wbmon/actions/workflows/pylint.yml)  [![Deployment](https://github.com/baidakovil/wbmon/actions/workflows/deployment.yml/badge.svg)](https://github.com/baidakovil/wbmon/actions/workflows/deployment.yml)

Wildberries marketplace prices monitor with publishing into Google Sheets.   
Sample of deployed and real-time running Google Sheets with results: [spreadsheet].

## Features
* Scheduling with `cron trigger`: APScheduler's [doc]
* Saving fields: `timestamp`, `link`, `brand name`, `goods name`, `seller`, `id`, `customer price`, `seller price`
* Reading **list of links** from Google Sheet or from file
* Publishing **parsed results** to Google Sheet and to file
* Detailed logging: [sample] 

[doc]: https://apscheduler.readthedocs.io/en/stable/modules/triggers/cron.html?highlight=week#apscheduler.triggers.cron.CronTrigger
[spreadsheet]: https://docs.google.com/spreadsheets/d/1wWehURjMgs6n4GlEl9EEvLRQomgIva5awKEYg2nBnvk/edit?usp=sharing
[sample]: /docs/logger_example.png

## Built with

#### Online-services
**[Wildberries]** - Online-marketplace, one of three leading in CIS  
**[Google Sheets]** - Spreadsheet application offered by Google  
**[Google Cloud APIs and services]** - you'll need create *project* in it, as an interface between **pygsheets** and **Google Sheets** 

#### Software
**[Python]** - Language to work quickly and integrate systems more effectively **|** *GPL compatible*  
**[APScheduler]** - Advanced Python scheduler coming with python-telegram-bot **|** *MIT*  
**[selenium]**  python script to get price from WB html page with **|** *Apache 2*  
**[pygsheets]** - library to access google spreadsheets through the Google Sheets API v4 **|** *MIT*  
**[python-dotenv]** - Read key-value pairs from a .env file and set them as envir-t variables **|** *BSD* 


[pygsheets]: https://github.com/nithinmurali/pygsheets
[python-dotenv]: https://pypi.org/project/python-dotenv/
[APScheduler]: https://apscheduler.readthedocs.io/en/3.x/userguide.html  
[Python]: https://www.python.org/
[selenium]: https://pypi.org/project/selenium/
[Wildberries]: https://www.wildberries.ru/
[Google Sheets]: https://google.com/sheets
[Google Cloud APIs and services]: https://console.cloud.google.com/apis/

## Contributing

Please feel free to open pull requests. If you're planning on implementing
something big (i.e. not fixing a typo, a small bug fix, minor refactor, etc)
then please open an issue first.
