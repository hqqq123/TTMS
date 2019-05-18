from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse

from authority.models import Auth
from system.views import is_login, is_auth


@is_login
@is_auth
def list(request):
    auths=Auth.objects.all()

    PageObj = Paginator(auths, per_page=5)
    page = request.GET.get('page', 1)
    try:
        authsPageObj = PageObj.page(page)
        auths = authsPageObj.object_list
    except:
        auths = PageObj.page(1)
        # playsPageObj=None
    return render(request, 'authority/list.html', context={
        'auths': auths,
        'authsPageObj': authsPageObj
    })
@is_login
@is_auth
def add(request):
    if request.method=='POST':
        name=request.POST['name']
        url=request.POST['url']
        auth=Auth(name=name,url=url)
        auth.save()
        return redirect(reverse('auth_list'))

    return render(request,'authority/add.html')
def edit(request,id):
    auth=get_object_or_404(Auth,id=id)
    if request.method=='POST':
        name = request.POST['name']
        url = request.POST['url']
        if name!=auth.name or url!=auth.url:
            auth.name=name
            auth.url=url
            auth.save()
        return redirect(reverse('auth_list'))
    return render(request,'authority/edit.html',context={
        'auth':auth,
    })
@is_login
@is_auth
def delete(request,id):
    auth=get_object_or_404(Auth,id=id)
    auth.delete()
    return redirect(reverse('auth_list'))

