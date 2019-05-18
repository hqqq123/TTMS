import datetime

import pytz
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse
from pytz import utc

from play.models import Play
from schedule.models import Schedule
from studio.models import Studio
from system.views import check_schedule, is_auth, is_login


@is_login
@is_auth
def list(request):
    schedules=Schedule.objects.all()
    PageObj = Paginator(schedules, per_page=5)
    page = request.GET.get('page', 1)
    try:
        schedulesPageObj = PageObj.page(page)
        schedules = schedulesPageObj.object_list
    except:
        schedules = PageObj.page(1)
        # playsPageObj=None
    return render(request, 'schedule/list.html', context={
        'schedules': schedules,
        'schedulesPageObj': schedulesPageObj
    })

@check_schedule
def add_schedule(request):
    play = request.POST['play']
    studio = request.POST['studio']
    show_time = request.POST['show_time']

    ticket_money = request.POST['money']

    str_showtime = show_time.replace('T', ' ')  # 把时间2019-05-05T13:30格式化为2019-05-05 13:30
    datetime_showtime = datetime.datetime.strptime(str_showtime, "%Y-%m-%d %H:%M")  # 把字符串转化为datetime时间，因为下面要进行加法计算

    play_obj = get_object_or_404(Play, id=play)

    datetime_endtime = datetime_showtime + datetime.timedelta(minutes=play_obj.length)
    end_time = datetime_endtime.strftime("%Y-%m-%dT%H:%M")  # datetime时间转化为字符串时间

    studio_obj = get_object_or_404(Studio, id=studio)
    ticket_counts = studio_obj.seat_rows * studio_obj.seat_cols
    ticket_all_counts = studio_obj.seat_rows * studio_obj.seat_cols

    # print(play, studio, show_time, ticket_money, ticket_counts, '---------------')

    schedule = Schedule(play=play_obj, studio=studio_obj, show_time=show_time, end_time=end_time,
                        ticket_counts=ticket_counts, ticket_money=float(ticket_money),
                        ticket_all_counts=ticket_all_counts)

    schedule.save()
    return redirect(reverse('schedule_list'))
@is_login
@is_auth
def add(request):
    plays=Play.objects.all()
    studios=Studio.objects.all()
    if request.method=='POST':
        return add_schedule(request)

    return render(request,'schedule/add.html',context={
        'plays':plays,
        'studios':studios
    })
@check_schedule
def edit_schedule(request,schedule):
    play = request.POST['play']
    studio = request.POST['studio']
    show_time = request.POST['show_time']

    ticket_money = request.POST['money']

    if int(play) != schedule.play.id:
        schedule.play_id = play
    if int(studio) != schedule.studio_id:
        schedule.studio_id = studio
    if float(ticket_money) != schedule.ticket_money:
        schedule.ticket_money = ticket_money

    if show_time != schedule.show_time.strftime("%Y-%m-%dT%H:%M"):
        schedule.show_time = show_time

        str_showtime = show_time.replace('T', ' ')  # 把时间2019-05-05T13:30格式化为2019-05-05 13:30
        datetime_showtime = datetime.datetime.strptime(str_showtime, "%Y-%m-%d %H:%M")  # 把字符串转化为datetime时间，因为下面要进行加法计算
        # play_obj = get_object_or_404(Play, id=pla

        datetime_endtime = datetime_showtime + datetime.timedelta(minutes=schedule.play.length)
        end_time = datetime_endtime.strftime("%Y-%m-%dT%H:%M")  # 达特提么时间转化为字符串时间

        schedule.end_time = end_time
    schedule.save()
    return redirect(reverse('schedule_list'))
@is_login
@is_auth
def edit(request,id):
    schedule=get_object_or_404(Schedule,id=id)
    plays=Play.objects.all()
    studios=Studio.objects.all()
    if request.method=='POST':
        return edit_schedule(request,schedule)

    return render(request,'schedule/edit.html',context={
        'schedule':schedule,
        'plays':plays,
        'studios':studios
    })
@is_login
@is_auth
def delete(request,id):
    schedule=get_object_or_404(Schedule,id=id)
    schedule.delete()
    messages.info(request,'电影%s的演出计划已删除' %(schedule.play.name))
    return redirect(reverse('schedule_list'))

# https://templatemag.com/demo/templates/Dashio/advanced_form_components.html