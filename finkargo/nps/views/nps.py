from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.settings import api_settings
from rest_framework import authentication, viewsets, permissions
from django.db.models import Count, Case, When
from django.db.models.functions import TruncMonth

from nps.models import Entidad, Colaborador, Encuesta

from nps.serializers import EntidadSerializer, ColaboradorSerializer, EncuestaSerializer,\
    TopSerializer, BestPromotorSerializer, MonthSerializer, EncuestaCompleteSerializer

from nps.decorators import add_meta_info

class EntidadView(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'put', 'delete']
    """Create a new user in the system"""
    serializer_class = EntidadSerializer
    queryset = Entidad.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)


class ColaboradorView(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'put', 'delete']
    """Create a new user in the system"""
    serializer_class = ColaboradorSerializer
    queryset = Colaborador.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)


class EncuestaView(viewsets.ModelViewSet):
    http_method_names = ['post']
    """Create a new user in the system"""
    serializer_class = EncuestaSerializer
    queryset = Encuesta.objects.all()
    authentication_classes = (authentication.TokenAuthentication,)


    @add_meta_info
    def create(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_anonymous:
            request.data.update({
                "user": user.id,
                "nombre": user.get_full_name(),
                "email": user.email
            })
        return super().create(request, *args,**kwargs)


class ReportsView(APIView):
    """Manage the authenticated user"""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def get(self, request):
        top_3 = Encuesta.objects.filter(
            calificacion__lte=6).values(
                "entidad__pais").annotate(
                    total_count=Count("entidad")).order_by("-total_count")
        top_3_serializer = TopSerializer(data=top_3, many=True)
        top_3_serializer.is_valid()

        best_promotor = Encuesta.objects.filter(calificacion__in=[9,10]).values(
            "user__user_colaborador__cargo").annotate(
                    total_count=Count(
                        Case(
                            When(user__isnull=True, then=1),
                            When(user__isnull=False, then=1),
                            )
                        )
                    ).order_by("-total_count")
        best_promotor_serializer = BestPromotorSerializer(data=best_promotor, many=True)
        best_promotor_serializer.is_valid()

        best_by_month = Encuesta.objects.filter(calificacion__in=[9,10]).values("entidad__nombre").annotate(
            month=TruncMonth('fecha'), total=Count("entidad__nombre")
            ).values("month", "total", "entidad__nombre").order_by("month")
        best_by_month_arr=[]
        for date in best_by_month.dates('fecha','month',order='DESC'):
            best = best_by_month.filter(fecha__date__month=date.month, fecha__date__year=date.year).order_by("-total")[0]
            best_by_month_serializer = MonthSerializer(data=best)
            best_by_month_serializer.is_valid()
            best_by_month_arr.append(best_by_month_serializer.data)

        
        worst_by_month = Encuesta.objects.filter(calificacion__lte=6).values("entidad__nombre").annotate(
            month=TruncMonth('fecha'), total=Count("entidad__nombre")
            ).values("month", "total", "entidad__nombre").order_by("month")
        worst_by_month_arr=[]
        for date in worst_by_month.dates('fecha','month',order='DESC'):
            best = worst_by_month.filter(fecha__date__month=date.month, fecha__date__year=date.year).order_by("-total")[0]
            worst_by_month_serializer = MonthSerializer(data=best)
            worst_by_month_serializer.is_valid()
            worst_by_month_arr.append(worst_by_month_serializer.data)
        
        ret_data ={
            "top_peor_3_paises": top_3_serializer.data[0:3],
            "mejor_tipo_promotor": best_promotor_serializer.data,
            "mejores_por_mes": best_by_month_arr,
            "peores_por_mes": worst_by_month_arr,

        }
        return Response(ret_data)


class EncuestaNPSView(viewsets.ModelViewSet):
    http_method_names = ['get', 'put']
    """Create a new user in the system"""
    serializer_class = EncuestaCompleteSerializer
    queryset = Encuesta.objects.filter(calificacion__lte=4)