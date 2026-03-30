import fcntl
import requests
import time


def base_request(method: str, url: str, **kwargs):

    with open('/tmp/p115_api.lock', 'a') as f:
        try:
            fcntl.flock(f, fcntl.LOCK_EX)
            resp = requests.request(method=method, url=url, **kwargs)
            time.sleep(1)
            try:
                data = resp.json()
            except ValueError:
                data = {}
            return data

        finally:
            fcntl.flock(f, fcntl.LOCK_UN)
