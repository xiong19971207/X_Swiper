from redis import Redis as _Redis
from pickle import dumps, loads, HIGHEST_PROTOCOL, UnpicklingError

from Swiper.config import REDIS


class Redis(_Redis):
    # 让Redis的set方法能序列化，能放入列表
    def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        pickle_value = dumps(value, HIGHEST_PROTOCOL)
        return super().set(name, pickle_value, ex, px, nx, xx)

    # 让get返回列表
    def get(self, name, default=None):
        pickle_value = super().get(name)
        if not pickle_value:
            return default
        else:
            try:
                print('===============================')
                print(loads(pickle_value))
                return loads(pickle_value)
            except UnpicklingError:
                return pickle_value


rds = Redis(**REDIS)
