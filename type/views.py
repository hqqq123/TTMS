from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse

from system.views import is_auth, is_login
from type.models import Type

@is_login
@is_auth
def list(request):
    types=Type.objects.all()
    PageObj=Paginator(types,per_page=5)
    page=request.GET.get('page',1)
    try:
        typesPageObj=PageObj.page(page)
        types=typesPageObj.object_list
    except:
        typesPageObj=PageObj.page(1)
        types=typesPageObj.object_list


        # typesPageObj=None
    return render(request, 'type/list.html',context={
        'types':types,
        'typesPageObj':typesPageObj
    })
@is_login
@is_auth
def add(request):
    if request.method=='POST':
        name=request.POST['name']
        type=Type(name=name)
        type.save()
        return redirect(reverse('type_list'))
    return render(request,'type/add.html')
@is_login
@is_auth
def edit(request,id):
    type = get_object_or_404(Type, id=id)

    if request.method == 'POST':
        name = request.POST.get('name', None)
        type.name = name
        type.save()
        return redirect(reverse('type_list'))

    return render(request, 'type/edit.html', context={
        'type': type
    })
@is_login
@is_auth
def delete(request,id):
    type=get_object_or_404(Type,id=id)
    type.delete()
    return redirect(reverse('type_list'))