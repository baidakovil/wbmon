# wbmon  
[![Pylint](https://github.com/baidakovil/wbmon/actions/workflows/pylint.yml/badge.svg)](https://github.com/baidakovil/wbmon/actions/workflows/pylint.yml)  [![Deployment](https://github.com/baidakovil/wbmon/actions/workflows/deployment.yml/badge.svg)](https://github.com/baidakovil/wbmon/actions/workflows/deployment.yml)

Wildberries marketplace prices monitor with publishing into Google Sheets.   
Sample of deployed and real-time running Google Sheets with results: [link](https://docs.google.com/spreadsheets/d/1xR6I6X6BsF1hWDuTIfhTfEY2hbvuAvaz6jiUnJ9G3g8/edit?usp=sharing).

## Table of contents
- [Functions](#functions)
- [Feedback](#feedback)
- [Built with](#built-with)
- [Deployment](#deployment-with-docker)
- [Contributing](#contributing)

## Functions
* Any possible schedules with APScheduler's CRON scheduler
* Parsed fields: 

## Built with
* python script to get price from WB html page with _selenim_  
* python script to send prices from python to google sheets with _pygsheets_  

  
## Stage 2  [DONE]
* six separate scripts:  
    - **main.py**   
    scheduler runner, main logger  
    - **config.py**  
    test/working sets of configs, lead by _dotenv-python_  
    - **gconnect.py**  
    _Gc_ class for automatic reconnection and worksheet  
    - **scheduler.py**  
    with _APSCheduler_  
    - **scraper.py**  
    pretty simple loop 
    - **wbparser.py**  
    _PageResult_ class for results storage, parse functions  
      
* automated links loading from *links* spreadsheet
* continuous working as systemd service with senging to goggle sheet


## Contributing

Please feel free to open pull requests. If you're planning on implementing
something big (i.e. not fixing a typo, a small bug fix, minor refactor, etc)
then please open an issue first.
