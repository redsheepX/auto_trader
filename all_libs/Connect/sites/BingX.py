import os
import sys
rootPath=os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
sys.path.append(rootPath)

from all_libs.Connect.sites import Base_class



class BingX(Base_class.Connection):
    def __init__(self) -> None:
        
        super().__init__()

if __name__ == '__main__':
    a=BingX()

