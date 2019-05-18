from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse

from account.models import Account
from role.models import Role
from system.views import is_login,is_auth


@is_login
@is_auth
def add(request):
    # form=AccountForm(request.POST)
    roles=Role.objects.all()
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        name=request.POST['name']
        role_id=int(request.POST['role'])
        role=get_object_or_404(Role,id=role_id)
        pwd_make=make_password(password)
        account=Account(email=email,password=pwd_make,name=name,role=role)
        account.save()
        return redirect(reverse('account_list'))
    return render(request,'account/add.html',context={
        'roles':roles
    })
@is_login
@is_auth
def list(request):
    accounts=Account.objects.all()
    pageObj=Paginator(accounts,per_page=5)
    page=request.GET.get('page',1)
    try:
        accountsPageObj=pageObj.page(page)
        accounts=accountsPageObj.object_list
    except:
        accounts=pageObj.page(1)

    return render(request,'account/list.html',context={
        'accounts':accounts,
        'accountsPageObj':accountsPageObj,
    })
@is_login
@is_auth
def edit(request,id):
    account=get_object_or_404(Account,id=id)
    roles=Role.objects.all()
    if request.method=='POST':
        email = request.POST['email']
        name = request.POST['name']
        role_id = int(request.POST['role'])
        role = get_object_or_404(Role, id=role_id)

        if email!=account.email or name!=account.name or role!=account.role:
            account.name=name
            account.email=email
            account.role=role
            account.save()
        return redirect(reverse('account_list'))

    return render(request,'account/edit.html',context={
        'account':account,
        'roles':roles
    })
@is_login
@is_auth
def delete(request,id):
    account=get_object_or_404(Account,id=id)
    account.delete()
    return redirect(reverse('account_list'))
@is_login
def pwd(request):
    id=request.session.get('user_id',None)
    account=get_object_or_404(Account,id=id)
    if request.method=='POST':
        old_pwd=request.POST['old_password']
        if not check_password(old_pwd,account.password):
            messages.info(request,"旧密码错误！")
            return redirect(reverse('account_pwd'))
        else:
            pwd=request.POST['new_password']
            account.password=make_password(pwd)
            account.save()
            return redirect(reverse('account_list'))


    return render(request,'account/pwd.html',context={
        'account':account,
    })

