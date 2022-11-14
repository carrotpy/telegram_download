from  sqlalchemy import create_engine
import logging
from  rich.logging  import RichHandler
import telethon
import yaml 

config=yaml.safe_load('config.yaml')

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()],
)

log=logging.getLogger('download_log')

class Media_downloader():
    
    def __init__(self) -> None:
        self.downd_path=''
        
        pass
    


