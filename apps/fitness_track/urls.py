from django.urls import path, include
from apps.fitness_track.views import LoginUserDetailView

urlpatterns = [
    path('login/', LoginUserDetailView.as_view())
]