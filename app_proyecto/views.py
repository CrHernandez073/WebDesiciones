from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.views.generic.list import ListView

from django.http import HttpResponse
from django.core import serializers
import json

from app_proyecto import models
# Create your views here.

def login(request):

	#SE EJECUTARÁ ESTA ACCION SI SE ACCEDE A LA PAGINA DEL MODO POST
	if request.method == "POST":
		#Obtiene los elementos de la base de datos
		datos = models.Empleado.objects.get(Curp=request.POST.get('f_curp'))
		if datos.contraseña == request.POST.get('f_contraseña'):

			#SE CREAN VARIABLES DE SESION
			request.session['curp'] = str(datos.Curp)
			request.session['id_puesto'] = str(datos.Id_Puesto)
	
			if str(datos.Id_Puesto) == "Empleado":
				return redirect('inicio_gerente')
			elif str(datos.Id_Puesto == "Supervisor"):
				return redirect('inicio_gerente')
			elif str(datos.Id_Puesto == "Gerente"):
				return redirect('inicio_gerente')
	
	#EL USUARIO TIPEÓ LA URL
	else:
		return render(request, 'app_proyecto/login.html')


def logout(request):
    #SE DESTRUYEN LAS VARIABLES DE SESION
    try:
        del request.session['curp']
        del request.session['id_puesto']
    except KeyError:
        pass
	#DESPUES DE DESTRUIR LAS VARIABLES DE SESIÓN, TE REDIGIRÁ A LA URL QUE TENGA EL NOMBRE "login"
    return redirect('login')

# ENLACES DEL GERENTE!
def inicio_gerente(request):
	return render(request, 'app_proyecto/gerente/index.html')

class consulta_empleados(ListView):
    template_name= "app_proyecto/gerente/consulta_empleados.html"
    queryset = models.Empleado.objects.filter(Id_Puesto = 0)

class consulta_supervisores(ListView):
    template_name= "app_proyecto/gerente/consulta_supervisores.html"
    queryset = models.Empleado.objects.filter(Id_Puesto = 1)

class consulta_gerentes(ListView):
    template_name= "app_proyecto/gerente/consulta_gerentes.html"
    queryset = models.Empleado.objects.filter(Id_Puesto = 2)

#FORMULARIOS OBLIGATORIOS
class form_persona(CreateView):
    template_name= "app_proyecto/form_persona.html"
    model = models.Personas
    fields = "__all__"
    success_url = reverse_lazy("login")

class form_persona_domicilio(CreateView):
    template_name= "app_proyecto/form_persona_domicilio.html"
    model = models.DireccionPersonas
    fields = "__all__"
    success_url = reverse_lazy("login")

def json_supervisor(request):
	data = serializers.serialize('json', models.Empleado.objects.filter(Id_Puesto = 2))
	return HttpResponse(data, "application/json")


#----------------- EXAMENES -----------------
def examen_jefe_abarrotes(request):	
	#SE EJECUTARÁ ESTA ACCION SI SE ACCEDE A LA PAGINA DEL MODO POST
	if request.method == "POST":
		curp = str(request.POST.get('curp'))
		datos = models.Personas.objects.get(Curp = curp)

		# 1. Verifica si el curp ingresado existe en la bd
		if datos.Curp == curp:
			detalle_examen = models.Examen.objects.get(Id_Examen="Examen Jefe Abarrotes") #Obtiene los detalles del examen

			id_examen = detalle_examen.Id_Examen
			minimo = int(detalle_examen.puntaje_minimo)
			maximo = int(detalle_examen.puntaje_maximo)

			#Cacha los valores que trae el formulario
			puntaje_edad = int(request.POST.get('edad'))
			puntaje_ingles = int(request.POST.get('ingles'))
			puntaje_estudios = int(request.POST.get('estudios'))		
			arr_consultas = request.POST.getlist('consultas') #Lista de valores seleccionados
			arr_experiencia = request.POST.getlist('experiencia') #Lista de valores seleccionados
			arr_conocimientos = request.POST.getlist('conocimientos') #Lista de valores seleccionados

			puntale_consulta = 0
			puntale_experiencia = 0
			puntale_conocimiento = 0

			for puntaje in arr_consultas:
				puntale_consulta = puntale_consulta + int(puntaje)

			for puntaje in arr_experiencia:
				puntale_experiencia = puntale_experiencia + int(puntaje)

			for puntaje in arr_conocimientos:
				puntale_conocimiento = puntale_conocimiento + int(puntaje)
			
			resultado_examen = puntaje_edad + puntaje_ingles + puntaje_estudios + puntale_consulta + puntale_experiencia + puntale_conocimiento

			#1. Guardando el examenrealizado 
			p = models.ExamenPersonas(Curp=models.Personas.objects.get(Curp=curp), Id_Examen=models.Examen.objects.get(Id_Examen=id_examen))
			p.save()

			#2. Extraer "num_examen"
			detalle = models.ExamenPersonas.objects.get(Curp=curp, Id_Examen="Examen Jefe Abarrotes")
			num_examen = detalle.Num_Examen

			if resultado_examen >= minimo:
				p = models.ResultadoExamenes(Num_Examen=models.ExamenPersonas.objects.get(Num_Examen=num_examen), Puntaje=resultado_examen, Dictamen = "Aceptado")
				p.save()

				e = models.Empleado(Curp=models.Personas.objects.get(Curp=curp), Id_Puesto=models.PuestoEmpleado.objects.get(Id_Puesto="Jefe de abarrotes"))
				e.save()

				contexto = {'resultado':"Aceptado", "r_color": "green"}
				return render(request, "app_proyecto/examenes/examen_jefe_abarrotes.html", contexto)
			else:
				p = models.ResultadoExamenes(Num_Examen=models.ExamenPersonas.objects.get(Num_Examen=num_examen), Puntaje=resultado_examen, Dictamen = "Rechazado")
				p.save()
				contexto = {'resultado':"Suerte para la próxima bro :V", "r_color": "red"}
				return render(request, "app_proyecto/examenes/examen_jefe_abarrotes.html", contexto)		
		else:
			contexto = {'Sumatoria':'ERROR'}
			return render(request, "app_proyecto/examenes/examen_jefe_abarrotes.html", contexto)
	else:
		supervisor = models.Empleado.objects.get(Id_Puesto = "Supervisor")
		contexto = {"No_Empleado": supervisor.No_Empleado, "Contraseña": supervisor.contraseña}
		return render(request, "app_proyecto/examenes/examen_jefe_abarrotes.html", contexto)

