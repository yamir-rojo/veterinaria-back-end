from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from veterinaria.models import Atencion, Cliente


class Command(BaseCommand):
    help = 'Crea grupos, usuarios y datos iniciales del sistema veterinario.'

    def handle(self, *args, **options):
        cliente_ct = ContentType.objects.get(app_label='veterinaria', model='cliente')
        atencion_ct = ContentType.objects.get(app_label='veterinaria', model='atencion')

        digitador_group, _ = Group.objects.get_or_create(name='Digitador')
        revisor_group, _ = Group.objects.get_or_create(name='Revisor')

        digitador_perms = Permission.objects.filter(
            content_type__in=[cliente_ct, atencion_ct],
            codename__in=['view_cliente', 'add_cliente', 'change_cliente', 'view_atencion', 'add_atencion', 'change_atencion'],
        )
        revisor_perms = Permission.objects.filter(
            content_type__in=[cliente_ct, atencion_ct],
            codename__in=['view_cliente', 'view_atencion'],
        )

        digitador_group.permissions.set(digitador_perms)
        revisor_group.permissions.set(revisor_perms)

        director, director_created = User.objects.get_or_create(
            username='director',
            defaults={'is_staff': True, 'is_superuser': True, 'email': 'director@veterinaria.cl'},
        )
        director.set_password('Inacap.2026')
        director.is_staff = True
        director.is_superuser = True
        director.save()

        digitador, _ = User.objects.get_or_create(
            username='digitador',
            defaults={'is_staff': True, 'email': 'digitador@veterinaria.cl'},
        )
        digitador.set_password('Inacap.2026')
        digitador.is_staff = True
        digitador.save()
        digitador.groups.set([digitador_group])

        revisor, _ = User.objects.get_or_create(
            username='revisor',
            defaults={'is_staff': True, 'email': 'revisor@veterinaria.cl'},
        )
        revisor.set_password('Inacap.2026')
        revisor.is_staff = True
        revisor.save()
        revisor.groups.set([revisor_group])

        clientes = [
            {'nombre': 'Ana', 'apellido': 'García', 'telefono': '+56911111111', 'email': 'ana.garcia@example.com', 'direccion': 'Av. Las Condes 101'},
            {'nombre': 'Luis', 'apellido': 'Pérez', 'telefono': '+56922222222', 'email': 'luis.perez@example.com', 'direccion': 'Calle Los Pinos 22'},
            {'nombre': 'Sofía', 'apellido': 'Martínez', 'telefono': '+56933333333', 'email': 'sofia.martinez@example.com', 'direccion': 'Pasaje El Bosque 8'},
        ]

        clientes_db = []
        for data in clientes:
            cliente, _ = Cliente.objects.get_or_create(**data)
            clientes_db.append(cliente)

        atenciones = [
            {'cliente': clientes_db[0], 'mascota': 'Luna', 'tipo_atencion': 'Consulta general', 'fecha': '2026-01-10', 'costo': 45000, 'descripcion': 'Control anual y revisión de signos vitales.'},
            {'cliente': clientes_db[0], 'mascota': 'Luna', 'tipo_atencion': 'Vacunación', 'fecha': '2026-02-12', 'costo': 32000, 'descripcion': 'Vacuna antirrábica anual aplicada.'},
            {'cliente': clientes_db[1], 'mascota': 'Max', 'tipo_atencion': 'Cirugía menor', 'fecha': '2026-01-18', 'costo': 89000, 'descripcion': 'Extracción de cuerpo extraño en la pata.'},
            {'cliente': clientes_db[1], 'mascota': 'Max', 'tipo_atencion': 'Desparasitación', 'fecha': '2026-03-05', 'costo': 24000, 'descripcion': 'Tratamiento antiparasitario mensual.'},
            {'cliente': clientes_db[2], 'mascota': 'Nina', 'tipo_atencion': 'Rayos X', 'fecha': '2026-02-22', 'costo': 67000, 'descripcion': 'Radiografía de columna para evaluación.'},
            {'cliente': clientes_db[2], 'mascota': 'Nina', 'tipo_atencion': 'Control postoperatorio', 'fecha': '2026-03-16', 'costo': 37000, 'descripcion': 'Revisión del postoperatorio y puntos de sutura.'},
        ]

        for data in atenciones:
            Atencion.objects.get_or_create(
                cliente=data['cliente'],
                mascota=data['mascota'],
                tipo_atencion=data['tipo_atencion'],
                fecha=data['fecha'],
                costo=data['costo'],
                descripcion=data['descripcion'],
            )

        self.stdout.write(self.style.SUCCESS('Datos iniciales cargados correctamente.'))
