from django.utils.deprecation import MiddlewareMixin

from common import stat
from libs.http import render_json


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
                raise stat.LogicErr
            else:
                request.uid = uid


class logicErrMiddleware(MiddlewareMixin):
    '''逻辑异常处理中间件'''

    def process_exception(self, request, exception):
        if isinstance(exception, stat.LogicErr):
            return render_json(exception.data, exception.code)
