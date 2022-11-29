from  sqlalchemy import create_engine
import logging
from  rich.logging  import RichHandler
import yaml 
from telethon import TelegramClient
from telethon.utils import get_extension
import os
from typing import Optional
import pandas as pd
from  sqlalchemy import create_engine
import asyncio
import traceback
from utils import decode_pass
import zipfile
import datetime

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
        self.chat_id='1'
        self.passw=decode_pass(config['PASSWORD'])
        # logging.info(decode_pass(config['PASSWORD']))
        self.ph =config['PHONE_NUMBER']
        # print(self.channel_ids)
        self.last_message_id=0
        self.config=dict()

        
        
    async def main(self,channel_ids,history_data,config):
        self.config=config
        
        for channel in channel_ids:
            os.makedirs(f'{os.getcwd()}\\{channel}',exist_ok=True)
            self.zf=zipfile.ZipFile(f'channel{datetime.datetime.now().date()}.zip', "a")

            self.client= await self.client_connect(self.api_id_config,self.api_hash_config)
            msg_id=self._is_exist(chat_id=channel,msg_id=1,action='message_id')
            if self.client:
                print('----> msg id',msg_id)
                print('data')
                await self.successive_data(message_id=msg_id,channel=channel)
                self.zf.close()

            #need to add the failed msg_id rerun
        self.engine.dispose()
              
    async def client_connect(self,api_id:int,api_hash:str):
        try:
            # api_id=25828699
            # api_hash='eea3a6141d6966d45c7475603a8b6739'
            client = TelegramClient('media_download', api_id, api_hash)
            await client.connect()
            if client.is_connected():
                logging.info('connected')
            return await client.start(phone=self.ph,password=self.passw)
        except:
            logging.warning('connection failed')
            return False
    # commeting out since the its not needed further      
    # async def history_data(self,channel:str):
    #     alloweded_media_list=['.pdf','.mp4','.jpg']
        
    #     try:
    #         #iterating through the messages
    #         async for d in  self.client.iter_messages(channel, reverse=True):
    #             if d.media and get_extension (d.media) in alloweded_media_list: # checking for the alllowded list
    #                 if not  self._is_exist(chat_id=str(d.chat_id),msg_id=d.id,action='check_exist'):# checking that if the data is already downloaded
    #                     filename=await d.download_media(file=f'{os.getcwd()}\\{channel}') #download media
    #                     if filename :
    #                         d=self.update_audict(file_nm=filename.split('\\')[-1],chat_id=str(d.chat_id),msg_id=d.id,date=str(d.date),status='Success',channel_nm=channel)
    #                     else:
    #                         d=self.update_audict(file_nm=filename.split('\\')[-1],chat_id=d.chat_id,msg_id=d.id,date=str(d.date),status='Fail',channel_nm=channel)
                        
    #     except Exception as e:
    #         print(traceback.format_exc())
    def _is_exist(self,chat_id:str,msg_id:Optional[int],action:str):
        if action=='check_exist':
            try:
                data=self.engine.execute(f"select distinct message_id,channel_id from telegram_loger.download_audict where message_id ={msg_id} and channel_id='{chat_id}' and status <> 'Fail' ;").fetchall()
                print('db data check------->',data)
                if data:
                    return True
                else:
                    return False
                    
            except Exception as e:
                print(traceback.format_exc())
                return False
        if action=='message_id':
            try:
                data=self.engine.execute(f"select max(message_id) as msg_id  from telegram_loger.download_audict where  channel_nm='{chat_id}' and status <> 'Fail' ;").fetchall()
                print(f"select max(message_id) as msg_id  from telegram_loger.download_audict where  channel_nm='{chat_id}' and status <> 'Fail' ;")
                print('db data message------->',data)
                
                if data[0]:
                    return data[0][0]
                else:
                    return 0
                    
            except Exception as e:
                print(traceback.format_exc())
                return 0
            
    def update_audict(self,chat_id:str,msg_id:int,date:str,file_nm:str,status:str,channel_nm:str) -> bool:
        try:
            self.engine.execute(f"INSERT INTO telegram_loger.download_audict(file_nm, channel_id, message_id, date,status,channel_nm) VALUES('{file_nm}', '{chat_id}', {msg_id}, '{date}','{status}','{channel_nm}');")
            return True
        except Exception as e:
            print(traceback.format_exc())
            return False
            

    async def successive_data(self,message_id:int,channel:str):
        alloweded_media_list=['.pdf','.mp4','.jpg']
        
        try:
            #iterating through the messages
            print('---->',message_id)
            async for d in  self.client.iter_messages(str(channel),min_id=int(message_id)):
                print(d)
                if d.media and get_extension (d.media) in alloweded_media_list: # checking for the alllowded list
                    if not  self._is_exist(chat_id=str(d.chat_id),msg_id=d.id,action='check_exist'):# checking that if the data is already downloaded
                        filename=await d.download_media(file=f'{os.getcwd()}\\{channel}') #download media
                        if filename :
                            d=self.update_audict(file_nm=filename.split('\\')[-1],chat_id=str(d.chat_id),msg_id=d.id,date=str(d.date),status='Success',channel_nm=channel)
                            self.zf.write(filename)
                        else:
                            d=self.update_audict(file_nm=filename.split('\\')[-1],chat_id=d.chat_id,msg_id=d.id,date=str(d.date),status='Fail',channel_nm=channel)
        except: 
            print(traceback.format_exc())
         
         
        
            

if __name__ =='__main__':
    
    config=yaml.load(open('config.yaml'),Loader=yaml.FullLoader)
    channel_ids=config['CHANNEL_ID']
    hist_flag=config['HISTORY_FLAG']
    executer=Media_downloader()
    asyncio.run(executer.main(channel_ids,hist_flag,config))


    
    


