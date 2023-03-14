

class CryptoCurrency:
    def __init__(self,crypto_name:str,dataFrom,crypto_base:str="USDT") -> None:
        self.name=crypto_name.upper()
        self.id=crypto_base.upper()
        self.dataFrom=dataFrom
