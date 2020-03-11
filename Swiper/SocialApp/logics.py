import datetime

from SocialApp.models import Swiped, Friend
from UserApp.models import Profile, User


def rcmd(uid):
    profile, _ = Profile.objects.get_or_create(id=uid)

    today = datetime.datetime.today()

    earliest_birthday = today - datetime.timedelta(profile.max_dating_age * 365)
    latest_birthday = today - datetime.timedelta(profile.min_dating_age * 365)

    users = User.objects.filter(
        gender=profile.dating_gender,
        location=profile.dating_location,
        birthday__gte=earliest_birthday,
        birthday__lte=latest_birthday
    )[:10]

    return users


def like_someone(uid, sid):
    # 添加滑动记录
    Swiped.objects.create(uid=uid, sid=sid)
    # 查看对方有没有喜欢或超级喜欢我
    if Swiped.is_liked(sid, uid):
        Friend.make_friends(uid, sid)
        return True
    else:
        return False
