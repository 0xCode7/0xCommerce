from django.urls import path
from .views import (
    LoginView,
    RegisterView,
    LogoutView,
    ProfileView,
    UpdateInfoView,
    UpdateShippingInfoView
)

app_name = 'authentication'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/info', UpdateInfoView.as_view(), name='update-info'),
    path('profile/shipping', UpdateShippingInfoView.as_view(), name='update-shipping'),

]
