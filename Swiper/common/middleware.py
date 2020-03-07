from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from common import stat


class AuthMiddleware(MiddlewareMixin):
    '''用户登陆中间件'''
    path_white_list = [
        # 测试
        '/user/testhelloworld/',
        '/test/test2/',
        
        '/api/user/gen_eamil/',
        '/api/user/submit_vcode/',
    ]

    def process_request(self, request):
        if request.path not in self.path_white_list:
            uid = request.session.get('uid')
            if not uid:
                return JsonResponse({'code': stat.LoginErr, 'data': None})
            else:
                request.uid = uid
