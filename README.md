# wbmon  
[![Pylint](https://github.com/baidakovil/wbmon/actions/workflows/pylint.yml/badge.svg)](https://github.com/baidakovil/wbmon/actions/workflows/pylint.yml)  [![Deployment](https://github.com/baidakovil/wbmon/actions/workflows/deployment.yml/badge.svg)](https://github.com/baidakovil/wbmon/actions/workflows/deployment.yml)

Wildberries marketplace prices monitor with publishing into Google Sheets.   
Sample of deployed and real-time running Google Sheets with results: [spreadsheet].

## Features
* Scheduling of parsed intervals with power of `cron scheduler`: see in APScheduler's [doc]
* Saving fields: `timestamp`, `link`, `brand name`, `goods name`, `seller`, `id`, `customer price`, `seller price`
* Reading **list of links** from Google Sheet or from file
* Publishing **parsed results** to Google Sheet and to file
* Detailed logging: [sample] 
* Up-to-date parsing conditions 👍

## Built with

#### Online-services
**[Wildberries]** - Online-marketplace, one of three leading in CIS  
**[Google Sheets]** - Spreadsheet application offered by Google  
**[Google Cloud APIs and services]** - you'll need create *project* in it to connect **pygsheets** and **Google Sheets** 

#### Software
**[Python]** - Language to work quickly and integrate systems more effectively **|** *GPL compatible*  
**[APScheduler]** - Advanced Python scheduler coming with python-telegram-bot **|** *MIT*  
**[selenium]**  python script to get price from WB html page with **|** *Apache 2*  
**[pygsheets]** - library to access google spreadsheets through the Google Sheets API v4 **|** *MIT*  
**[python-dotenv]** - Read key-value pairs from a .env file and set them as envir-t variables **|** *BSD* 


[doc]: https://apscheduler.readthedocs.io/en/stable/modules/triggers/cron.html#api
[spreadsheet]: https://docs.google.com/spreadsheets/d/1wWehURjMgs6n4GlEl9EEvLRQomgIva5awKEYg2nBnvk/edit?usp=sharing
[sample]: /docs/logger_example.png

[Wildberries]: https://www.wildberries.ru/
[Google Sheets]: https://google.com/sheets
[Google Cloud APIs and services]: https://console.cloud.google.com/apis/

[pygsheets]: https://github.com/nithinmurali/pygsheets
[python-dotenv]: https://pypi.org/project/python-dotenv/
[APScheduler]: https://apscheduler.readthedocs.io/en/3.x/userguide.html  
[Python]: https://www.python.org/
[selenium]: https://pypi.org/project/selenium/

## How to run

Before running app these bare steps required:
1. Create project in Google Cloud Console to authorize pygsheets. Google account is required
2. Install dependencies
3. Finish authentification flow by following URL, given Google and pasting answer code
4. Prepare list of your links into one of two sources: Google Sheet or text file

#### 1. Create project in Google Cloud Console

- In order to authorize `pygsheets` and have ability to publish parsed results to Google Sheets, please follow [pygsheet instruction], following method
**OAuth Credentials**
- Doing that, on stage 7 choose [Desktop app]. Keep *Publishing status* to *Testing*
- Download credentials and put it in the app folder with name `client_secret.json`. The
  name controlled by `OAUTH_CREDENTIALS_FILE` setting

#### 2. Installing dependencies

* Create project folder and clone the project:
    ```
    $ cd /projects/project-folder/
    $ git clone https://github.com/baidakovil/wbmon .
    ```

* (Optional, recommended) Create dedicated virtual environment to use the bot and  
    activate it. I use *virtualenv*, some *venv*. Path and name are to your discretion. 
    ```
    $ cd /virtual-environments-folder/
    $ virtualenv env_name
    $ source env_name/bin/activate
    ```

* With virtual env activated, `cd` into project folder and install dependencies:
    ```
    $ cd /project-folder/
    $ python3 -m pip install -r requirements.txt
    ```

#### 3. Prepare links to parse
- If you want to store links in Google Sheets, create spreadsheet with name `links` in
  Google Account that you will authorize in next step. Then, paste links in **column
  A**, starting from cell A1 down to A2 and below. Example of [links file]
- Simplest way: create file `links.txt` in project folder, where each line will consist URL started with *https:// www.wildberries...*. When program will not find `links` spreadsheet, it will read this file.

    *Notice*: `links` and `links.txt` are defined by `LINKS_SPREADSHEET_NAME` and
    `LINKS_FILE` in `config.py`  
    *Notice*: you can use different Google accounts to create project in **1** (*User1*) and to store spreadsheets (*User2*). How to: add user *User2* in the section *[Test users]* at Google Cloud Console, and choose *User2* in the next, **4** step.

#### 4. Finish authorization
* With virtual environment activated, run the program:
    ```
    $ cd /project-folder/
    $ python main.py
    ```
* Look into console: you will be prompted with message

    ```
    Please go to this URL and finish the authentication flow: https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=...
    ```
* Open link in browser, authorize your Google account, copy code and paste it to console. You'll see `sheets.googleapis.com-python.json` file in project folder. This step should be passed once for given `client_secret.json` file.

    *Notice*: with *Publishing status* set to *Testing*, token will expire after 7 days. Unfortunately, I can't manage authorization after setting *Publishing status* to *Production*, though this documented to be OK. Hope you'll be more lucky, if you need more than 7 days of continuous work.


[Test users]: /docs/test_users.png
[Desktop app]: /docs/oauth_app_type.png
[pygsheet instruction]: https://pygsheets.readthedocs.io/en/stable/authorization.html
[links file]: https://docs.google.com/spreadsheets/d/1iRMm0IiBFxok6jCC_2m1EVyhHbNR_tRsm9La17UOEu4/


## How to deploy 24/7

There is nothing special about the deployment of this application compared to other python applications. I do it with **systemd**, in the way as described in [manual deployment] section of my favourit Green Grass Bot project. For this type of deployment I have attach sample file `scripts/wbmon.service-example` and `deployment.yml` workflow in `.github` folder. It works well.

[manual deployment]: https://github.com/baidakovil/GreenGrassBot#manual-deployment

## What matters

#### Look at config
Many things are defined by settings in the `config.py` file. It is well-documented, so read it all. 
With  `.env` file you can control two modes: *test* and *working*. For test mode be enabled, `.env` file should consist exactly `TEST='false'` string.
Notice, there are 3 sections in `config.py`: 
- *COMMON SETTINGS* — settings with values, similar for *test* and *working* modes
- *TEST CONFIG* — setting values for *test* mode
- *WORKING CONFIG* — setting values for *working* mode 

#### Ask questions
If you stuck, please feel free to contact me

## Contributing

Please feel free to open pull requests. If you're planning on implementing
something big (i.e. not fixing a typo, a small bug fix, minor refactor, etc)
then please open an issue first.