def examen_cajas(request):	
	#SE EJECUTARÁ ESTA ACCION SI SE ACCEDE A LA PAGINA DEL MODO POST
	if request.method == "POST":
		curp = str(request.POST.get('curp'))
		datos = models.Personas.objects.get(Curp = curp)

		# 1. Verifica si el curp ingresado existe en la bd
		if datos.Curp == curp:
			detalle_examen = models.Examen.objects.get(Id_Examen="Examen Jefe de Cajas") #Obtiene los detalles del examen

			id_examen = detalle_examen.Id_Examen
			minimo = int(detalle_examen.puntaje_minimo)
			maximo = int(detalle_examen.puntaje_maximo)

			#Cacha los valores que trae el formulario
			puntaje_edad = int(request.POST.get('edad'))
			puntaje_ingles = int(request.POST.get('ingles'))
			puntaje_estudios = int(request.POST.get('estudios'))		
			arr_consultas = request.POST.getlist('consultas') #Lista de valores seleccionados
			arr_experiencia = request.POST.getlist('experiencia') #Lista de valores seleccionados

			puntale_consulta = 0
			puntale_experiencia = 0

			for puntaje in arr_consultas:
				puntale_consulta = puntale_consulta + int(puntaje)

			for puntaje in arr_experiencia:
				puntale_experiencia = puntale_experiencia + int(puntaje)

		
			resultado_examen = puntaje_edad + puntaje_ingles + puntaje_estudios + puntale_consulta + puntale_experiencia

			#1. Guardando el examenrealizado 
			p = models.ExamenPersonas(Curp=models.Personas.objects.get(Curp=curp), Id_Examen=models.Examen.objects.get(Id_Examen=id_examen))
			p.save()

			#2. Extraer "num_examen"
			detalle = models.ExamenPersonas.objects.get(Curp=curp, Id_Examen="Examen Jefe de Cajas")
			num_examen = detalle.Num_Examen

			if resultado_examen >= minimo:
				p = models.ResultadoExamenes(Num_Examen=models.ExamenPersonas.objects.get(Num_Examen=num_examen), Puntaje=resultado_examen, Dictamen = "Aceptado")
				p.save()

				e = models.Empleado(Curp=models.Personas.objects.get(Curp=curp), Id_Puesto=models.PuestoEmpleado.objects.get(Id_Puesto="Jefe de Cajas"))
				e.save()

				contexto = {'resultado':"Aceptado", "r_color": "green"}
				return render(request, "app_proyecto/login.html", contexto)
			else:
				p = models.ResultadoExamenes(Num_Examen=models.ExamenPersonas.objects.get(Num_Examen=num_examen), Puntaje=resultado_examen, Dictamen = "Rechazado")
				p.save()
				contexto = {'resultado':"Suerte para la próxima bro :V", "r_color": "red"}
				return render(request, "app_proyecto/examenes/login.html", contexto)		
		else:
			contexto = {'Sumatoria':'ERROR'}
			return render(request, "app_proyecto/examenes/examen_cajas.html", contexto)
	else:
		supervisor = models.Empleado.objects.get(Id_Puesto = "Supervisor")
		contexto = {"No_Empleado": supervisor.No_Empleado, "Contraseña": supervisor.contraseña}
		return render(request, "app_proyecto/examenes/examen_cajas.html", contexto)