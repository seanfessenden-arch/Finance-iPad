#!/bin/python3

import json
import time
from pathlib import Path


class TimeToDie:

	def __init__(self):

		self.ttd_json = Path("cache/ttd.json")

		self.cache_times = {
			"SECTOR": 40,
			"PRICES": 10,
			"HISTORY": 10,
		}

		self.cache_duration = {}

		self._load()

	#---------------------------------------------------------
	def _default_cache(self):

		now = int(time.time())

		return {
			name: now + seconds
			for name, seconds in self.cache_times.items()
		}

	#---------------------------------------------------------
	def _load(self):

		if not self.ttd_json.exists():
			self.cache_duration = self._default_cache()
			self._save()
			return

		try:
			with open(self.ttd_json, "r", encoding="utf-8") as file:
				self.cache_duration = json.load(file)

		except (json.JSONDecodeError, OSError):
			self.cache_duration = self._default_cache()
			self._save()

	#---------------------------------------------------------
	def _save(self):

		with open(self.ttd_json, "w", encoding="utf-8") as file:
			json.dump(self.cache_duration, file, indent=4)

	#---------------------------------------------------------
	def cache_expired(self, cache_name):

		self._load()

		if cache_name not in self.cache_duration:
			self.reset_cache(cache_name)
			return True

		if time.time() >= self.cache_duration[cache_name]:
			self.reset_cache(cache_name)
			return True

		return False
	#---------------------------------------------------------
	def reset_cache(self, cache_name):

		self._load()

		seconds = self.cache_times.get(cache_name, 60)

		self.cache_duration[cache_name] = int(time.time()) + seconds

		self._save()

#end class TimeToDie


if __name__ == "__main__":

	ttd = TimeToDie()

	if ttd.cache_expired("HISTORY"):
		print("expired")
		ttd.reset_cache("HISTORY")
	else:
		print("cache valid")
