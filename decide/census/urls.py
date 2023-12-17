from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.CensusCreate.as_view(), name='census_create'),
    path('front/', views.CensusFront.as_view(), name='all_censuss'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
    path('import/', views.CensusImport.as_view(), name='census import'),
    path('import/ldap/', views.CensusImportLDAP.as_view(), name='census import ldap'),
    path('export/<int:voting_id>', views.CensusExport.as_view(), name="census export"),
    path('export/', views.CensusExport.as_view(), name="census export")
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
    path('user-details/',views.UserDataCreate.as_view(),name='user_details_create'),
    path('get-filtered-census',views.CensusFilter.as_view(),name='census_filter'),
    path('census-reuse', views.CensusReuse.as_view(), name='census_reuse'),
]
