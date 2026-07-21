#!/bin/python3
import logging
import functools

class ManagedLogger:
    # We use a class-level variable to store the actual logger instance
    _logger = None
    _saved_level = logging.INFO

    @classmethod
    def init_logger(cls, name="GlobalAppLogger", initial_level=logging.INFO, log_file="app.log"):
        cls._logger = logging.getLogger(name)
        if not cls._logger.handlers:
            handler = logging.FileHandler(log_file, mode="a")
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            cls._logger.addHandler(handler)
        cls._logger.setLevel(initial_level)
        cls._saved_level = initial_level

    @classmethod
    def disable(cls):
        if cls._logger:
            cls._saved_level = cls._logger.level
            cls._logger.setLevel(logging.CRITICAL)

    @classmethod
    def enable(cls):
        if cls._logger:
            cls._logger.setLevel(cls._saved_level)

    # By making the decorator a static method, it is available 
    # to your classes instantly without needing an object instance created first
    @staticmethod
    def log(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if ManagedLogger._logger:
                ManagedLogger._logger.info(f"Executing: '{func.__name__}'")
            return func(*args, **kwargs)
        return wrapper

