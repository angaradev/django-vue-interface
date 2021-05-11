from rest_framework.response import Response
from rest_framework.views import APIView
from users.api.serializers import UserDisplaySerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


class CurrentUserAPIVeiw(APIView):
    def get(self, request):
        serializer = UserDisplaySerializer(request.user)
        return Response(serializer.data)


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data["token"])
        return Response(
            {
                "token": token.key,
                "user": {"username": token.user.username, "email": token.user.email},
            }
        )
