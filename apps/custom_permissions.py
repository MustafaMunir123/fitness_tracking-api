from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class TokenAuthenticationNotGET(TokenAuthentication):
    def authenticate(self, request):
        if request.method == 'GET' and "HTTP_AUTHORIZATION" not in request.META.keys():
            return None
        else:
            return super().authenticate(request)


class IsAuthenticatedNotGET(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True

        return super().has_permission(request, view)
