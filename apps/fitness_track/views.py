from rest_auth.views import LoginView


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
    