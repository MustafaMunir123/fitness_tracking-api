from django.urls import path
from apps.fitness_track.views import (
    LoginUserDetailView,
    UserDetailAPIView,
    ExerciseAPIView,
    UserExerciseAPIView,
    UserGoals,
    DashBoardAPIView,
    ExerciseHistoryAPIView
)

urlpatterns = [
    path('login/', LoginUserDetailView.as_view()),
    path('user-details/', UserDetailAPIView.as_view()),
    path('exercises/', ExerciseAPIView.as_view()),
    path('my-exercises/', UserExerciseAPIView.as_view()),
    path('goals/', UserGoals.as_view()),
    path('dashboard/', DashBoardAPIView.as_view()),
    path('exercise/check/', ExerciseHistoryAPIView.as_view())
]
