from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('', views.summary, name='summary'),
    path('add/', views.add, name='add'),
    path('update/', views.update, name='update'),
    path('delete/<int:id>', views.delete, name='delete'),

]
