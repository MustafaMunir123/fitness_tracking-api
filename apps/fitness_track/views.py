from rest_auth.views import LoginView
from rest_framework.views import APIView, status
from apps.utils import success_response
from apps.fitness_track.serializers import (
    UserDetailsSerializer
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


class UserDetailsAPIView(APIView):
    @staticmethod
    def get_serializer():
        return UserDetailsSerializer

    def post(self, request):
        try:
            serializer = self.get_serializer()
            serializer = serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return success_response(data=serializer.validated_data, status=status.HTTP_200_OK)
        except Exception as ex:
            raise ex
