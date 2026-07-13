from enum import Enum

class Mode(Enum):
    NORMAL = 0
    ADD = 1
    DELETE = 2

class Cache(Enum):
    SECTOR = 0
    PRICES = 1
    HISTORY = 2

class TransactionType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    DIVIDEND = "DIVIDEND"
    SPLIT = "SPLIT"
