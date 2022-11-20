from  sqlalchemy import create_engine
from  rich.logging  import RichHandler
import base64
import yaml

def decode_pass(encode:str) -> str:
    sample_string_bytes = encode.encode("ascii")
  
    base64_bytes = base64.b64decode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string

def write_into_yaml(config:dict):
    with open('config.yaml') as file:
        documents = yaml.dump(config, file)

    
    
