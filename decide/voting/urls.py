from django.urls import path
from . import views
from .views import getVoteStringKeys


urlpatterns = [
    path('', views.VotingView.as_view(), name='voting'),
    path('<int:voting_id>/', views.VotingUpdate.as_view(), name='voting'),
    path('<int:voting_id>/stringkeys', getVoteStringKeys, name='voting'),
]
