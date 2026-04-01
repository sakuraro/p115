import alibabacloud_oss_v2 as oss
from .crypto import base64_encode


class AliyunOSS:
    def __init__(self, endpoint, access_key_id, access_key_secret, security_token, expiration):
        cfg = oss.config.load_default()
        credentials_provider = oss.credentials.StaticCredentialsProvider(access_key_id, access_key_secret, security_token)
        cfg.credentials_provider = credentials_provider
        cfg.region = 'cn-shenzhen'
        cfg.endpoint = endpoint
        self.client = oss.Client(cfg)


    def upload(self, file_path, bucket, key, callback, callback_var, checkpoint_dir="data/"):
        uploader = self.client.uploader(enable_checkpoint=True, checkpoint_dir=checkpoint_dir)
        result = uploader.upload_file(
            oss.PutObjectRequest(bucket=bucket, key=key, callback=base64_encode(callback), callback_var=base64_encode(callback_var)),
            filepath=file_path
        )
        return result
