import os

import requests
import functools
import time


class Logger:
    method_url = f'http://{os.environ.get("PROMETHEUS_EXPORTER_HOST", "localhost")}:' \
                 f'{os.environ.get("PROMETHEUS_EXPORTER_PORT", "5555")}/track_methods_metric'

    def __init__(self, level: str = "info"):
        self.level = level

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Logger, cls).__new__(cls)
        return cls.instance

    @staticmethod
    def log_method_duration(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            method_name = func.__name__
            start = time.time()
            response = func(*args, **kwargs)
            payload = {"duration": time.time() - start, "method": method_name}
            Logger.send_message(payload=payload, url=Logger.method_url)
            return response
        return wrapper

    @staticmethod
    def log_async_method_duration(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            method_name = func.__name__
            start = time.time()
            response = await func(*args, **kwargs)
            payload = {"duration": time.time() - start, "method": method_name}
            Logger.send_message(payload=payload, url=Logger.method_url)
            return response
        return wrapper


    @classmethod
    def send_message(cls, payload: dict, url: str):
        try:
            requests.post(url=url, json=payload)
            print("Metrics sent: ", payload)
        except:
            print("Can't push metrics", payload)
