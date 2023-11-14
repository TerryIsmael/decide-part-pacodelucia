from django.urls import path
from .views import VisualizerView, VisualizerYesNoView


urlpatterns = [
    path('<int:voting_id>/', VisualizerView.as_view()),
    path('yesno/<int:voting_id>/', VisualizerYesNoView.as_view()),
]
