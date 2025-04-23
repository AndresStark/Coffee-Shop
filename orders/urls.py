from django.urls import path

from .views import CreateOrderProductView, RemoveOrderProductView, MyOrderView

urlpatterns = [
    path("mi-orden", MyOrderView.as_view(), name="my_order"),
    path("agregar-producto", CreateOrderProductView.as_view(), name="add_product"),
    path("eliminar-producto/(?P<pk>\d+)", RemoveOrderProductView.as_view(), name="remove_product"),
]