import fcntl
import requests
import time
from .log import log_info


def base_request(method: str, url: str, **kwargs):

    with open('/tmp/p115_api.lock', 'a') as f:
        try:
            fcntl.flock(f, fcntl.LOCK_EX)
            log_info(f'request: {method} {url} {kwargs}')
            resp = requests.request(method=method, url=url, **kwargs)
            try:
                data = resp.json()
            except ValueError:
                data = {}
            log_info(f'response: {data}')
            return data

        finally:
            fcntl.flock(f, fcntl.LOCK_UN)
