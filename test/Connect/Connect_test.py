import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))


from all_libs.Connect import ConnectControl


class ConnectBingXTest(unittest.TestCase):
    def setUp(self) -> None:
        connection=ConnectControl.Connection("BingX")
        
    


if __name__=='__main__':
    unittest.main()