from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse

from order.models import Order
from system.views import is_auth, is_login


@is_login
@is_auth
def list(request):
    orders=Order.objects.all()
    order=orders.first()
    print()

    PageObj = Paginator(orders, per_page=5)
    page = request.GET.get('page', 1)
    try:
        ordersPageObj = PageObj.page(page)
        orders = ordersPageObj.object_list
    except:
        orders = PageObj.page(1)
        # playsPageObj=None


    return render(request,'order/list.html',context={
        'orders':orders,
        'ordersPageObj':ordersPageObj,
    })
@is_login
@is_auth
def delete(request,id):
    order=get_object_or_404(Order,id=id)
    order.status=-1
    order.save()

    schedule=order.schedule

    for ticket in order.ticket_set.all():
        ticket.seat.status=False
        ticket.seat.save()
        schedule.ticket_counts+=1
    schedule.save()
    return redirect(reverse('order_list'))




