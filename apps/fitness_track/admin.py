from django.contrib import admin
from apps.fitness_track.models import (
    CustomUser,
    UserExercise,
    ExerciseHistory,
    Goal,
    UserDetails
)

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(UserDetails)
admin.site.register(UserExercise)
admin.site.register(ExerciseHistory)
admin.site.register(Goal)
