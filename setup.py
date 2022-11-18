#create the db
#install the requirement.txt file
#make the download path for each channel
#confirm if all the requirements are fullfilled if not dont run the code

import yaml
import logging
from rich.logging  import RichHandler
import os



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
    pass



if __name__ =='__main__':
    main()