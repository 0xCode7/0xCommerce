from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('product/<int:product_id>/', views.product, name='product'),
    path('search', views.search, name='search'),

]
