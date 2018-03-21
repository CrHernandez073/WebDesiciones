from django.contrib import admin
from django.urls import path
from app_proyecto import views

urlpatterns = [
    path('admin/', admin.site.urls), #Administraciòn por defecto

    #LINKS DE SESIÓN
    path('login/', views.login, name = 'login'), #Iniciar sesiòn
    path('salir/', views.logout, name = 'salir'),

    #LINKS DEL GERENTE
    path('inicio_gerente/', views.inicio_gerente, name = 'inicio_gerente'),
    path('consulta_empleados/', views.consulta_empleados.as_view(), name = 'consulta_empleados'),
    path('consulta_supervisores/', views.consulta_supervisores.as_view(), name = 'consulta_supervisores'),
    path('consulta_gerentes/', views.consulta_gerentes.as_view(), name = 'consulta_gerentes'),

#FORMULARIO
   # 1.- Crear a la persona
	path('form_persona/', views.form_persona.as_view(), name = 'form_persona'),
	path('form_persona_domicilio/', views.form_persona_domicilio.as_view(), name = 'form_persona_domicilio'),
    path('form_caja/', views.form_caja.as_view(), name = 'form_caja'),
    
]
