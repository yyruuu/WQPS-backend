from django.urls import path
from . import views
urlpatterns = [
    path('register', views.create_user, name='创建用户'),
    path('login', views.login, name='用户登陆'),
    path('signout', views.sign_out, name='用户登出'),
]