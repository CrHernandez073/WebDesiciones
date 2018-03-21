from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy

from django.views.generic.list import ListView

from app_proyecto import models
# Create your views here.

def login(request):

	#SE EJECUTARÁ ESTA ACCION SI SE ACCEDE A LA PAGINA DEL MODO POST
	if request.method == "POST":
		#Obtiene los elementos de la base de datos
		datos = models.Empleados.objects.get(Curp=request.POST.get('f_curp'))
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
    queryset = models.Empleados.objects.filter(Id_Puesto = 0)

class consulta_supervisores(ListView):
    template_name= "app_proyecto/gerente/consulta_supervisores.html"
    queryset = models.Empleados.objects.filter(Id_Puesto = 1)

class consulta_gerentes(ListView):
    template_name= "app_proyecto/gerente/consulta_gerentes.html"
    queryset = models.Empleados.objects.filter(Id_Puesto = 2)

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

class form_caja(CreateView):
    template_name= "app_proyecto/form_caja.html"
    model = models.AreasTrabajo
    fields = "__all__"
    success_url = reverse_lazy("login")