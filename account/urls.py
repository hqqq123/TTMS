from django.urls import path

from account.views import add, list, edit, delete, pwd

urlpatterns = [
    path('list/', list, name='account_list'),
    path('add/', add, name='account_add'),
    path('edit/<int:id>/', edit, name='account_edit'),
    path('delete/<int:id>/', delete, name='account_delete'),
    path('pwd/', pwd, name='account_pwd'),

]