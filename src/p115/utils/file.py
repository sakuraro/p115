import hashlib
from pathlib import Path

from p115.utils.log import *


def get_name(file_path):
    return Path(file_path).name


def get_size(file_path):
    return Path(file_path).stat().st_size


def calc_hash(file_path, offset=0, size=0):
    size = size if size else get_size(file_path)
    sha1 = hashlib.sha1()
    with open(file_path, 'rb') as f:
        f.seek(offset)
        for i in range(size//4096):
            chunk = f.read(4096)
            sha1.update(chunk)
        chunk = f.read(size%4096)
        sha1.update(chunk)
    return sha1.hexdigest()


def calc_header_hash(file_path):
    return calc_file_hash(file_path, 0, 128*1024)
