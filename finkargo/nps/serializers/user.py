from rest_framework import serializers
from rest_framework import status
from django.contrib.auth import get_user_model, authenticate
from rest_framework.exceptions import APIException
from django.utils.encoding import force_str


class CustomTokenException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail, field, status_code):
        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            self.detail = {field: force_str(detail)}
        else:
            self.detail = {'detail': force_str(self.default_detail)}


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""
    password = serializers.CharField()

    class Meta:
        model = get_user_model()
        fields = (
            'id', 
            'email', 
            'name', 
            'last_name',
            'password'
            )
        read_only_fields = ('id',)

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        try:
            password = validated_data.pop("password", "")
            if not password:
                password = get_user_model().objects.make_random_password()
            new_user = get_user_model()(**validated_data)
            new_user.set_password(password)
            new_user.save()
            return new_user
        except Exception as ie:
            raise serializers.ValidationError(ie.args)
        

class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = 'Credenciales Invalidas!'
            raise CustomTokenException(detail=msg, field='mensaje', status_code=status.HTTP_401_UNAUTHORIZED)
        attrs['user'] = user
        return attrs
