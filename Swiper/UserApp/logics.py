import random

import requests
from django.core.mail import send_mail

from Swiper import config


def gen_random_code(length=6):
    '''产生指定长度的随机码'''
    return ''.join([str(random.randint(0, 9)) for i in range(length)])


def send_vcode(mobile):
    '''
    发送短信验证码
    '''
    vcode = gen_random_code()

    args = config.YZX_SMS_ARGS.copy()
    args['param'] = vcode
    args['mobile'] = mobile

    response = requests.post(config.YZX_API, json=config.YZX_SMS_ARGS)

    # 检查结果
    if response.status_code == 200:
        result = response.json()
        if result['msg'] == 'OK':
            return True
    return False


def save_avatar(uid, avatar):
    '''本地保存图片'''
    filename = 'avatar-%s' % uid
    filepath = './tmp/%s' % filename
    with open(filepath, 'wb') as fp:
        for chunk in avatar.chunks():
            fp.write(chunk)
    return filepath, filename
