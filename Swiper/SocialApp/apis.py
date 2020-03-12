from SocialApp import logics
from libs.http import render_json


def rcmd_user(request):
    users = logics.rcmd(request.uid)
    rcmd_date = [user.to_dict() for user in users]
    return render_json(rcmd_date)


def like(request):
    sid = int(request.POST.get('sid'))
    is_matched = logics.like_someone(request.uid, sid)
    return render_json({'is_matched': is_matched})


def superlike(request):
    sid = int(request.POST.get('sid'))
    is_matched = logics.superlike_someone(request.uid, sid)
    return render_json({'is_matched': is_matched})
