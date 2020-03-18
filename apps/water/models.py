from django.db import models
from datetime import datetime
# Create your models here.


class WaterData(models.Model):
    """
    水质数据
    """
    PH = models.FloatField(verbose_name="ph值")
    DO = models.FloatField(verbose_name="溶解氧")
    CODMn = models.FloatField(verbose_name="CODMn")
    NH3_N = models.FloatField(verbose_name="NH2-N")
    time = models.DateTimeField(default=datetime.now, verbose_name="日期")

    class Meta:
        verbose_name = "水质数据"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.time
