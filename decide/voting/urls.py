from django.urls import path
from . import views
from .views import getVoteStringKeys, getVotingsByUser

urlpatterns = [
    path('', views.VotingView.as_view(), name='voting'),
    path('<int:voting_id>/', views.VotingUpdate.as_view(), name='voting'),
    path('all-questions/', views.AllQuestionsView.as_view(), name='all_questions'),
    path('voting/', views.VotingFrontView.as_view(), name='voting front'),
    path('<int:voting_id>/stringkeys', getVoteStringKeys, name='voting'),
    path('getbyuser', getVotingsByUser),
    path('votingbypreference', views.VotingByPreferenceView.as_view(), name='votingbypreference'),
    path('votingbypreference/<int:voting_id>/', views.VotingByPreferenceUpdate.as_view(), name='votingbypreference'),
    path('votingyesno/', views.VotingYesNoView.as_view(), name='votingyesno'),
    path('votingyesno/<int:voting_id>/', views.VotingYesNoUpdate.as_view(), name='votingyesno'),
]
