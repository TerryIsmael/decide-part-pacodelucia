from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.CensusCreate.as_view(), name='census_create'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
    path("censuspreference/",views.CensusPreferenceCreate.as_view(),
    name="census_preference_create",),
    path(
        "censuspreference/<int:voting_preference_id>/",
        views.CensusPreferenceDetail.as_view(),
        name="census_preference_detail",
    ),
    path("censusyesno/",views.CensusYesNoCreate.as_view(),
    name="census_yesno_create",),
    path(
        "censusyesno/<int:voting_yesno_id>/",
        views.CensusYesNoDetail.as_view(),
        name="census_yesno_detail",
    ),
]
