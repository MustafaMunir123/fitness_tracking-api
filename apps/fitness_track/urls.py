from django.urls import path, include
from apps.fitness_track.views import (
    LoginUserDetailView,
    UserDetailAPIView,
    ExerciseAPIView,
    UserExerciseAPIView
)

urlpatterns = [
    path('login/', LoginUserDetailView.as_view()),
    path('user-details/', UserDetailAPIView.as_view()),
    path('exercises/', ExerciseAPIView.as_view()),
    path('my-exercises/', UserExerciseAPIView.as_view())
]
