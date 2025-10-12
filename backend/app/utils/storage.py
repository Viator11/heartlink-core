import boto3
from botocore.config import Config
from ..core.config import get_settings

_s = get_settings()
_session = boto3.session.Session(
    aws_access_key_id=_s.S3_ACCESS_KEY,
    aws_secret_access_key=_s.S3_SECRET_KEY,
    region_name=_s.S3_REGION or "us-east-1",
)
_s3 = _session.client(
    "s3",
    endpoint_url=_s.S3_ENDPOINT,
    config=Config(s3={"addressing_style": "path" if _s.S3_USE_PATH_STYLE else "auto"}),
)

def put_object(bucket: str, key: str, data: bytes, content_type: str):
    _s3.put_object(Bucket=bucket, Key=key, Body=data, ContentType=content_type, ACL="private")

def get_presigned_url(bucket: str, key: str, method: str="get_object", expires: int=3600) -> str:
    return _s3.generate_presigned_url(
        ClientMethod=method,
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expires
    )
