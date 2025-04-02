from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from store.models import Profile, Product
from .forms import SignInForm, UpdateUserForm, UserInfoForm
from payment.forms import ShippingAddressForm
from payment.models import ShippingAddress
from cart.cart import Cart
import json


# Create your views here.
class LoginView(View):
    @staticmethod
    def get(request):
        context = {'auth_page': True}
        if request.user.is_authenticated:
            return redirect('store:index')
        return render(request, 'auth/login.html', context)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('expenses')

        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                user_profile = Profile.objects.get(user_id=user.id)
                if user_profile.cart:
                    user_cart = user_profile.cart
                    converted_cart = json.loads(user_cart)
                    cart = Cart(request)

                    for product_id, quantity in converted_cart.items():
                        product = Product.objects.get(pk=product_id)
                        cart.add(product, quantity)

                messages.success(request, 'Welcome, ' + user.first_name + '. You are now logged in')
                return redirect('store:index')
            else:
                messages.error(request, 'Invalid credentials, try again')
                return render(request, 'auth/login.html')
        else:
            messages.error(request, 'Please fill all fields')
            return render(request, 'auth/login.html')


class RegisterView(View):
    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            return redirect('store:index')
        context = {
            'auth_page': True
        }
        return render(request, 'auth/register.html', context)

    def post(self, request):
        form = SignInForm(request.POST)
        if form.is_valid():
            user = form.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            messages.success(request, 'Account created successfully')
            return redirect('authentication:login')
        else:
            if form.errors:
                first_error = list(form.errors.items())[0]
                field, error = first_error
                field = field.replace('_', ' ').capitalize()
                messages.error(request, error[0])
            else:
                messages.error(request, 'An error occurred during registration')
            return redirect('authentication:register')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('authentication:login')


class ProfileView(View):
    login_url = 'authentication:login'

    def get(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.id)
            profile = user.profile
            shipping_address = ShippingAddress.objects.get(user=user)
            form = UserInfoForm(instance=profile)

            shipping_form = ShippingAddressForm(instance=shipping_address)
            context = {
                'user': user,
                'form': form,
                'shipping_form': shipping_form
            }
            return render(request, 'auth/update-user.html', context)

        return redirect('authentication:login')

    def post(self, request):
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            try:
                password1 = form.cleaned_data.get('password1')
                password2 = form.cleaned_data.get('password2')
                if password1 != password2:
                    messages.error(request, 'Passwords do not match')
                    return redirect('authentication:profile')
                form.save()
                login(request, form.instance)
                messages.success(request, 'Profile updated successfully')
                return redirect('authentication:profile')
            except ValueError as e:
                messages.error(request, 'An error occurred during updating profile')
                print(e)
                return redirect('authentication:profile')
        else:
            messages.error(request, 'An error occurred during updating profile')
            return redirect('authentication:profile')


class UpdateInfoView(View):
    login_url = 'authentication:login'

    def post(self, request):
        form = UserInfoForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('authentication:profile')
        else:
            messages.error(request, 'An error occurred during updating profile')
            return redirect('authentication:update-info')


class UpdateShippingInfoView(View):
    login_url = 'authentication:login'

    def post(self, request):
        shipping_address = ShippingAddress.objects.get(user=request.user)
        form = ShippingAddressForm(request.POST, instance=shipping_address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('authentication:profile')
        else:
            messages.error(request, 'An error occurred during updating profile')
            return redirect('authentication:update-info')
