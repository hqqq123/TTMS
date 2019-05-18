from django.db import models

# Create your models here.
from order.models import Order
from play.models import Play
from schedule.models import Schedule
from seat.models import Seat
from studio.models import Studio


class Ticket(models.Model):
    #用户
    # play=models.ForeignKey(Play,on_delete=models.SET_NULL,null=True)
    # studio=models.ForeignKey(Studio,on_delete=models.SET_NULL,null=True)
    schedule=models.ForeignKey(Schedule,on_delete=models.SET_NULL,null=True)
    seat=models.ForeignKey(Seat,on_delete=models.SET_NULL,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    # status=models.IntegerField()#-1 已完成




    # money=models.FloatField()
