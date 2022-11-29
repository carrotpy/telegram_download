# Annyeonghaseyo!
What do i do?
1. setup.py
 > I am a py file ,I install all the requirements and create necessary tables those associated with the projects
    my prerequsites are(python3,and postgres need to be installed)
    to run me please give the following comment in terminal
    `python3 setup.py &>> setup_log.log`
2. utils.py
    >I am just an supporting file Technically i have some functions that would be needed during execution
3. media_downloader.py
  > **I am the king** technically i am the main file i have all the sub functions that need to download the telegram
   `python3 media_downloader.py >> download_log.log`
4. details that need to be filed in yaml
   ```  
     1. CHANNEL_ID: ['Tamil_bookss'] # list of channels that need to download
     2. API_HASH: '' # api hash we got from the telegram.org
     3. API_ID: ''# api id we got from the telegram.org
     4. PHONE_NUMBER: ''# Your mobile number
     5. PASSWORD : '' # Your telegram password
     6. BOT_TOKEN: '' #if you have bot token use this
     7. SETUP_STATUS: False ' # its just for my purpose







