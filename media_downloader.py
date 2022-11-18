from  sqlalchemy import create_engine
import logging
from  rich.logging  import RichHandler
import yaml 
from telethon import TelegramClient
from telethon.utils import get_extension
import os
import pandas as pd
from  sqlalchemy import create_engine
import asyncio
import traceback
from utils import decode_pass

config=yaml.load(open('config.yaml'),Loader=yaml.FullLoader)



logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()],
)

log=logging.getLogger('download_log')

# logging.info(config)

class Media_downloader():
    
    def __init__(self) -> None:
        self.engine=create_engine("postgresql://postgres:Carrotpy123@localhost/postgres")
        self.downd_path=''
        self.client=''
        self.api_hash_config=config['API_HASH']
        self.api_id_config=config['API_ID']
        self.channel_ids=config['CHANNEL_ID']
        self.passw=decode_pass(config['PASSWORD'])
        # logging.info(decode_pass(config['PASSWORD']))
        self.ph =config['PHONE_NUMBER']
        # print(self.channel_ids)
        self.last_message_id=0

        
        
    async def main(self):
        self.client= await self.client_connect(self.api_id_config,self.api_hash_config)
        if self.client:
            await self.history_data()
              
    async def client_connect(self,api_id:int,api_hash:str):
        try:
            # api_id=25828699
            # api_hash='eea3a6141d6966d45c7475603a8b6739'
            client = TelegramClient('media_download', api_id, api_hash)
            await client.connect()
            if client.is_connected():
                logging.info('connected')
            return await client.start(phone=self.ph_nm,password=self.passw)
        except:
            logging.warning('connection failed')
            return False
        
    async def history_data(self):
        alloweded_media_list=['.pdf','.mp4','.jpg']
        
        try:
            async for d in  self.client.iter_messages('iamadhee', reverse=False):
                if d.media and get_extension (d.media) in alloweded_media_list:
                    if not  self._is_exist(chat_id=str(d.chat_id),msg_id=d.id):
                        filename=await d.download_media(file=f'{os.getcwd()}\\iamadhee')
                        if filename :
                            d=self.update_audict(file_nm=filename.split('\\')[-1],chat_id=str(d.chat_id),msg_id=d.id,date=str(d.date),status='Success')
                        else:
                            d=self.update_audict(file_nm=filename.split('\\')[-1],chat_id=d.chat_id,msg_id=d.id,date=str(d.date),status='Fail')
                        
        except Exception as e:
            print(traceback.format_exc())
    def _is_exist(self,chat_id:str,msg_id:int) -> bool:
        
        try:
            data=self.engine.execute(f"select distinct message_id,channel_id from telegram_loger.download_audict where message_id ={msg_id} and channel_id='{chat_id}' and status <> 'Fail' ;").fetchall()
            print(data)
            if data:
                return True
            else:
                return False
                
        except Exception as e:
            print(traceback.format_exc())
            return False
            
        finally:
            self.engine.dispose()
    def update_audict(self,chat_id:str,msg_id:int,date:str,file_nm:str,status:str) -> bool:
        try:
            self.engine.execute(f"INSERT INTO telegram_loger.download_audict(file_nm, channel_id, message_id, date,status) VALUES('{file_nm}', '{chat_id}', {msg_id}, '{date}','{status}');")
            return True
        except Exception as e:
            print(traceback.format_exc())
            return False
            
        finally:
            self.engine.dispose()

        

if __name__ =='__main__':

    executer=Media_downloader()
    asyncio.run(executer.main())
    


