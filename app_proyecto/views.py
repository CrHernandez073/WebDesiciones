from django.shortcuts import render
from django.shortcuts import redirect

from app_proyecto import models
# Create your views here.

def inicio(request):

	if request.method == "POST":
		
		curp = request.POST["username"]
		password = request.POST["password"]

		existe = models.Empleados.objects.filter(Curp = curp, contraseña = password).count()

		if existe > 0:
			v_idpuesto = models.Empleados.objects.filter(Curp = curp).values_list("Id_Puesto")
			datos_personales = models.Personas.objects.filter(Curp = curp).values()

			request.session['curp']=curp
			request.session['puesto']="gerente"

			return redirect('inicio_gerente')

		else:
			return render(request, 'app_proyecto/inicio.html')
	else:
		return render(request, 'app_proyecto/inicio.html', {"curp": request.session.get("curp")})
		






		

def logout(request):
    try:
        del request.session['curp']
        del request.session['puesto']
    except KeyError:
        pass
    return redirect('inicio')

def inicio_gerente(request):
	return render(request, 'app_proyecto/gerente/index.html', {"curp": request.session.get("curp")})	

















# if v_idpuesto == 0:
# 				response = render(request, 'app_proyecto/base.html', {"puesto": "Empleado normal", "datos" :datos_personales})
# 			elif v_idpuesto == 1:
# 				response = render(request, 'app_proyecto/base.html', {"puesto": "Supervisor", "datos" :datos_personales})
# 			else:
# 				response = render(request, 'app_proyecto/base.html', {"puesto": "Gerente", "datos" :datos_personales})

# 			response.set_cookie("datos", datos_personales)
# 			response.set_cookie("id_puesto", v_idpuesto)
# 			return response