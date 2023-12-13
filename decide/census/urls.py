from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.CensusCreate.as_view(), name='census_create'),
    path('all-censuss/', views.AllCensus.as_view(), name='all_censuss'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
]
