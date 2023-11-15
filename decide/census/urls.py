from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.CensusCreate.as_view(), name='census_create'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
    path('import/', views.CensusImport.as_view(), name='census import'),
    path('import/ldap/', views.CensusImportLDAP.as_view(), name='census import ldap'),
    path('export/<int:voting_id>', views.CensusExport.as_view(), name="census export"),
    path('export/', views.CensusExport.as_view(), name="census export")
]
