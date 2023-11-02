from django.urls import path, include

from .views import CreateUserView, CreateTokenView, EntidadView, ColaboradorView, EncuestaView, ReportsView, EncuestaNPSView
from rest_framework.routers import DefaultRouter


app_name = 'nps'

router = DefaultRouter()

router.register('entidad', EntidadView, basename='entidad')
router.register('colaborador', ColaboradorView, basename='colaborador')
router.register('encuesta', EncuestaView, basename='encuesta')
router.register('nps_bajo', EncuestaNPSView, basename='nps_bajo')

urlpatterns = [
    path('create_user/', CreateUserView.as_view(), name='create'),
    path('token/', CreateTokenView.as_view(), name='token'),
    path('reports/', ReportsView.as_view(), name='reports'),
    path('', include(router.urls)),
]
