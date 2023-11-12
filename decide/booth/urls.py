from django.urls import path
from .views import BoothView, BoothByPreferenceView


urlpatterns = [
    path('<int:voting_id>/', BoothView.as_view()),
    path('bp/<int:voting_by_preference_id>/', BoothByPreferenceView.as_view()),
]
