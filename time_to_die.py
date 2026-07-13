#!/bin/python3

import time
from pathlib import Path
import enums
import json

class TimeToDie:
    def __init__(self):
        self.SECTOR_CTIME = 40
        self.PRICES_CTIME =  10
        self.HISTORY_CTIME = 10 

        self.ttd_json = "ttd.json"
        epoch_time = time.time()

        self.cache_duration = {
            "SECTOR": int(epoch_time + self.SECTOR_CTIME),
            "PRICES": int(epoch_time + self.PRICES_CTIME),
            "HISTORY": int(epoch_time + self.HISTORY_CTIME),
        }

        self.init_cache_refresh_times()
#end init

    def init_cache_refresh_times(self):
        '''
            Take the cache expire time from the ttd.json if 
            it exists, otherwise create one with the cache times
            as set above
        '''
        cache_file = Path(self.ttd_json)

        if cache_file.exists():
            with open(self.ttd_json, "r", encoding="utf-8") as file:
                self.cache_duration = json.load(file)
                #print(f"{self.cache_duration}")
        else:
            with open(self.ttd_json, "w", encoding="utf-8") as file:
                json.dump(self.cache_duration, file, indent=4)
                #print("created ttd.json")
#end init cache refresh times

    def cache_expired(self, cache_name: str) -> bool:
        with open(self.ttd_json, "r", encoding="utf-8") as file:
            self.cache_duration = json.load(file)
            expire_cache = self.cache_duration[cache_name]
            if expire_cache < time.time():
                self.reset_cache(cache_name)
                return True
            else:
                return False
#end cache expired

    def reset_cache(self, cache_name: str) -> None:

        cache_time = time.time() + self.SECTOR_CTIME

        with open(self.ttd_json, "r+", encoding="utf-8") as file:
            self.cache_duration = json.load(file)
            self.cache_duration[cache_name] = cache_time
            file.seek(0)#back to top of file
            json.dump(self.cache_duration, file, indent=4)
            file.close()
    #end reset cache

#end class TimeToDie

def load_sector()-> None:
	print("Dummy method for testing")

if __name__ == "__main__":
    ttd = TimeToDie()
    if ttd.cache_expired('SECTOR'):
        load_sector()
        ttd.reset_cache('SECTOR')
    else:
        print("cache not expired")
