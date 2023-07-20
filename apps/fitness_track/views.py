import json
from datetime import datetime
from typing import List, Any
from rest_auth.views import LoginView
from rest_framework.views import APIView, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from apps.fitness_track.services import UserDetailServices
from apps.custom_permissions import (
    TokenAuthenticationNotGET,
    IsAuthenticatedNotGET
)
from apps.utils import success_response
from apps.fitness_track.models import (
    UserExercise,
    Goal,
    UserDetail,
    CustomUser,
    ExerciseHistory
)
from apps.fitness_track.serializers import (
    UserDetailSerializer,
    UserExerciseSerializer,
    GoalSerializer,
    ExerciseHistorySerializer
)


class LoginUserDetailView(LoginView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.data.update(
            {
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "id": self.user.id,
            }
        )
        return response


class UserDetailAPIView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_serializer():
        return UserDetailSerializer

    def post(self, request):
        try:
            data = request.data
            user_id = request.user.id
            UserDetailServices.copy_to_initial_data(request.data)
            data.update({"user_id": user_id})
            serializer = self.get_serializer()
            serializer = serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            user = CustomUser.objects.get(id=user_id)
            user.complete_details = True
            user.save()

            return success_response(data=serializer.validated_data, status=status.HTTP_200_OK)
        except Exception as ex:
            raise ex


class ExerciseAPIView(APIView):

    def get(self, request):
        try:
            with open("apps/fitness_track/json/exercises.json") as file:
                json_data = json.load(file)
            return success_response(data=json_data, status=status.HTTP_200_OK)
        except Exception as ex:
            raise ex


class UserExerciseAPIView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_serializer():
        return UserExerciseSerializer

    def get(self, request):
        try:
            user_ex = UserExercise.objects.filter(user_id=request.user.id)
            serializer = self.get_serializer()
            serializer = serializer(user_ex, many=True)

            return success_response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            raise ex

    def post(self, request):
        try:
            if UserExercise.objects.filter(user_id=request.user.id, exercise_name=request.data["exercise_name"]).exists():
                raise ValueError("Exercise already exists")
            request.data.update({"user_id": request.user.id})
            serializer = self.get_serializer()
            serializer = serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return success_response(data=serializer.validated_data, status=status.HTTP_200_OK)
        except Exception as ex:
            raise ex


class UserGoals(APIView):

    authentication_classes = [TokenAuthenticationNotGET]
    permission_classes = [IsAuthenticatedNotGET]

    @staticmethod
    def add_ManyToMany_ids(id_list: List, obj: Any) -> None:
        obj.goals.set(id_list)
        obj.save()

    @staticmethod
    def get_serializer():
        return GoalSerializer

    def patch(self, request):
        try:
            user_id = request.user.id
            user_details = UserDetail.objects.get(user_id=user_id)
            self.add_ManyToMany_ids(request.data["goals"], user_details)

            serializer = UserDetailSerializer(user_details, many=False)

            return success_response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            raise ex

    def get(self, request):
        try:
            goals = Goal.objects.all()
            public_session = True

            if str(request.user) != "AnonymousUser":
                user = request.user.id
                goals = Goal.objects.filter(user_id=user)
                public_session = False

            serializer = self.get_serializer()
            serializer = serializer(goals, many=True)

            message = {
                "public_session": public_session,
                "goals": serializer.data
            }
            return success_response(data=message, status=status.HTTP_200_OK)
        except Exception as ex:
            raise ex


class DashBoardAPIView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_id = request.user.id
            user = CustomUser.objects.get(id=user_id)
            date_today = datetime.today().date()

            message = {
                "raise_modal": False,
                "message": "Fill the details first"
            }

            if user.complete_details:
                user_exercises = UserExercise.objects.filter(user_id=user_id)

                exercises_history = {}
                calories_date_data = []
                total_calories_burn = 0
                for exercise in user_exercises:
                    """
                    creates exercise history object if one day is passed (for each user exercise)
                    """
                    if date_today > exercise.last_attempt:
                        exercise_history = {
                            "user_id": user_id,
                            "exercise_id": exercise.id
                        }
                        ExerciseHistory.objects.create(**exercise_history)
                        exercise.last_attempt = date_today

                    """
                    iterating through each exercise and adding each exercise history objects in exercises_history,
                    also storing calories burns per day
                    """
                    if exercise.exercise_name not in exercises_history.keys():
                        exercises_history[exercise.exercise_name] = []
                        past_exercises = ExerciseHistory.objects.filter(user_id=user_id, exercise_id=exercise.id)

                        for past_exercise in past_exercises:
                            exercises_history[exercise.exercise_name].append({
                                "attempted": past_exercise.date,
                                "done": past_exercise.done
                            })

                            if past_exercise.done:
                                total_calories_burn += exercise.burn_calories
                                calories_date_data.append({
                                    "date": past_exercise.date,
                                    "calories_burn": exercise.burn_calories
                                })

                """
                generating recommendations list based of user's goals
                """
                recommendations = []
                user_details = UserDetail.objects.get(user_id=user_id)
                user_detail_serializer = UserDetailSerializer(user_details, many=False)
                if user_detail_serializer.data["goals"]:
                    goals_list = user_detail_serializer.data.get('goals', [])
                    for goal in goals_list:
                        goal_name = str(goal["category"]).upper().replace(" ", "_")
                        with open("apps/fitness_track/json/exercises.json") as file:
                            json_data = json.load(file)
                            recommendations.append(json_data[goal_name])

                """
                calculating expected weight
                """
                initial_weight = user_details.ini_weight
                calorie_factor = 0.00012
                expected_weight = initial_weight - (total_calories_burn * calorie_factor)

                today_exercise = ExerciseHistory.objects.filter(date=datetime.today().date())
                exercise_history_serializer = ExerciseHistorySerializer(today_exercise, many=True)

                message = {
                    "raise_modal": False,
                    "today_exercises": exercise_history_serializer.data,
                    "exercise_history": exercises_history,
                    "calories_date_data": calories_date_data,
                    "total_calories_burn": total_calories_burn,
                    "expected_weight": expected_weight,
                    "recommendations": recommendations
                }

            return success_response(data=message, status=status.HTTP_200_OK)
        except Exception as ex:
            raise ex


class ExerciseHistoryAPIView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:

            user_id = request.user.id
            exercise = ExerciseHistory.objects.get(id=request.data["exercise_id"])
            exercise.done = True
            exercise.save()

            return success_response(data="exercise status updated", status=status.HTTP_200_OK)

        except Exception as ex:
            raise ex



