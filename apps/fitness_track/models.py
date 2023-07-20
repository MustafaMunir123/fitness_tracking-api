import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.fitness_track.constants import EXERCISE_GOALS

# Create your models here.


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=13)
    complete_details = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.username}"


class UserDetail(models.Model):
    """
    user personal info
    """
    height = models.FloatField(null=False, blank=True)
    weight = models.FloatField(null=False, blank=True)
    sleep = models.FloatField(null=False, blank=True)
    walk = models.FloatField(null=True, blank=True)
    ini_height = models.FloatField(null=False, blank=True)
    ini_weight = models.FloatField(null=False, blank=True)
    ini_sleep = models.FloatField(null=False, blank=True)
    ini_walk = models.FloatField(null=True, blank=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="user_detail")
    goals = models.ManyToManyField("Goal", related_name="user_detail")

    def __str__(self):
        return f"{self.user.username} {self.ini_height}"


class UserExercise(models.Model):
    exercise_name = models.CharField(max_length=50, null=False, blank=True)
    burn_calories = models.PositiveIntegerField(null=False, blank=True)
    sets = models.PositiveIntegerField(default=3, null=True, blank=False)
    reps = models.PositiveIntegerField(default=3, null=True, blank=False)
    last_attempt = models.DateField(auto_now=True, editable=True)
    focus = models.CharField(max_length=50, null=False, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_exercise")

    def __str__(self):
        return f"{self.user.username} \t{self.exercise_name}"


class ExerciseHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='exercise_history')
    exercise = models.ForeignKey(UserExercise, on_delete=models.CASCADE, related_name='exercise_history')
    date = models.DateField(auto_now=True)
    done = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} \t{self.exercise} \t {self.date}"


class Goal(models.Model):
    category = models.CharField(null=False, blank=True, max_length=50)

    def __str__(self):
        return f"{self.category}"


# python manage.py loaddata goals.json
