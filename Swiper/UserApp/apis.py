from django.core.cache import cache
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from UserApp import logics
from UserApp.logics import gen_random_code
from UserApp.models import User
from common import stat


def testhelloworld(request):
    return render(request, 'test.html')


def gen_vcode(request):
    '''
    发送验证码
    此处用不上,OK
    '''
    phonenum = request.GET.get('phonenum')
    status = logics.send_vcode(phonenum)
    if status:
        return JsonResponse({'code': stat.OK, 'data': None})
    else:
        return JsonResponse({'code': stat.VCODE_ERR, 'data': None})


def gen_email(request):
    '''发送email'''

    vcode = gen_random_code()
    print(vcode)

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
        cache.set('vcode-%s' % email, vcode, 180)
        return JsonResponse({'code': stat.OK, 'data': None})
    else:
        return JsonResponse({'code': stat.VCODE_ERR, 'data': None})


def submit_vcode(request):
    vcode = request.POST.get('vcode')
    email = request.POST.get('email')
    ck_vcode = cache.get('vcode-%s' % email)
    print(ck_vcode)

    if vcode and ck_vcode == vcode:
        try:
            user = User.objects.get(phonenum=email)
        except User.DoesNotExist:
            user = User.objects.create(phonenum=email)
        request.session['uid'] = user.id
        return JsonResponse({'code': stat.OK, 'data': user.to_dict()})
    else:
        return JsonResponse({'code': stat.VCODE_ERR, 'data': None})


def get_profile(request):
    user = User.objects.get(id=request.uid)
    return JsonResponse(user.profile.to_dict())
