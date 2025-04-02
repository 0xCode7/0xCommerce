from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.core.serializers import serialize
from django.contrib import messages
import json
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='authentication:login')
def summary(request):
    cart = Cart(request)
    cart_products = cart.get_products()
    if not cart_products:
        messages.error(request, 'Your cart is empty')
        return redirect('store:index')
    total_price = cart.get_total_price()

    context = {
        'cart_products': cart_products,
        'total_price': total_price,
    }
    return render(request, 'cart/summary.html', context)


@login_required(login_url='authentication:login')
def add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_quantity = str(request.POST.get('product_quantity'))
        product = get_object_or_404(Product, id=product_id)

        # Save to session
        cart.add(product=product, quantity=product_quantity)
        cart_quantity = cart.__len__()

        product_data = serialize('json', [product])
        product_data = json.loads(product_data)[0]['fields']
        product_data['id'] = product_id
        response = JsonResponse({
            'product': product_data,
            'cart_quantity': cart_quantity,
        })

        messages.success(request, 'Item Added Successfully')

        return response


@login_required(login_url='authentication:login')
def update(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = int(request.POST.get('product_id'))
        product_quantity = str(request.POST.get('quantity'))

        # Update Cart
        cart.update(product_id=product_id, quantity=product_quantity)
        total_price = cart.get_total_price()
        response = JsonResponse({
            'quantity': product_quantity,
            'total': total_price,
        })

        return response


@login_required(login_url='authentication:login')
def delete(request, id):
    cart = Cart(request)

    product_id = id

    cart.delete(product_id=product_id)
    messages.error(request, 'Item Deleted Successfully')

    return redirect('cart:summary')
