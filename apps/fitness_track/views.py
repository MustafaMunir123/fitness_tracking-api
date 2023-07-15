import json
from rest_auth.views import LoginView
from rest_framework.views import APIView, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from apps.utils import success_response
from apps.fitness_track.models import (
    UserExercise
)
from apps.fitness_track.serializers import (
    UserDetailSerializer,
    UserExerciseSerializer
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
