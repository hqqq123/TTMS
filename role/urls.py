from django.urls import path
from role.views import list, add, edit, delete

urlpatterns = [
    path('list/', list, name='role_list'),
    path('add/', add, name='role_add'),
    path('edit/<int:id>/', edit, name='role_edit'),
    path('delete/<int:id>/', delete, name='role_delete'),
    # path('get_data/', get_data, name='get_data'),

]