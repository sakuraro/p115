import random
from base64 import urlsafe_b64encode
from hashlib import sha256
from string import ascii_letters, digits

from p115.utils import log


def gen_code_verifier_and_challenge():
    # use a cryptographically strong random number generator source
    rand = random.SystemRandom()

    code_verifier = ''.join(rand.choices(ascii_letters + digits, k=128))
    code_verifier_hash = sha256(code_verifier.encode()).digest()
    code_challenge = urlsafe_b64encode(code_verifier_hash).decode().rstrip('=')

    log.log_debug(f'code_challenge: {code_challenge}, code_verifier: {code_verifier}')

    return code_challenge, code_verifier
