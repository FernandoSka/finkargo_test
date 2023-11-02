from nps.models import Entidad, Colaborador, Encuesta
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
import random
from datetime import timedelta, datetime

def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)

class Command(BaseCommand):
    """Command to verify is the user admin exits, case don't create it"""

    def handle(self, *args, **options):
        entidades = [
            {"nombre": "BBVA", "tipo": "Banco", "pais": "Mexico"},
            {"nombre": "Amazon", "tipo": "Empresa", "pais": "EEUU"},
            {"nombre": "Claro", "tipo": "Empresa", "pais": "Colombia"},
            {"nombre": "YPF", "tipo": "Empresa", "pais": "Argentina"},
            {"nombre": "Empresa4", "tipo": "banco", "pais": "Chile"},
            {"nombre": "Empresa5", "tipo": "Partner", "pais": "Peru"},
            {"nombre": "Empresa6", "tipo": "Empresa", "pais": "Venezuela"},
            {"nombre": "Empresa7", "tipo": "Empresa", "pais": "Bolivia"},
        ]
        cargos = [
            "Empleado",
            "socio",
            "accionista",
            "gestor",
        ]
        for entidad in entidades:
            new_entidad = Entidad.objects.create(**entidad)
            for i in range(1,5):
                empleado_base = f"Colaborador_{i}_{new_entidad.nombre}"
                user_colaborador = get_user_model().objects.filter(email=f"{empleado_base}@nps.com")
                if len(user_colaborador) == 0:
                    payload = {
                        'email': f"{empleado_base}@nps.com",
                        'password': "123abc456",
                        'name': empleado_base,
                        'last_name': 'colaborador',
                    }
                    user_colaborador = get_user_model().objects.create_user(**payload)
                    Colaborador.objects.create(user=user_colaborador, entidad=new_entidad, nombre=empleado_base, cargo=cargos[random.randint(0,3)])
                    
        entidad_list = Entidad.objects.all()
        colaborador_list = Colaborador.objects.all()
        for i in range(0,200):
            ran_entidad = entidad_list[random.randint(0, entidad_list.count()-1)]
            ran_colaborador = colaborador_list[random.randint(0, colaborador_list.count()-1)]
            d1 = datetime.strptime('1/1/2023 1:00 AM', '%m/%d/%Y %I:%M %p')
            d2 = datetime.strptime('1/1/2024 1:00 AM', '%m/%d/%Y %I:%M %p')
            Encuesta.objects.create(
                user=ran_colaborador.user,
                entidad=ran_entidad,
                nombre=ran_colaborador.nombre,
                email=ran_colaborador.user.email,
                calificacion=random.randint(0, 10),
                fecha=random_date(d1, d2),
            )



