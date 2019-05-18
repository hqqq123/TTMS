from django.urls import path

from schedule.views import list, add, edit, delete

urlpatterns = [
    path('list/',list,name='schedule_list'),
    path('add/', add, name='schedule_add'),
    path('edit/<int:id>/', edit, name='schedule_edit'),
    path('delete/<int:id>/', delete, name='schedule_delete'),

]