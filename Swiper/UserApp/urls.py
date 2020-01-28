from django.conf.urls import url

from UserApp import apis

urlpatterns = [
    url(r'^test2/',apis.testhelloworld),
]
