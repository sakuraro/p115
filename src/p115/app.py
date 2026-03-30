from p115.fs.controller import mkdir_iter, upload_recursive


def main(**kwargs):
    if kwargs['method'] == 'upload':
        local_path = kwargs.get('local_path')
        remote_path = kwargs.get('remote_path')
        pid = mkdir_iter(remote_path)
        upload_recursive(local_path, pid)
