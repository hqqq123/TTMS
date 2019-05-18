from django.db import models
# Create your models here.
from schedule.models import Schedule
from studio.models import Studio


class Seat(models.Model):
    row_id=models.IntegerField()
    col_id=models.IntegerField()
    status=models.BooleanField(default=False,null=False)
    #如果演出厅删除了，则座位也删除了
    studio=models.ForeignKey(Studio,on_delete=models.CASCADE)












