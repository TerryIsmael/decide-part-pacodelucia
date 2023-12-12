from django.urls import path
from . import views


urlpatterns = [
    path('', views.VotingView.as_view(), name='voting'),
    path('<int:voting_id>/', views.VotingUpdate.as_view(), name='voting'),
    path('votingyesno/', views.VotingYesNoView.as_view(), name='votingyesno'),
    path('votingyesno/<int:voting_id>/', views.VotingYesNoUpdate.as_view(), name='votingyesno'),
]
