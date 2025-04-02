from django.urls import path
from . import views

app_name = 'payment'
urlpatterns = [
    path("checkout/", views.checkout, name='checkout'),
    path("info/", views.info, name="info"),
    path("success/", views.process_order, name='success'),
    path("orders/", views.orders, name='orders'),
    path("order/<int:id>", views.order, name='order_details')
]
