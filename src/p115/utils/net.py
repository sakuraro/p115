import fcntl
import requests
import time
from requests.exceptions import RequestException
from .log import log_info, log_debug, log_error


def base_request(method: str, url: str, **kwargs):

    with open('/tmp/p115_api.lock', 'a') as f:
        try:
            fcntl.flock(f, fcntl.LOCK_EX)
            log_debug(f'request: {method} {url} {kwargs}')
            try:
                resp = requests.request(method=method, url=url, **kwargs)
                data = resp.json()
            except RequestException:
                log_error(f'RequestException: request: {method} {url} {kwargs}')
                data = {}
            except ValueError:
                log_error(f'ValueError: response: {resp.text}')
                data = {}
            log_debug(f'response: {data}')
            return data

        finally:
            fcntl.flock(f, fcntl.LOCK_UN)
