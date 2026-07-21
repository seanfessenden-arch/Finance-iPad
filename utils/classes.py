from datetime import datetime, timezone
from enum import Enum

class Mode(Enum):
    NORMAL = 0
    ADD = 1
    DELETE = 2
#end class Mode

class Cache(Enum):
    SECTOR = 0
    PRICES = 1
    HISTORY = 2
#end class Cache

class TransactionType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    DIVIDEND = "DIVIDEND"
    SPLIT = "SPLIT"
#end class TransactionType

class Stock:
    def __init__(self, db_id, symbol, name):
        self.db_id = db_id
        self.symbol = symbol
        self.company_name = name
#end class Stock
