from django.contrib import admin
from apps.fitness_track.models import (
    CustomUser,
    UserExercise,
    ExerciseHistory,
    Goal,
    UserDetail
)

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(UserDetail)
admin.site.register(UserExercise)
admin.site.register(ExerciseHistory)
admin.site.register(Goal)
