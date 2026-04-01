import random
from base64 import urlsafe_b64encode, b64encode
from hashlib import sha256
from string import ascii_letters, digits

from .log import log_debug


def gen_code_verifier_and_challenge():
    # use a cryptographically strong random number generator source
    rand = random.SystemRandom()

    code_verifier = ''.join(rand.choices(ascii_letters + digits, k=128))
    code_verifier_hash = sha256(code_verifier.encode()).digest()
    code_challenge = urlsafe_b64encode(code_verifier_hash).decode().rstrip('=')

    log_debug(f'code_challenge: {code_challenge}, code_verifier: {code_verifier}')

    return code_challenge, code_verifier


def base64_encode(s: str):
    result = b64encode(s.encode('utf-8')).decode('utf-8')
    return result
