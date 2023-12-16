from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.CensusCreate.as_view(), name='census_create'),
    path('front/', views.CensusFront.as_view(), name='all_censuss'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
    path('user-details/',views.UserDataCreate.as_view(),name='user_details_create'),
    path('get-filtered-census',views.CensusFilter.as_view(),name='census_filter')
]
