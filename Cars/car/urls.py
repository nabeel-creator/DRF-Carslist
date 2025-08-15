from django.urls import path
from . import views

urlpatterns=[
    path('list', views.list_cars, name='list_cars'),
    path('id/<int:car_id>/', views.get_car, name='get_car'),
]