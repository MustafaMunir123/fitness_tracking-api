from rest_framework import serializers
from apps.fitness_track.models import *

class CustomUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)
    phone = serializers.CharField(max_length=13)
    complete_details = serializers.BooleanField(default=True)

    def create(self, validated_data):
        return CustomUser.objects.create(**validated_data)


class GoalSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    category = serializers.CharField(max_length=50)

    def create(self, validated_data):
        return Goal.objects.create(**validated_data)


class UserDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    height = serializers.FloatField()
    weight = serializers.FloatField()
    sleep = serializers.FloatField()
    walk = serializers.FloatField(allow_null=True)
    ini_height = serializers.FloatField()
    ini_weight = serializers.FloatField()
    ini_sleep = serializers.FloatField()
    ini_walk = serializers.FloatField(allow_null=True)
    user_id = serializers.IntegerField()
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    goals = GoalSerializer(read_only=True, many=True)

    def create(self, validated_data):
        return UserDetail.objects.create(**validated_data)

    def update(self, instance, validated_data):
        user_details = UserDetail.objects.filter(id=instance.id).update(**validated_data)
        return user_details


class UserExerciseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField()
    exercise_name = serializers.CharField(max_length=50)
    burn_calories = serializers.IntegerField()
    sets = serializers.IntegerField(default=3)
    reps = serializers.IntegerField(default=3)
    # last_attempt = serializers.CharField(allow_null=True, max_length=40, allow_blank=True)

    def create(self, validated_data):
        return UserExercise.objects.create(**validated_data)


class ExerciseHistorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField()
    exercise_id = serializers.IntegerField()
    done = serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        return ExerciseHistory.objects.create(**validated_data)




    # def update(self, instance, validated_data):
    #     event = Goal.objects.filter(id=instance.id).update(**validated_data)
    #     return event
