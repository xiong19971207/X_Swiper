"""Swiper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import include
from UserApp import apis as user_api

urlpatterns = [

    url(r'^test/', include('UserApp.urls')),

    # 测试
    url(r'^user/testhelloworld/', user_api.testhelloworld),

    # 用户模块
    url(r'^api/user/gen_eamil/', user_api.gen_email),
    url(r'^api/user/submit_vcode/', user_api.submit_vcode),
    url(r'api/user/get_profile/', user_api.get_profile),
    url(r'api/user/set_profile', user_api.set_profile),
    url(r'api/user/upload_avatar', user_api.upload_avatar),
    
    # 社交模块     

]
