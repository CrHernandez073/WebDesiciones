from django.db import models
import datetime

# Create your models here.
class PuestoEmpleado(models.Model):
	Id_Puesto = models.CharField(max_length = 40, primary_key = True)

	def __str__(self):
		return  str(self.Id_Puesto)

class Personas(models.Model):
	Curp = models.CharField(max_length = 20, primary_key = True)
	Nombres = models.CharField(max_length = 150)
	Ap_Paterno = models.CharField(max_length = 100)
	Ap_Materno = models.CharField(max_length = 100)
	NSS = models.CharField(max_length = 40) 
	RFC = models.CharField(max_length = 40) 
	Fecha_Nacimiento = models.DateField(auto_now=False, auto_now_add=False)
	Edo_Civil = (
        ("Casado", 'Casado'),
        ("Soltero", 'Soltero'),
        ("Divorciado", 'Divorciado'),
        ("Viudo", 'Viudo'),
        ("Comprometido", 'Comprometido'),
    )
	Escolaridad = (
        ("Primaria",'Primaria'),
        ("Secundaria",'Secundaria'),
        ("Preparatoria",'Preparatoria'),
        ("Universidad",'Universidad'),
    )

	estado_civil=models.CharField(choices=Edo_Civil,max_length=50)
	nivel_escolar = models.CharField(max_length=50, choices=Escolaridad)

	def __str__(self):
		return  self.Curp

class DireccionPersonas(models.Model):
	Curp = models.ForeignKey(Personas, on_delete=models.CASCADE)
	Calle = models.CharField(max_length = 200)
	Colonia = models.CharField(max_length = 200)
	Num_Interior = models.CharField(max_length = 30)
	Num_Exterior = models.CharField(max_length = 30)

	def __str__(self):
		return  self.Curp.Curp

class Empleado(models.Model):
	No_Empleado = models.AutoField(primary_key=True) #autoincrementable
	Curp = models.ForeignKey(Personas, on_delete=models.CASCADE)
	Id_Puesto = models.ForeignKey(PuestoEmpleado, on_delete=models.CASCADE)
	contraseña = models.CharField(max_length=50)
	estado = models.BooleanField(default=True)
	def __str__(self):
		return self.Curp.Curp + ", \t" + str(self.Id_Puesto)

class AreasTrabajo(models.Model):
	Id_Area = models.CharField(max_length = 20, primary_key = True)
	Nombre = models.CharField(max_length = 150)
	Encargado = models.ForeignKey(Empleado, on_delete=models.CASCADE)

	def __str__(self):
		return  self.Nombre

class Examen(models.Model):
	Id_Examen = models.CharField(max_length = 50, primary_key=True)
	Nombre = models.CharField(max_length = 150)
	Id_Area = models.ForeignKey(AreasTrabajo, on_delete=models.CASCADE)
	puntaje_minimo = models.IntegerField()
	puntaje_maximo = models.IntegerField()

	def __str__(self):
		return  self.Nombre

class ExamenPersonas(models.Model):
	Num_Examen = models.AutoField(primary_key=True) #autoincrementable
	Curp = models.ForeignKey(Personas, on_delete=models.CASCADE)
	Id_Examen = models.ForeignKey(Examen, on_delete=models.CASCADE)
	Fecha_Elaborado = models.DateField(auto_now=True)

	def __str__(self):
		return  str(self.Num_Examen) + ", Curp: " + str(self.Curp.Curp)

class ResultadoExamenes(models.Model):
	Num_Examen = models.ForeignKey(ExamenPersonas, on_delete=models.CASCADE)
	Puntaje = models.IntegerField()
	Dictamen=models.CharField(max_length=50)

	def __str__(self):
		return str(self.Num_Examen)


# Enrutamiento estatico: con este enrutamiento el enrutador es ordenado por el administrador de la red, 
# por deonde llegan las redes remotes, se configura manualmente y dentro de sus ventajas, está el control
# total sobre la seleccion de la ruta. 
# 	Ventajas: 
# 		Disponibilidad

# Enrutamiento dinamico: se logra mediante el uso de los protocolos de enrutamiento RIP y IGRP y EIGRP, OSPF.
# Este enrutamiento posee una gran convergencia y escala mucho mejor que el de redes, but tiene un alto costo
# en la utilizacion de recursos como son la ram, ciclo de CPU, y ancho de banda. 

# Los protocolos de enturamiento indican al enrutador como enrutarse. mientras que los protocolos enrutados
# son aquellos que están siendo enrutados por los protocolos de enturamiento.

# TAREA: 
# 	traer para que sirven los protocolos de enrutamiento
# 	RIP
# 	IGRP
# 	EIGRP

# que son sistemas autonomos en redes