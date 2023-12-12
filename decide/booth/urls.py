from django.urls import path
from . import views


urlpatterns = [
    path('<int:voting_id>/', views.BoothView.as_view(),name='booth'),
    path('bp/<int:voting_id>/', views.BoothByPreferenceView.as_view()),
    path('<int:voting_id>/', views.BoothView.as_view()),
    path('yesno/<int:voting_id>/', views.BoothYesNoView.as_view()),
]
