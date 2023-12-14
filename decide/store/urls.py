from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.StoreView.as_view(), name='store'),
    path('front/', views.StoreFrontView.as_view(), name='store-front'),
]
