# wbmon  
The app to continuous prices monitoring on Wildberries marketplace  
  
## Stage 1   
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

## Stage 3 [PAUSED]

* More parse functions
* Database storage
* Function definitions
* python-typing

## Stage 4

* Proxy rotating
