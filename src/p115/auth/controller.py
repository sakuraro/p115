import json
import time
import qrcode
from functools import wraps
from pathlib import Path

from .api import auth_device_code, get_qrcode_status, device_code_to_token, refresh_access_token
from p115.utils.crypto import gen_code_verifier_and_challenge


def load_login_info(cache_file=None):
    p = Path(cache_file) if cache_file else (Path.home() / Path('.cache/115_auth.json'))
    with p.open(mode='r', encoding='utf-8') as f:
        try:
            login_info = json.load(f)
        except Exception:
            login_info = {}
    access_token = login_info.get('access_token', None)
    refresh_token = login_info.get('refresh_token', None)
    expires_in = login_info.get('expires_in', None)

    return access_token, refresh_token, expires_in


def dump_login_info(access_token=None, refresh_token=None, expires_in=None, cache_file=None):
    login_info = {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'expires_in': expires_in
    }

    p = Path(cache_file) if cache_file else (Path.home() / '.cache/115_auth.json')
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open(mode='w', encoding='utf-8') as f:
        json.dump(login_info, f)


def login_oauth_code_pkce(cache_file=None):
    access_token, refresh_token, expires_in = load_login_info()

    data = refresh_access_token(refresh_token)
    if data.get('code') == 0 and data.get('state') == 1 and data.get('errno') == 0:
        access_token = data.get('data', {}).get('access_token')
        refresh_token = data.get('data', {}).get('refresh_token')
        expires_in = data.get('data', {}).get('expires_in')

    else:
        code_challenge, code_verifier = gen_code_verifier_and_challenge()
        data = auth_device_code('100195125', code_challenge, 'sha256')
        uid = data.get('data', {}).get('uid')
        _time = data.get('data', {}).get('time')
        _qrcode = data.get('data', {}).get('qrcode')
        sign = data.get('data', {}).get('sign')
        qr = qrcode.QRCode()
        qr.add_data(_qrcode)
        qr.print_ascii()

        succeed = False
        for i in range(40):
            data = get_qrcode_status(uid, _time, sign)
            time.sleep(3)
            if data.get('code') == 0 and data.get('state') == 1 and data.get('data', {}).get('status') == 2:
                succeed = True
                break

        access_token, refresh_token, expires_in = None, None, None
        if succeed:
            data = device_code_to_token(uid, code_verifier)
            if data.get('code') == 0 and data.get('state') == 1 and data.get('errno') == 0:
                access_token = data.get('data', {}).get('access_token')
                refresh_token = data.get('data', {}).get('refresh_token')
                expires_in = data.get('data', {}).get('expires_in')

    dump_login_info(access_token, refresh_token, expires_in)
    return access_token


def with_authorized(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        access_token, refresh_token, expires_in = load_login_info()
        headers = {
            **(kwargs.get('headers',{})),
            'Authorization': 'Bearer ' + access_token
        }
        kwargs['headers'] = headers
        result = func(*args, **kwargs)
        if str(result.get('code', 40140199)).startswith('401401'):
            access_token = login_oauth_code_pkce()
            headers = {
                **(kwargs.get('headers',{})),
                'Authorization': 'Bearer ' + access_token
            }
            kwargs['headers'] = headers
            result = func(*args, **kwargs)
        return result

    return wrapper
