import os
import sys
rootPath=os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
sys.path.append(rootPath)

from all_libs.Connect.sites import Base_class
import configparser
import requests
import base64
import hmac
from hashlib import sha256
import urllib.parse
from json import loads

class BingX(Base_class.Connection):
    def __init__(self) -> None:
        super().__init__()
        config=configparser.ConfigParser()
        config.read(f"{rootPath}/Setting/Connect/ConnectSetup.ini")
        self.api_key=config["BingX"]["ApiKey"]
        self.secret_key=config["BingX"]["SecretKey"]
        self.api_url="https://api-swap-rest.bingbon.pro"
        self.currency="USDT"
        
    def gen_postUrl(self,method:str,api_path:str,):
        
        pass

    def gne_Signature(self,data:str) -> str:
        return urllib.parse.quote_plus(str(base64.b64encode(hmac.new(self.secret_key.encode('utf-8'),data.encode('utf-8'),digestmod=sha256).digest()),"utf-8"))



if __name__ == '__main__':
    a=BingX()
    
