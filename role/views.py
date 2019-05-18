from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse

from authority.models import Auth
from role.models import Role
from system.views import is_auth, is_login

@is_login
@is_auth
def list(request):
    roles = Role.objects.all()
    PageObj = Paginator(roles, per_page=5)
    page = request.GET.get('page', 1)
    try:
        rolesPageObj = PageObj.page(page)
        roles = rolesPageObj.object_list
    except:
        roles = PageObj.page(1)
        # rolesPageObj=None
    return render(request, 'role/list.html', context={
        'roles': roles,
        'rolesPageObj': rolesPageObj
    })
@is_login
@is_auth
def add(request):
    auths=Auth.objects.all()
    if request.method=='POST':
        name=request.POST['name']
        auths=request.POST.getlist('auths')
        role=Role(name=name)
        role.save()
        for auth in auths:
            role.auths.add(int(auth))
        # role.auths.save()
        role.save()

        return redirect(reverse('role_list'))
    return render(request,'role/add.html',context={
        'auths':auths
    })
@is_login
@is_auth
def edit(request,id):
    role=get_object_or_404(Role,id=id)
    auths=Auth.objects.all()
    if request.method=='POST':
        name=request.POST['name']
        auths_list =[str(auth.id) for auth in role.auths.all()]
        auths=request.POST.getlist('auths')


        if name!=role.name:
            role.name=name
            role.save()
        if auths!=auths_list:
            role.auths.clear()
            for auth in auths:
                role.auths.add(int(auth))
            role.save()
        return redirect(reverse('role_list'))


    return render(request,'role/edit.html',context={
        'role':role,
        'auths':auths,
    })
@is_login
@is_auth
def delete(request,id):

    role=get_object_or_404(Role,id=id)
    role.delete()
    return redirect(reverse('role_list'))
