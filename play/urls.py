from django.urls import path
from play.views import list, add, edit, delete, get_data

urlpatterns = [
    path('list/', list, name='play_list'),
    path('add/', add, name='play_add'),
    path('edit/<int:id>/', edit, name='play_edit'),
    path('delete/<int:id>/', delete, name='play_delete'),
    path('get_data/', get_data, name='get_data'),

]