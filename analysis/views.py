import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from order.models import Order
from system.views import is_login, is_auth


@is_login
@is_auth
def sale(request):

    return render(request,'analyse/sale.html')

def play_count(request):
    data={}
    orders=Order.objects.filter(status=1)[1:]
    print(orders)
    for order in orders:
        play=order.schedule.play.name
        count=order.ticket_set.count()
        data[play]=data.get(play,0)+count
    plays=[]
    counts=[]

    for play in data:
        plays.append(play)
        counts.append(data[play])
    print(plays,counts)
    data={
        'plays':plays,
        'counts':counts
    }
    return JsonResponse(data)
def play_money(request):
    data={}
    orders=Order.objects.filter(status=1)[1:]
    print(orders)
    for order in orders:
        schedule=order.schedule
        play=schedule.play.name
        count=order.ticket_set.count()
        money=schedule.ticket_money
        data[play]=data.get(play,0)+count*money
    res=[]
    for play in data:
        res.append({"value":data[play],"name":play})
    res={'info':res}
    print(res['info'])
    return JsonResponse(res)