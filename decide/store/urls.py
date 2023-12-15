from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.StoreView.as_view(), name='store'),
    path('bp/', views.StoreByPreferenceView.as_view(), name='storebypreference'),
    path('yesno/', views.StoreYesNoView.as_view(), name='storeYesNo')

]
