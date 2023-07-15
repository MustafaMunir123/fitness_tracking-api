from rest_framework import serializers
from apps.fitness_track.models import *

class CustomUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)
    phone = serializers.CharField(max_length=13)

    def create(self, validated_data):
        return CustomUser.objects.create(**validated_data)


class UserDetailsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    height = serializers.FloatField()
    weight = serializers.FloatField()
    sleep = serializers.FloatField()
    walk = serializers.FloatField(allow_null=True)
    exercises = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def create(self, validated_data):
        return UserDetails.objects.create(**validated_data)


class UserExerciseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    exercise_name = serializers.CharField(max_length=50)
    burn_calories = serializers.IntegerField()
    sets = serializers.IntegerField(default=3)
    reps = serializers.IntegerField(default=3)
    last_attempted = serializers.DateField(allow_null=True)
    done = serializers.BooleanField(default=False)

    def create(self, validated_data):
        return UserExercise.objects.create(**validated_data)


class ExerciseHistorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    exercise = serializers.PrimaryKeyRelatedField(read_only=True)
    date = serializers.DateField()

    def create(self, validated_data):
        return ExerciseHistory.objects.create(**validated_data)


class GoalSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    category = serializers.CharField(max_length=50)

    def create(self, validated_data):
        return Goal.objects.create(**validated_data)
