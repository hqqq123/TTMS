import datetime
import pytz
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from scipy.stats import moment

from order.models import Order
from play.models import Play
from schedule.models import Schedule
from seat.models import Seat
from studio.models import Studio
from system.views import is_auth, is_login
from ticket.models import Ticket

@is_login
@is_auth
def sale(request,id=2):
    plays=Play.objects.all()

    play=get_object_or_404(Play,id=id)
    schedules=Schedule.objects.filter(play=play).order_by('show_time')
    # print(play.name)
    return render(request,'ticket/sale.html',context={
        'plays':plays,
        'play':play,
        'schedules':schedules,
    })
def seat(request,id):
    schedule=get_object_or_404(Schedule,id=id)
    studio=get_object_or_404(Studio,id=schedule.studio_id)

    seats=Seat.objects.filter(studio=studio).all()
    seats_list=list(seats)
    # print([i.id for i in seats_list],'------------------********')
    # rows = [i for i in range(1, studio.seat_rows + 1)]
    # cols = [i for i in range(1, studio.seat_cols + 1)]
    # print(seats_list)
    seats=[]
    for row in range(studio.seat_rows ):
        seats_row=[]
        for col in range(studio.seat_cols):
            seats_row.append(seats_list[row*studio.seat_cols+col])
        seats.append(seats_row)
    seat=get_object_or_404(Seat,id=id)
    # seat.ticket_set.filter(schedule)
    # print(seats,'--------')
    return render(request,'ticket/seat.html',context={
        'schedule':schedule,
        'seats':seats,
    })
@is_login
def buy(request,id):
    # print(request.path_info.split("/buy/")[0]+"/buy/",type(request.path_info),'------------')

    ids=request.GET['id_str']
    id_li=ids.split(" ")

    schedule=get_object_or_404(Schedule,id=id)
    seats=[get_object_or_404(Seat,id=int(seat_id)) for seat_id in id_li]

    if request.method=='POST':

        with transaction.atomic():
            save_id=transaction.savepoint()

            order=Order()
            money=len(seats)*schedule.ticket_money
            order.money=money
            order.schedule=schedule
            order.save()


            for seat in seats:
                if seat.status:
                    if seat.ticket_set.filter(schedule=schedule):
                        print('=-=---===========================')
                        transaction.savepoint_rollback(save_id)
                        # raise
                        # return JsonResponse({'res':5, 'errmsg':'错误'})
                        messages.info(request,"您选的座位已被购买，请重选！")
                        return redirect(reverse('ticket_seat',args=(schedule.id,)))

                seat.status=True
                seat.save()

                schedule.ticket_counts-=1
                schedule.save()
                # order.save()

                ticket=Ticket(schedule=schedule,seat=seat,order=order)
                ticket.save()
            transaction.savepoint_commit(save_id)



            return render(request,'ticket/ok.html')

    # order_time = (datetime.datetime.now() + datetime.timedelta(minutes=1)).replace(tzinfo=pytz.timezone('UTC'))
    # print(order_time,'-----')
    # request.session['order_time'] = datetime.datetime.now()
    # request.session.set_expiry(60)
    return render(request,'ticket/order.html',context={
        'schedule':schedule,
        'seats':seats,
        'ids':ids,
        # 'order_time':order_time
    })

def search(request):
    name=request.GET['search']
    print(name,'-----------')
    play=Play.objects.filter(name__icontains=name).first()
    plays=Play.objects.all()
    schedules=Schedule.objects.filter(play__name__icontains=name).order_by('show_time')
    return render(request, 'ticket/sale.html', context={
        'plays': plays,
        'play': play,
        'schedules': schedules,
    })


