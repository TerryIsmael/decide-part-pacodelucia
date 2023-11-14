from django.urls import path
from .views import VisualizerView,VisualizerBPView


urlpatterns = [
    path('<int:voting_id>/', VisualizerView.as_view()),
    path('bp/<int:voting_id>/', VisualizerBPView.as_view())
]
