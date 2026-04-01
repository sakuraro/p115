from pathlib import Path

from p115.utils.log import log_info, log_error, log_caller
from p115.utils.file import get_name, get_size, calc_hash, calc_header_hash
from .api import ufile_list, fold_get_info_by_path, fold_add, upload_init, upload_get_token


@log_caller
def ls(pid, **kwargs):
    data = ufile_list(params={'cid': pid, 'cur': 1, 'show_dir': 1, 'offset': 0, 'limit': 100})
    ufiles = []
    if data.get('code') == 0 and data.get('state') == True:
        count = data.get('count', 0)
        if count != 0:
            ufiles += data.get('data', [])
            for i in range((count - 1) // 100):
                data = ufile_list(params={'cid': pid, 'cur': 1, 'show_dir': 1, 'offset': i*100+100, 'limit': 100})
                if data.get('code') == 0 and data.get('state') == True:
                    ufiles += data.get('data', [])

    return ufiles


@log_caller
def existed(remote_path, **kwargs):
    try:
        data = fold_get_info_by_path(remote_path)
        # fold or file dosen't exist remotely
        if not (data.get('code') == 0 and data.get('state') == True and data.get('data') != []):
            raise ValueError(f'{data}')
        ufile_id = data.get('data', {}).get('file_id')
    except Exception as e:
        ufile_id = None

    return ufile_id


@log_caller
def mkdir(pid, name, **kwargs):
    ufile_id = None
    data = fold_add(pid, file_name=name, **kwargs)
    if data.get('code') == 0 and data.get('state') == True:
        ufile_id = data.get('data', {}).get('file_id')
    # 目录已存在
    elif data.get('code') == 20004 and data.get('state') == False:
        ufiles = ls(pid)
        for ufile in ufiles:
            if ufile.get('fc') == '0' and ufile.get('fn') == name:
                ufile_id = ufile.get('fid')

    return ufile_id


@log_caller
def mkdir_iter(remote_path, **kwargs):
    if Path(remote_path) == Path('/'):
        return '0'

    ufile_id = existed(remote_path)
    if not ufile_id:
        pid = mkdir_iter(str(Path(remote_path).parent))
        ufile_id = mkdir(pid, str(Path(remote_path).name))

    return ufile_id


@log_caller
def upload_file(local_file, pid, **kwargs):
    try:
        if not pid:
            raise ValueError(f'upload_file params: {local_file} {pid}')
        target = 'U_1_' + pid
        file_name = get_name(local_file)
        file_size = get_size(local_file)
        file_hash = calc_hash(local_file)

        data = upload_init(file_name, file_size, target, file_hash)
        if not (data.get('code') == 0 and data.get('state') == True and data.get('data') != []):
            raise ValueError(f'{data}')
        # if need to perform 2-step verification
        if data.get('data', {}).get('code') == 701 and data.get('data', {}).get('status') == 7:
            sign_key = data.get('data',{}).get('sign_key')
            start, stop = data.get('data',{}).get('sign_check','0-0').split('-')
            sign_val = calc_hash(local_file, int(start), int(stop)-int(start)+1).upper()

            data = upload_init(
                file_name, file_size, target, file_hash, files={'sign_key':(None,sign_key),'sign_val':(None,sign_val)}
            )
            if not (data.get('code') == 0 and data.get('state') == True and data.get('data') != []):
                raise ValueError(f'{data}')
        # if can't rapid upload
        if data.get('data', {}).get('status') == 1:
            log_info(f'无法秒传 {file_name}')
            data = upload_get_token()
            if not (data.get('code') == 0 and data.get('state') == True and data.get('data') != []):
                raise ValueError(f'{data}')
            endpoint = data.get('data', {}).get('endpoint')
            access_key_id = data.get('data', {}).get('AccessKeyId')
            access_key_secret = data.get('data', {}).get('AccessKeySecret')
            security_token = data.get('data', {}).get('SecurityToken')
            expiration = data.get('data', {}).get('Expiration')
            # TODO: 上传oss
        # if can rapid upload
        elif data.get('data', {}).get('status') == 2:
            log_info(f'成功秒传 {file_name}')
        else:
            raise ValueError(f'{data}')
    except Exception as e:
        log_error(e)


@log_caller
def upload_file_iter(local_file, remote_path, **kwargs):
    remote_file = Path(remote_path) / Path(local_file).name

    ufile_id = existed(remote_path)
    if ufile_id:
        ufile_id = data.get('data', {}).get('file_id')
    else:
        pid = mkdir_iter(remote_path)
        ufile_id = upload_file(local_file, pid)

    return ufile_id


@log_caller
def upload_recursive(local_path, pid, **kwargs):
    try:
        p = Path(local_path)
        # if path doesn't exist locally or pid is None
        if not p.exists() or not pid:
            raise ValueError(f'upload_recursive params: {local_path} {pid}')
        # if path points to folder locally
        elif p.is_dir():
            ufile_id = mkdir(pid, p.name)
            ufiles = ls(ufile_id)
            for lpath in p.iterdir():
                # except the file in the folder exist remotely
                if not (lpath.is_file() and [ufile for ufile in ufiles if ufile.get('fc') == '1' and ufile.get('sha1') == calc_hash(str(lpath))] != []):
                    upload_recursive(str(lpath), ufile_id)
        # if path points to file locally
        elif p.is_file():
            ufile_id = upload_file(local_path, pid)
    except Exception as e:
        ufile_id = None
        log_error(e)

    return ufile_id
