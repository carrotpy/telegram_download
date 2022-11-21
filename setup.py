#create the db
#install the requirement.txt file
#make the download path for each channel
#confirm if all the requirements are fullfilled if not dont run the code

import yaml
import logging
from rich.logging  import RichHandler
import os
import subprocess as sp
from  sqlalchemy import create_engine


config=yaml.load(open('config.yaml'),Loader=yaml.FullLoader)



logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()],
)

log=logging.getLogger('setup_log')

def main():
    #run setup checks one by one if its precedder is succesfullly executed
    #else stop there and put false in yaml "SETUP_STATUS"
    sp.Popen('pip3 install  -r requirements.txt', shell=True,close_fds=True)
    
    engine=create_engine("postgresql://postgres:Carrotpy123@localhost/postgres")
    try:
        engine.execute('CREATE SCHEMA telegram_loger AUTHORIZATION postgres;')
        engine.execute('''CREATE TABLE telegram_loger.download_audict (
        file_nm varchar NOT NULL,
        channel_id varchar NOT NULL,
        message_id int8 NOT NULL,
        "date" date NULL,
        status varchar NULL,
        channel_nm varchar NULL,
        CONSTRAINT download_audict_pkey PRIMARY KEY (channel_id, message_id)
    );''')
    except Exception as e:
        logging.info({e})
    finally:
        engine.dispose()
    
        
    pass



if __name__ =='__main__':
    main()