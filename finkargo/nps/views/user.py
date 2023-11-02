from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication
from nps.serializers import AuthTokenSerializer, UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        Token.objects.filter(user=user).delete()

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'full_name': user.get_full_name()
        })


class CreateUserView(CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)
