from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.fitness_track.constants import EXERCISE_GOALS

# Create your models here.


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=13)
    complete_details = models.BooleanField(default=True, blank=True)


class UserDetail(models.Model):
    """
    user personal info
    """
    height = models.FloatField(null=False, blank=True)
    weight = models.FloatField(null=False, blank=True)
    sleep = models.FloatField(null=False, blank=True)
    walk = models.FloatField(null=True, blank=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="user_detail")


class UserExercise(models.Model):
    exercise_name = models.CharField(max_length=50, null=False, blank=True)
    burn_calories = models.PositiveIntegerField(null=False, blank=True)
    sets = models.PositiveIntegerField(default=3, null=True, blank=False)
    reps = models.PositiveIntegerField(default=3, null=True, blank=False)
    last_attempted = models.DateField(editable=True, null=True, blank=True)
    done = models.BooleanField(default=False, blank=False, null=True)
    focus = models.CharField(max_length=50, null=False, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_exercise")


class ExerciseHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='exercise_history')
    exercise = models.ForeignKey(UserExercise, on_delete=models.CASCADE, related_name='exercise_history')
    date = models.DateField(auto_now=True)


class Goal(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='goal')
    category = models.CharField(choices=EXERCISE_GOALS, null=False, blank=True, max_length=50)


