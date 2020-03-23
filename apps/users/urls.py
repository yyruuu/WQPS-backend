from django.urls import path
from . import views
urlpatterns = [
    path('register', views.create_user, name='创建用户'),
    path('login', views.login, name='用户登陆'),
    path('signout', views.sign_out, name='用户登出'),
    path('data', views.get_user_datas, name='获取所有用户数据'),
    path('data/<user_id>', views.get_a_data, name='获取一条用户数据'),
    path('edit', views.edit_data, name="修改用户数据"),
    path('delete/<data_id>', views.delete_data, name="删除用户数据")
]