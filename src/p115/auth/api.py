from p115.utils.net import base_request


def auth_device_code(app_id, code_challenge, code_challenge_method):
    url = 'https://passportapi.115.com/open/authDeviceCode'
    data = {
        'client_id': app_id,
        'code_challenge': code_challenge,
        'code_challenge_method': code_challenge_method
    }

    data = base_request(method='POST', url=url, data=data)
    return data


def get_qrcode_status(uid, time, sign):
    url = 'https://qrcodeapi.115.com/get/status/'
    params = {
        'uid': uid,
        'time': time,
        'sign': sign
    }

    data = base_request(method='GET', url=url, params=params)
    return data


def device_code_to_token(uid, code_verifier):
    url = 'https://passportapi.115.com/open/deviceCodeToToken'
    data = {
        'uid': uid,
        'code_verifier': code_verifier
    }

    data = base_request(method='POST', url=url, data=data)
    return data


def refresh_access_token(refresh_token):
    url = 'https://passportapi.115.com/open/refreshToken'
    data = {
        'refresh_token': refresh_token
    }

    data = base_request(method='POST', url=url, data=data)
    return data
