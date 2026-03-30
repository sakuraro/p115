from p115.utils.log import *
from p115.utils.net import base_request

from p115.auth.controller import with_authorized


HOST = 'https://proapi.115.com'


@with_authorized
def upload_get_token(**kwargs):
    url = HOST + '/open/upload/get_token'

    data = base_request(method='GET', url=url, **kwargs)
    return data


@with_authorized
def upload_init(file_name, file_size, target, file_hash, **kwargs):
    url = HOST + '/open/upload/init'
    files = {
        **(kwargs.get('files',{})),
        'file_name': (None, file_name),
        'file_size': (None, file_size),
        'target': (None, target),
        'fileid': (None, file_hash),
    }
    kwargs['files'] = files

    data = base_request(method='POST', url=url, **kwargs)
    return data


@with_authorized
def ufile_list(**kwargs):
    url = HOST + '/open/ufile/files'
    params = {
        **(kwargs.get('params',{})),
    }
    kwargs['params'] = params

    data = base_request(method='GET', url=url, **kwargs)
    return data


@with_authorized
def fold_get_info_by_path(path, **kwargs):
    url = HOST + '/open/folder/get_info'
    files = {
        **(kwargs.get('files',{})),
        'path': (None, path),
    }
    kwargs['files'] = files

    data = base_request(method='POST', url=url, **kwargs)
    return data


@with_authorized
def fold_get_info_by_fid(file_id, **kwargs):
    url = HOST + '/open/folder/get_info'
    params = {
        **(kwargs.get('params',{})),
        'file_id': file_id,
    }
    kwargs['params'] = params

    data = base_request(method='GET', url=url, **kwargs)
    return data


@with_authorized
def fold_add(pid, file_name, **kwargs):
    url = HOST + '/open/folder/add'
    files = {
        **(kwargs.get('files',{})),
        'pid': (None, pid),
        'file_name': (None, file_name),
    }
    kwargs['files'] = files

    data = base_request(method='POST', url=url, **kwargs)
    return data
