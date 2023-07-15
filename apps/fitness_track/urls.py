from django.urls import path, include
from apps.fitness_track.views import (
    LoginUserDetailView,
    UserDetailsAPIView,
)

urlpatterns = [
    path('login/', LoginUserDetailView.as_view()),
    path('user-details/', UserDetailsAPIView.as_view())
]
