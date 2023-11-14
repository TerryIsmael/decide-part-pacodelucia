from django.urls import path
from . import views


urlpatterns = [
    path('', views.VotingView.as_view(), name='voting'),
    path('<int:voting_id>/', views.VotingUpdate.as_view(), name='voting'),
    path('', views.VotingByPreferenceView.as_view(), name='votingbypreference'),
    path('<int:voting_id>/', views.VotingByPreferenceUpdate.as_view(), name='votingbypreference'),
]
