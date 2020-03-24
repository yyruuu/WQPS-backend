from django.urls import path
from . import views
urlpatterns = [
    path('data', views.get_weather_data, name='获取气象数据'),
    path('data/<data_id>', views.get_a_data, name='获取一条气象数据'),
    path('edit', views.edit_data, name="修改气象数据"),
    path('delete/<data_id>', views.delete_data, name="删除气象数据"),
    path('add', views.add_data, name="新增气象数据"),
    path('plot', views.plot_data, name="绘制数据趋势")
]