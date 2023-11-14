from django.urls import path
from .views import VisualizerView, stats


urlpatterns = [
    path('<int:voting_id>/', VisualizerView.as_view()),
    path('<int:voting_id>/stats',stats)
]
