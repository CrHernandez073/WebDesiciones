from django.db import models
import datetime

# Create your models here.
class PuestoEmpleado(models.Model):
	IdPuesto = models.AutoField(primary_key=True) #autoincrementable
	Nombre = models.CharField(max_length = 150)

	def __str__(self):
		return  self.IdPuesto

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

	def __str__(self):
		return  self.Curp

class DireccionPersonas(models.Model):
	Curp = models.ForeignKey('Personas', on_delete = models.CASCADE,)
	Calle = models.CharField(max_length = 200)
	Colonia = models.CharField(max_length = 200)
	Num_Interior = models.CharField(max_length = 30)
	Num_Exterior = models.CharField(max_length = 30)

	def __str__(self):
		return  self.Curp

class Empleados(models.Model):
	No_Empleado = models.AutoField(primary_key=True) #autoincrementable
	Curp = models.ForeignKey('Personas', on_delete = models.CASCADE,)
	Id_Puesto = models.ForeignKey( 'PuestoEmpleado', on_delete = models.CASCADE,)

	def __str__(self):
		return  self.No_Empleado

class AreasTrabajo(models.Model):
	Id_Area = models.CharField(max_length = 20, primary_key = True)
	Nombre = models.CharField(max_length = 150)
	Encargado = models.ForeignKey('Empleados', on_delete = models.CASCADE,)

	def __str__(self):
		return  self.Nombre

class Examen(models.Model):
	Id_Examen = models.CharField(max_length = 50, primary_key=True)
	Nombre = models.CharField(max_length = 150)
	Id_Area = models.ForeignKey('AreasTrabajo', on_delete = models.CASCADE,)

	def __str__(self):
		return  self.Nombre

class ExamenPersona(models.Model):
	Num_Examen = models.AutoField(primary_key=True) #autoincrementable
	Curp = models.ForeignKey('Personas', on_delete = models.CASCADE,)
	Id_Examen = models.ForeignKey('Examen', on_delete = models.CASCADE,)	
	Fecha_Elaborado = models.DateField(auto_now=True)

	def __str__(self):
		return  self.Num_Examen + ", Curp: " + self.Curp

class ResultadoExamen(models.Model):
	Num_Examen = models.ForeignKey('ExamenPersona', on_delete = models.CASCADE,)
	Aciertos = models.IntegerField()
	Errores = models.IntegerField()
	Cant_Preguntas = models.IntegerField()
	Dictamen = (
        ("Aceptado",'Aceptado'),
        ("Rechazado",'Rechazado'),
    )

	def __str__(self):
		return  self.Num_Examen + ", Dictamen: " + self.Dictamen