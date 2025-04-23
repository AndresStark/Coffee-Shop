from decimal import ROUND_HALF_EVEN, Decimal
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, DeleteView

from .forms import OrderProductForm
from .models import Order, OrderProduct

class MyOrderView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "orders/my_order.html"
    context_object_name = "order"

    def get_object(self, queryset = None):
        # Llamado del pedido del usuario actual si está activo
        order = Order.objects.filter(user=self.request.user, is_active=True).first()

        # Reseteo de variables para ser recalculadas al recargar la página
        order.subtotal = 0
        order.iva = 0
        order.total = 0

        # Cálculo del subtotal
        for item in order.orderproduct_set.all():
            order.subtotal += item.product.price
        
        # Asignación de datos relevantes
        order.iva = (order.subtotal * Decimal(0.13)).quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN) #IVA de El Salvador: 13%
        order.total = (order.subtotal * Decimal(1.13)).quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN)

        # Actualización de datos en la base de datos
        order.save()
        return order
    
class CreateOrderProductView(LoginRequiredMixin, CreateView):
    template_name = "orders/create_order_product.html"
    form_class = OrderProductForm
    success_url = reverse_lazy('my_order')

    def form_valid(self, form):
        order, _ = Order.objects.get_or_create(
            is_active=True,
            user=self.request.user,
        )
        form.instance.order = order
        form.instance.quantity = 1
        form.save()
        return super().form_valid(form)
        
class RemoveOrderProductView(DeleteView):
    template_name = "orders/remove_order_product.html"
    model = OrderProduct
    success_url = reverse_lazy('my_order')