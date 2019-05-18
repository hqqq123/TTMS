from django.db import models

# Create your models here.
from django.utils import timezone

from schedule.models import Schedule
from seat.models import Seat


class Order(models.Model):
    time=models.DateTimeField(default=timezone.now)
    money=models.FloatField()
    # seats=models.ManyToManyField(Seat)
    schedule=models.ForeignKey(Schedule,on_delete=models.SET_NULL,null=True)
    # tickets=models.ForeignKey(Ticket,on_delete=models.SET_NULL,null=True)
    status=models.IntegerField(default=1)#-1已退 0已完成 1未完成