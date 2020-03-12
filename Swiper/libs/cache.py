from redis import Redis

from Swiper.config import REDIS


rds = Redis(**REDIS)