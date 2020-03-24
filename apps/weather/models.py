from django.db import models
from datetime import datetime
# Create your models here.


class WeatherData(models.Model):
    """
    气象数据
    """
    T = models.FloatField(verbose_name="温度")
    Po = models.FloatField(verbose_name="气象站水平大气压")
    P = models.FloatField(verbose_name="平均大气压")
    U = models.FloatField(verbose_name="湿度-N")
    Ff = models.FloatField(verbose_name="风速")
    VV = models.FloatField(verbose_name="水平能见度")
    Td = models.FloatField(verbose_name="露点温度")
    RRR = models.FloatField(verbose_name="降水量")
    time = models.DateTimeField(default=datetime.now, verbose_name="日期")

    class Meta:
        verbose_name = "气象数据"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.time
