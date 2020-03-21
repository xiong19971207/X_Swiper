OK = 0


class LogicErr(Exception):
    code = None
    data = None

    def __init__(self, data=None):
        # 等于自己不然就等于类的名字
        self.data = data or self.__class__.__name__


def gen_logic_err(name, code):
    # 封装一个逻辑异常类，也可以用class方法定义
    return type(name, (LogicErr,), {'code': code})


VCODE_ERR = gen_logic_err('VCODE_ERR', code=1000)  # 发送短信异常
SUBCODE_ERR = gen_logic_err('SUBCODE_ERR', code=1001)  # 状态码异常
LoginErr = gen_logic_err('LoginErr', code=1002)  # 用户未登陆
UserFormErr = gen_logic_err('UserFormErr', code=1003)  # 用户表单错误
ProFormErr = gen_logic_err('ProFormErr', code=1004)  # 资料表单错误

StypeErr = gen_logic_err('StypeErr', code=1005)  # 滑动类型错误
ReswipeErr = gen_logic_err('ReswipeErr', code=1006)  # 重复滑动一个人
RewindtimesErr = gen_logic_err('RewindtimesErr', code=1007)  # 反悔次数超过3次
RewindtimeoutErr = gen_logic_err('RewindtimeoutErr', code=1008)  # 反悔时间超过五分钟
