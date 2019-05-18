import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse

from play.models import Play
from system.views import is_login, is_auth
from type.models import Type

@is_login
def list(request):
    plays = Play.objects.all().order_by("play_time")
    PageObj = Paginator(plays, per_page=5)
    page = request.GET.get('page', 1)
    try:
        playsPageObj = PageObj.page(page)
        plays = playsPageObj.object_list
    except:
        playsPageObj = PageObj.page(1)
        plays=playsPageObj.object_list
        # playsPageObj=None
    return render(request, 'play/list.html', context={
        'plays': plays,
        'playsPageObj': playsPageObj
    })
#
@is_login
@is_auth
def add(request):
    types=Type.objects.all()

    if request.method=='POST':
        name=request.POST['name']
        play_time=request.POST['play_time']
        length=request.POST['length']
        director=request.POST['director']
        actors=request.POST['actors']
        area=request.POST['area']
        types=request.POST.getlist('types')
        desc=request.POST['desc']
        play=Play(name=name,play_time=play_time,length=length,director=director,actors=actors,area=area,desc=desc)
        # play.types.create

        play.save()


        for type in types:


            play.types.add(int(type))
        play.save()

        return redirect(reverse('play_list'))
    return render(request,'play/add.html',context={
        'types':types
    })
@is_login
@is_auth
def delete(request,id):
    play=get_object_or_404(Play,id=id)
    play.delete()

    return redirect(reverse('play_list'))
@is_login
@is_auth
def edit(request,id):
    play=get_object_or_404(Play,id=id)

    types=Type.objects.all()
    if request.method=='POST':
        play.name = request.POST['name']
        play.play_time = request.POST['play_time']
        play.length = request.POST['length']
        play.director = request.POST['director']
        play.actors = request.POST['actors']
        play.area = request.POST['area']
        types = request.POST.getlist('types')
        play.desc = request.POST['desc']

        # play.update(name=name,play_time=play_time,length=length,director=director,actors=actors,area=area,desc=desc)
        play.save()
        play.types.clear()
        for type in types:
            play.types.add(int(type))
        play.save()

        return redirect(reverse('play_list'))


    return render(request,'play/edit.html',context={
        'play':play,
        'types':types
    })

def get_data(request):
    data = {
        'name': 'jkhj'
    }
    if request.is_ajax():
        print('111')

        return JsonResponse(data)
    return JsonResponse(data)