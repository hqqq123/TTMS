import datetime
from functools import wraps

import pytz
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse

from account.models import Account
from schedule.models import Schedule


def is_login(func):

    @wraps(func)
    def wrapper(request,*args,**kwargs):
        user=request.session.get("user",None)
        if user:
            return func(request,*args,**kwargs)
        else:
            messages.error(request, "用户未登录,请先登录！")

            return redirect(reverse('login'))
    return wrapper

def is_auth(func):

    @wraps(func)
    def wrapper(request,*args,**kwargs):
        # if not request.user.is_authenticated():
        #     return redirect(reverse('login'))

        print('============')
        id=request.session.get('user_id',None)
        print(id)
        try:
            account=get_object_or_404(Account,id=id)
            auths = account.role.auths.all()
            url=request.path_info
            if url.find('/edit/')>=0:
                url=url.split('/edit/')[0]+'/edit/'
            elif url.find('/delete/')>=0:
                url=url.split('/delete/')[0]+'/delete/'
            elif url.find('/sele/')>=0:
                url=url.split('/sale')[0]+'/sale/'
            else:
                url=url

            for auth in auths:
                if auth.url==url:

                    return func(request,*args,**kwargs)
            else:
                messages.info(request,'当前用户没有权限!')
                return redirect(reverse('index'))
        except Exception as e:
            return redirect(reverse('index'))
    return wrapper

def check_schedule(func):
    def wrapper(request,*args,**kwargs):
        studio = request.POST['studio']
        show_time = request.POST['show_time']
        str_showtime = show_time.replace('T', ' ')  # 把时间2019-05-05T13:30格式化为2019-05-05 13:30
        datetime_showtime = datetime.datetime.strptime(str_showtime, "%Y-%m-%d %H:%M") #把字符串转化为datetime时间
        datetime_showtime=datetime_showtime.replace(tzinfo=pytz.timezone('UTC'))
        schedules=Schedule.objects.all()
        for schedule in schedules:
            # print(type(studio),type(schedule.studio.id))
            if int(studio)==schedule.studio.id and datetime_showtime>= schedule.show_time and datetime_showtime<=(schedule.end_time+datetime.timedelta(hours=1)):
                messages.info(request, "演出时间冲突！")
                return redirect(reverse('schedule_add'))
        else:

            return func(request, *args, **kwargs)

            # print(schedule.show_time, schedule.end_time, '**********', datetime_showtime >= schedule.show_time)

            # print(schedule.show_time,schedule.end_time,'============',datetime_showtime>=schedule.show_time)


        # return func(request,*args,**kwargs)

    return wrapper
def login(request):

    if request.method=='POST':
        email=request.POST['email']
        # print(email,'---------------')
        account=Account.objects.filter(email=email).first()
        # print(account.email)
        if account:
            password=request.POST['password']
            if check_password(password,account.password):
                # messages.success()
                request.session['user']=account.email
                request.session['user_id']=account.id
                request.session.set_expiry(60*60)

                return redirect(reverse('play_list'))
            else:
                messages.error(request,"用户名或密码不正确！")
                return redirect(reverse('login'))
        else:
            messages.info(request, "用户不存在！")
            return redirect(reverse('login'))

    return render(request,'system/login.html')
@is_login
def logout(request):
    del request.session['user']
    del request.session['user_id']
    return redirect(reverse('login'))
#
@is_login
def index(request):
    return redirect(reverse('play_list'))


