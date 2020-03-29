from django.urls import path
from . import views
urlpatterns = [
    path('train', views.train, name='训练模型'),
]