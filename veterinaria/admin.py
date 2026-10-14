from django.contrib import admin

from .models import Atencion, Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'telefono', 'email', 'direccion')
    search_fields = ('nombre', 'apellido', 'telefono', 'email')
    list_filter = ('apellido',)
    ordering = ('apellido', 'nombre')


@admin.register(Atencion)
class AtencionAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'mascota', 'tipo_atencion', 'fecha', 'costo_formateado', 'descripcion')
    search_fields = ('mascota', 'tipo_atencion', 'descripcion', 'cliente__nombre', 'cliente__apellido')
    list_filter = ('fecha', 'tipo_atencion', 'cliente')
    ordering = ('-fecha', 'mascota')

    def costo_formateado(self, obj):
        return f'${obj.costo:,.0f}'.replace(',', '.')

    costo_formateado.short_description = 'Costo'
