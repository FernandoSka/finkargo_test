from rest_framework import serializers
from django.contrib.auth import get_user_model
from nps.models import Entidad, Colaborador, Encuesta


class EntidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entidad
        fields = '__all__'
        read_only_fields = ('id',)


class ColaboradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colaborador
        fields = '__all__'
        read_only_fields = ('id',)


class EncuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Encuesta
        fields = '__all__'
        read_only_fields = ('id', 'fecha', 'contactado')


class TopSerializer(serializers.Serializer):
    pais = serializers.CharField(source="entidad__pais")
    total = serializers.IntegerField(source="total_count")


class BestPromotorSerializer(serializers.Serializer):
    tipo_persona = serializers.CharField(source="user__user_colaborador__cargo")
    total = serializers.IntegerField(source="total_count")


class MonthSerializer(serializers.Serializer):
    entidad__nombre = serializers.CharField()
    month = serializers.DateTimeField(format="%Y-%m")
    total = serializers.IntegerField()



class UserColaboradorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Colaborador
        fields = (
            "entidad",
            "nombre",
            "cargo",
        )
        read_only_fields = (
            "entidad",
            "nombre",
            "cargo",
        )


class UserNPSSerializer(serializers.ModelSerializer):
    user_colaborador = UserColaboradorSerializer()
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = (
            'id', 
            'email', 
            'name', 
            'last_name', 
            'user_colaborador'
            )
        read_only_fields = (
            'id', 
            'email', 
            'name', 
            'last_name', 
            'user_colaborador'
            )


class EncuestaCompleteSerializer(serializers.ModelSerializer):
    user = UserNPSSerializer(required=False, allow_null=True)


    class Meta:
        model = Encuesta
        fields = (
            'id',
            'user',
            'entidad',
            'nombre',
            'email',
            'calificacion',
            'fecha',
            'contactado'
        )
        read_only_fields = (
            'id',
            'user',
            'entidad',
            'nombre',
            'email',
            'calificacion',
            'fecha'
            )
