from django.db import models
from django.contrib.auth.models import User

from products.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="usuario")
    is_active = models.BooleanField(default=True, verbose_name="esta_activo")
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="fecha_de_orden")
    subtotal = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name="subtotal")
    total = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name="total")
    iva = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name="iva")

    def __str__(self):
        return f"Order {self.id} by {self.user}"
    
    # Método de dudosa funcionalidad
    # def calculateSubtotal(self):
    #     subtotal = 0
    #     for item in self.orderproduct_set.all:
    #         subtotal += item.product.price
    #     return subtotal
    
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="orden")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="producto")
    quantity = models.IntegerField(default=0, verbose_name="cantidad")

    def __str__(self):
        return f"{self.order} - {self.product}"