from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('all/', views.get_all_record, name='all'),
    path('order/', views.push_order, name='order'),
    path('path_auto/', views.get_path_auto, name='Path Auto'),
    path('done/', views.order_done, name= 'Done')
]