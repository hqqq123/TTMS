from django.urls import path

from authority.views import add,list,edit,delete

urlpatterns = [
    path('list/', list, name='auth_list'),
    path('add/', add, name='auth_add'),
    path('edit/<int:id>/', edit, name='auth_edit'),
    path('delete/<int:id>/', delete, name='auth_delete'),
    # path('get_data/', get_data, name='get_data'),

]