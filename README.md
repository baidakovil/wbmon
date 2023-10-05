# wbmon  
The app to continuous prices monitoring on Wildberries marketplace  
  
## Stage 1   
* python script to get price from WB html page with _selenim_  
* python script to send prices from python to google sheets with _pygsheets_  
  
## Stage 2  
* separate scripts:  
    - **main.py**   
    with only run the scheduler  and logger  
    - **config.py**  
    with test/working sets, lead by _dotenv-python_  
    - **gconnect.py**  
    with _Gc_ class for automatic reconnection and worksheet
    - **scheduler.py**  
    with _APSCheduler_
    - **scraper.py**  
    from Stage 1
* automated links loading from *links* spreadsheet
* continuous working as systemd service with senging to goggle sheet