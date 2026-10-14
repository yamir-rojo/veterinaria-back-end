from django.db import models


class Cliente(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    apellido = models.CharField(max_length=100, verbose_name='Apellido')
    telefono = models.CharField(max_length=20, verbose_name='Teléfono')
    email = models.EmailField(verbose_name='Correo electrónico')
    direccion = models.CharField(max_length=200, verbose_name='Dirección')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f'{self.nombre} {self.apellido}'


class Atencion(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='atenciones', verbose_name='Cliente')
    mascota = models.CharField(max_length=100, verbose_name='Mascota')
    tipo_atencion = models.CharField(max_length=100, verbose_name='Tipo de atención')
    fecha = models.DateField(verbose_name='Fecha')
    costo = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Costo')
    descripcion = models.TextField(verbose_name='Descripción')

    class Meta:
        verbose_name = 'Atención'
        verbose_name_plural = 'Atenciones'
        ordering = ['-fecha', 'mascota']

    def __str__(self):
        return f'{self.mascota} - {self.tipo_atencion}'

    @property
    def costo_formateado(self):
        return f'${self.costo:,.0f}'.replace(',', '.')
