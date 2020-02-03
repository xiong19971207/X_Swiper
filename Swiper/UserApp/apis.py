from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from UserApp import logics
from UserApp.logics import gen_random_code
from common import stat


def testhelloworld(request):
    return render(request, 'test.html')

def gen_vcode(request):
    '''发送验证码'''
    phonenum = request.GET.get('phonenum')
    status = logics.send_vcode(phonenum)
    if status:
        return JsonResponse({'code': stat.OK, 'data': None})
    else:
        return JsonResponse({'code': stat.VCODE_ERR, 'data': None})

def gen_email(request):
    '''发送email'''

    vcode = gen_random_code()

    subject = '熊氏老方'
    message = '没有用，但必须写'

    email = request.GET.get('email')

    from_email = '17855370672@163.com'
    recipient_list = [email]
    print(recipient_list)

    html_message = '<h1>你的验证码是:</h1>' + vcode
    send_mail(subject=subject, message=message, html_message=html_message, from_email=from_email,
              recipient_list=recipient_list)

    if email:
        return JsonResponse({'code': stat.OK, 'data': None})
    else:
        return JsonResponse({'code': stat.VCODE_ERR, 'data': None})
