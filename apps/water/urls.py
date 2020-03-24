from django.urls import path
from . import views
urlpatterns = [
    path('data', views.get_water_data, name='获取水质数据'),
    path('data/<data_id>', views.get_a_data, name='获取一条水质数据'),
    path('edit', views.edit_data, name="修改水质数据"),
    path('delete/<data_id>', views.delete_data, name="删除水质数据"),
    path('add', views.add_data, name="新增水质数据"),
    path('plot', views.plot_data, name="绘制数据趋势")
]