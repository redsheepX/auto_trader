import abc


class Connection(metaclass=abc.ABCMeta):
    
    def __init__(self) -> None:
        pass
    @abc.abstractmethod
    def getBalance(self) -> dict:
        """獲得帳戶數據
        """
        return NotImplemented