from django.urls import path
from order.views import list, delete

urlpatterns = [
    path('list/', list, name='order_list'),
    # path('add/', add, name='play_add'),
    # path('edit/<int:id>/', edit, name='play_edit'),
    path('delete/<int:id>/', delete, name='order_delete'),
    # path('get_data/', get_data, name='get_data'),

]