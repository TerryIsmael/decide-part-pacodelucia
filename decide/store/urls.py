from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.StoreView.as_view(), name='store'),
    path('yesno/', views.StoreYesNoView.as_view(), name='storeYesNo')
]
