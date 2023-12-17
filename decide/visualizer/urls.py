from django.urls import path
from .views import VisualizerView,VisualizerBPView,VisualizerYesNoView,stats


urlpatterns = [
    path('<int:voting_id>/', VisualizerView.as_view()),
    path('<int:voting_id>/stats',stats, name='stats'),
    path('bp/<int:voting_id>/', VisualizerBPView.as_view()),
    path('yesno/<int:voting_id>/', VisualizerYesNoView.as_view()),
]
