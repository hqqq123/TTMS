from django.urls import path

from ticket.views import sale,seat,buy,search

urlpatterns = [
    path('sale/',sale,name='ticket_sale'),
    path('sale/<int:id>/', sale, name='ticket_sale'),

    path('seat/', seat, name='ticket_seat'),
    path('seat/<int:id>/', seat, name='ticket_seat'),
    path('seat/buy/<int:id>/', buy, name='seat_buy'),
    path('search/', search, name='search'),

    # path('edit/<int:id>/', edit, name='studio_edit'),
    # path('delete/<int:id>/', delete, name='studio_delete'),

]