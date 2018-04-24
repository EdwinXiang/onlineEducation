"""onlineEducation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path,include,re_path
from apps.users.views import LoginView,RegisterView,ActiveUserView,ForgetPwdView,ModifyPwdView
from apps.organization.views import OrgView
from django.views.static import serve
from onlineEducation.settings import MEDIA_ROOT
import xadmin
xadmin.autodiscover()

# version模块自动注册需要版本控制的 Model
from xadmin.plugins import xversion
xversion.register_models()

urlpatterns = [
    path('xadmin/', xadmin.site.urls), # 后台管理地址
    path('', TemplateView.as_view(template_name='index.html'),name='index'), # 首页地址
    path('login/', LoginView.as_view(), name = 'login'), # 登录地址
    path('register/', RegisterView.as_view(), name='register'), # 注册地址
    path('captcha/', include('captcha.urls')), # 验证码地址
    path('active/(?P<active_code>.*)/', ActiveUserView.as_view(), name='user_active'),
    re_path('reset/(?P<active_code>.*)/', ForgetPwdView.as_view(), name='reset_pwd'),
    path('modify_pwd/', ModifyPwdView.as_view(), name='modify_pwd'),
    # 机构列表相关接口
    path('org_list/', OrgView.as_view(), name = 'org_list'),
    re_path(r'^media/(?P<path>.*)',serve, {'document_root':MEDIA_ROOT})
]
