from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('showrooms', views.showroom_view, basename='showroom')

urlpatterns=[
    path('list', views.list_cars, name='list_cars'),
    path('id/<int:car_id>/', views.get_car, name='get_car'),
    path('', include(router.urls)),
    # path('showrooms/', views.showroomList.as_view(), name='showroom_list'),
    # path('showrooms/<int:pk>/', views.showroom_details.as_view(), name='showroom_details'),
    # path('reviews/', views.ReviewList.as_view(), name='review_list'),
    # path('reviews/<int:pk>/', views.ReviewDetail.as_view(), name='review_detail'),
    path('showroom/<int:showroom_pk>/reviews/', views.ReviewList.as_view(), name='car_review_list'),
    path('showroom/<int:showroom_pk>/reviews-create/', views.ReviewCreate.as_view(), name='car_review_create'),
    path('showroom/reviews/<int:pk>/', views.ReviewDetail.as_view(), name='car_review_detail')
]