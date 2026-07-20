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

##############

# Example epoch timestamp (in seconds)
def convert_epoch(e_time:int) -> str:
    epoch_seconds = e_time

    # Convert to UTC datetime object
    dt_utc = datetime.fromtimestamp(epoch_seconds, timezone.utc)

    return dt_utc
# Output: 2024-06-20 00:00:00+00:00

def percent_gain(initial_price, final_price):
    if initial_price <= 0:
        raise ValueError("Initial price must be greater than zero.")
        
    gain = final_price - initial_price
    percent_gain = (gain / initial_price) * 100
    return percent_gain
