from django.db import models

# Create your models here.
from django.db import models

class Estudiante(models.Model):
    TIPO_DOC = [('CC', 'Cédula'), ('TI', 'Tarjeta de Identidad')]

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=2, choices=TIPO_DOC)
    numero_documento = models.CharField(max_length=20)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()
    ficha = models.CharField(max_length=10)
    programa = models.CharField(max_length=100)
    horario = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Reporte(models.Model):
    TIPO_REPORTE = [('Académico', 'Académico'), ('Disciplinario', 'Disciplinario')]

    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_REPORTE)
    detalle = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    instructor = models.CharField(max_length=100)

    def __str__(self):
        return f"Reporte {self.tipo} - {self.estudiante}"
