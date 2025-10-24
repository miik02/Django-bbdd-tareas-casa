from django.db import models

# Create your models here.

class Tarea(models.Model):
    TAREAS = [("CENA", "Cena"), ("COMIDA", "Comida")]
    
    persona = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateTimeField()
    tarea = models.CharField(max_length=20, choices=TAREAS, default="COMIDA")
    pone_mesa = models.BooleanField(default=True)
    quita_mesa = models.BooleanField(default=True)
    mete_lava = models.BooleanField(default=False)
    saca_lava = models.BooleanField(default=False)
    era_mi_turno = models.BooleanField(default=True)
    num_fregados = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.persona} hizo {self.tarea}"
    
class Users(models.Model):
    name = models.CharField(max_length=100)
    contraseña = models.CharField(max_length=20)
    
    def __str__(self):
        return f"Usuario: {self.name}"