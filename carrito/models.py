from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.
class Platillo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)

    def clean(self):
        # Agregamos validaciones personalizadas para el modelo Platillo
        if self.precio <= 0:
            raise ValidationError("El precio debe ser mayor que cero.")

    def __str__(self):
        return self.nombre 
    
class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    platillo = models.ForeignKey(Platillo, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    total = models.DecimalField(max_digits=8, decimal_places=2)

    def clean(self):
        # Validacion personalizada: la cantidad debe ser mayor que cero
        if self.cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor que cero.")

    def save(self, *args, **kwargs):
        # Calcula el total antes de guardar el pedido
        self.total = self.platillo.precio + self.cantidad
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Orden: {self.platillo} - {self.cantidad}"