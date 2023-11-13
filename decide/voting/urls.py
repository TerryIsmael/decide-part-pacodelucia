from django.urls import path
from . import views


urlpatterns = [
    path('', views.VotingView.as_view(), name='voting'),
    path('<int:voting_id>/', views.VotingUpdate.as_view(), name='voting'),
    path('all-questions/', views.AllQuestionsView.as_view(), name='all_questions'),
    path('all-auths/', views.AllAuthsAPIView.as_view(), name='all_auths_api')
]