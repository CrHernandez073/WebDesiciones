from django.contrib import admin
from app_proyecto import models

# Register your models here.
admin.site.register(models.PuestoEmpleado)
admin.site.register(models.Personas)
admin.site.register(models.DireccionPersonas)
admin.site.register(models.Empleado)
admin.site.register(models.AreasTrabajo)
admin.site.register(models.Examen)
admin.site.register(models.ExamenPersonas)
admin.site.register(models.ResultadoExamenes)