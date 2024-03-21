from django.db import models

# Create your models here.

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=200)
    cantidad= models.IntegerField()
    descripcion= models.CharField(max_length=300,default='')
    precio= models.DecimalField(max_digits=9999999, decimal_places=2)
    def __str__(self):
        return self.nombre+ " - " + self.codigo + " - " + str(self.cantidad) + " - " + str(self.precio) + "€"

class Ticket(models.Model):
    numero= models.IntegerField()
    date= models.DateTimeField()
    #metodo_pago
    total= models.DecimalField(max_digits=9999999, decimal_places=2)
    
class ProductoEnTicket(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)


class Facturas(models.Model):
    numero= models.IntegerField()
    persona_id=models.IntegerField()
    date=models.DateTimeField()
    #metodo_pago
    total= models.DecimalField(max_digits=9999999, decimal_places=2)

class ProductoEnFactura(models.Model):
    factura = models.ForeignKey(Facturas, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

class Persona(models.Model):
    nombre=models.CharField(max_length=200)
    localidad= models.CharField(max_length=200)
    calle=models.CharField(max_length=200)
    nif=models.CharField(max_length=200)
    telefono=models.IntegerField()
    def __str__(self):
        return self.nombre+ " - " + self.localidad + " - " + self.calle + " - " + self.nif + " - " + str(self.telefono)
"""
class Project(models.Model):
    name=models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
class Task(models.Model):
    title=models.CharField(max_length=200)
    description = models.TextField()
    project=models.ForeignKey(Project, on_delete=models.CASCADE)
    done=models.BooleanField(default=False)
    def __str__(self):
        return self.title + " --> " + self.project.name
    """