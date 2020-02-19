from qiniu import Auth, put_file

# 构建鉴权对象
from Swiper import config


def upload_to_qn(filename, filepath):
    q = Auth(config.QN_access_key, config.QN_secret_key)

    # 要上传的空间
    bucket_name = config.Bucket_Name

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, filename, 3600)

    put_file(token, filename, filepath)
    avatar_url = '%s/%s' % (config.qn_url, filename)
    return avatar_url
