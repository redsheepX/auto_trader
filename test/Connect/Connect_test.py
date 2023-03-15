import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))


from all_libs.Connect.sites import BingX


class ConnectBingXTest(unittest.TestCase):
    def setUp(self) -> None:
        self.conn=BingX.BingX()
        self.conn.api_key="Zsm4DcrHBTewmVaElrdwA67PmivPv6VDK6JAkiECZ9QfcUnmn67qjCOgvRuZVOzU"
        self.conn.timestamp="1615272721001"
        self.conn.currency="USDT"
        
    def signString_test(self):
        method="POST"
        api_path="/api/v1/user/getBalance"
        
        
        result=self.conn.gen_postUrl()
        excepted="https://api-swap-rest.bingbon.pro/api/v1/user/getBalance?apiKey=Zsm4DcrHBTewmVaElrdwA67PmivPv6VDK6JAkiECZ9QfcUnmn67qjCOgvRuZVOzU&currency=USDT&timestamp=1616488398013&sign=S7Ok3L5ROXSbYfXj9ryeBbKfRosh9tmH%2FAKiwj7eAoc%3D"
        self.assertEqual(result,excepted)
        
    


if __name__=='__main__':
    unittest.main()