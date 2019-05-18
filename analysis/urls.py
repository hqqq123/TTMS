from django.urls import path

from analysis.views import sale, play_count, play_money

urlpatterns = [
    path('sale/', sale, name='analisis_sale'),

    path('play_count/', play_count, name='analisis_play_count'),
    path('play_money/', play_money, name='analisis_play_money'),

    # path('edit/<int:id>/', edit, name='play_edit'),
    # path('delete/<int:id>/', delete, name='play_delete'),
    # path('get_data/', get_data, name='get_data'),

]