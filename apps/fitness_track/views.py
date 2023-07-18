import json
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
    Goal
)
from apps.fitness_track.serializers import (
    UserDetailSerializer,
    UserExerciseSerializer,
    GoalSerializer
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
            UserDetailServices.copy_to_initial_data(request.data)
            data.update({"user_id": request.user.id})
            serializer = self.get_serializer()
            serializer = serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
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
            print(request.data)
            serializer = self.get_serializer()
            serializer = serializer(data=request.data)
            serializer.save()

            return success_response(data=serializer.validated_data, status=status.HTTP_200_OK)
        except Exception as ex:
            raise ex


class UserGoals(APIView):

    authentication_classes = [TokenAuthenticationNotGET]
    permission_classes = [IsAuthenticatedNotGET]

    @staticmethod
    def get_serializer():
        return GoalSerializer

    # def post(self, request):
    #     user = request.user.id
    #
    #     serializer = self

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
