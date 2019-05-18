from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse

from seat.models import Seat
from studio.models import Studio
from system.views import is_login, is_auth


@is_login
@is_auth
def list(request):
    studios=Studio.objects.all()
    PageObj=Paginator(studios,per_page=5)
    page=request.GET.get('page',1)
    try:
        studiosPageObj=PageObj.page(page)
        studios=studiosPageObj.object_list
    except:
        studios=PageObj.page(1)
    return render(request, 'studio/list.html',context={
        'studios':studios,
        'studiosPageObj':studiosPageObj
    })
@is_login
@is_auth
def add(request):
    if request.POST:
        name=request.POST.get('name',None)
        seat_rows=request.POST.get('seat_rows',None)

        seat_cols=request.POST.get('seat_cols',None)
        print(name,seat_rows,seat_cols)

        studio=Studio(name=name,seat_rows=seat_rows,seat_cols=seat_cols)
        studio.save()

        for i in range(1,int(seat_rows)+1):
            for j in range(1,int(seat_cols)+1):
                seat=Seat(row_id=i,col_id=j,studio=studio)
                seat.save()
        return redirect(reverse('studio_list'))

    return render(request,'studio/add.html')
@is_login
@is_auth
def edit(request,id):
    studio=get_object_or_404(Studio,id=id)
    # print(studio.name)
    # request.data['name']=studio.name
    # request.POST['name']=studio.name


    if request.method=='POST':
        name=request.POST.get('name',None)
        seat_rows=request.POST.get('seat_rows',None)
        seat_cols=request.POST.get('seat_cols',None)
        studio.name=name
        studio.seat_rows=seat_rows
        studio.seat_cols=seat_cols
        studio.save()



    return render(request,'studio/edit.html',context={
        'studio':studio,
    })
@is_login
@is_auth
def delete(request,id):
    studio=get_object_or_404(Studio,id=id)
    studio.delete()
    return redirect(reverse('studio_list'))
def get_data(request):
    if request.is_ajax():
        print('111')
        data = {
            'name': 'jkhj'
        }
        return JsonResponse(data)
    data='失败'
    return JsonResponse(data)