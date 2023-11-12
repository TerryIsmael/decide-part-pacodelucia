from django.urls import path
from .views import BoothView, BoothYesNoView


urlpatterns = [
    path('<int:voting_id>/', BoothView.as_view()),
    path('yesno/<int:voting_id>/', BoothYesNoView.as_view()),
]
