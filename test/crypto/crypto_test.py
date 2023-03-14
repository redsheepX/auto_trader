import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from all_libs.crypto_data import crypto

class CryptoTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.btc=crypto.CryptoCurrency("BTC")
        return super().setUp()
    
    def test_BasicSetup(self):
        excepted = "BTC"
        result=self.btc.name
        self.assertEqual(excepted,result)
    
    def test_GetHistoryData(self):
        excepted = {}
        result = self.btc.get_history()
        self.assertEqual(excepted,result)

if __name__=='__main__':
    unittest.main()