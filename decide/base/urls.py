from django.urls import path
from . import views

urlpatterns = [
    path('auth/', views.AllAuthsAPIView.as_view(), name='all_auths_api')
]
