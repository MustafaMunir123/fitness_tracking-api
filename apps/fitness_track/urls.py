from django.urls import path, include
from apps.fitness_track.views import (
    LoginUserDetailView,
    UserDetailAPIView,
)

urlpatterns = [
    path('login/', LoginUserDetailView.as_view()),
    path('user-details/', UserDetailAPIView.as_view())
]
