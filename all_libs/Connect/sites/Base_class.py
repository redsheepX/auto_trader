import abc


class Connection(metaclass=abc.ABCMeta):
    
    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def account_balance(self):
        """獲得帳戶餘額"""
        return NotImplemented
    
    @abc.abstractmethod
    def get_historyKline(self):
        return NotImplemented

    @abc.abstractmethod
    def trade_buy(self):
        return NotImplemented
    
    @abc.abstractmethod
    def trade_sell(self):
        return NotImplemented
    
    @abc.abstractmethod
    def account_position(self):
        return NotImplemented