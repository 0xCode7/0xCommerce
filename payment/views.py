from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from cart.cart import Cart
from payment.models import ShippingAddress, Order, OrderItem
from payment.forms import ShippingAddressForm, PaymentForm
from store.models import Profile

# Paypal
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid  # unique userid for duplicate orders


# Create your views here.

@login_required(login_url='authentication:login')
def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_products()
    if not cart_products:
        messages.error(request, 'Your cart is empty')
        return redirect('store:index')
    total_price = cart.get_total_price()

    shipping_address = ShippingAddress.objects.filter(user=request.user).first()
    if shipping_address:
        shipping_form = ShippingAddressForm(instance=shipping_address)
    else:
        shipping_form = ShippingAddressForm()

    context = {
        'cart_products': cart_products,
        'total_price': total_price,
        'shipping_form': shipping_form
    }
    return render(request, 'payment/checkout.html', context)


def info(request):
    if request.method == 'POST':
        cart = Cart(request)
        cart_products = cart.get_products()
        total_price = cart.get_total_price()

        shipping_form = request.POST

        request.session['shipping_form'] = shipping_form

        # Paypal
        host = request.get_host()
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': total_price,
            'item_name': '',
            'invoice': str(uuid.uuid4()),  # Unique invoice ID
            'currency_code': 'USD',
            'notify_url': 'http://{}{}'.format(host, "/paypal-ipn/"),
            'return': 'http://{}{}'.format(host, reverse('payment:success')),
            'cancel_return': 'http://{}{}'.format(host, reverse('payment:checkout')),
        }

        # Create the PayPal form
        paypal_form = PayPalPaymentsForm(initial=paypal_dict)
        context = {
            'cart_products': cart_products,
            'total_price': total_price,
            'shipping_form': shipping_form,
            'paypal_form': paypal_form,
        }
        return render(request, 'payment/info.html', context)
    else:
        messages.error(request, 'Access Denied')
        return redirect('store:index')


def process_order(request):
    if request.method == 'POST':
        cart = Cart(request)
        cart_products = cart.get_products()
        total_price = cart.get_total_price()
        payment_info = PaymentForm(request.POST or None)
        shipping_form = request.session.get('shipping_form')

        shipping_address = "\n".join(filter(None, [
            shipping_form.get("shipping_full_name", ""),
            shipping_form.get("shipping_email", ""),
            shipping_form.get("shipping_address1", ""),
            shipping_form.get("shipping_address2", ""),
            shipping_form.get("shipping_country", ""),
            shipping_form.get("shipping_state", ""),
            shipping_form.get("shipping_city", ""),
            shipping_form.get("shipping_zipcode", "")
        ]))

        # Process the order
        if request.user.is_authenticated:
            order = Order.objects.create(
                user=request.user,
                full_name=shipping_form.get("shipping_full_name", ""),
                email=shipping_form.get("shipping_email", ""),
                shipping_address=shipping_address,
                amount_paid=total_price
            )

            for product in cart_products:
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=product.quantity,
                    price=product.sale_price if product.is_sale else product.price,
                )
            # Clear the cart
            cart.clear()

            messages.success(request, 'Order was successful')
            return redirect('store:index')

        else:
            messages.error(request, 'Access Denied')
            return redirect('store:index')
    else:
        messages.error(request, 'Access Denied')
        return redirect('store:index')


def orders(request):
    context = {}
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.order_by('shipped').prefetch_related('order_items__product')

        for order in orders:
            for product in order.order_items.all():
                print(product.quantity)
        context = {
            'orders': orders,
        }
    else:
        messages.error(request, 'Access Denied')
        # return redirect('store:index')
    return render(request, 'payment/shipped_dashboard.html', context)


def order(request, id):
    order = Order.objects.get(pk=id)

    order.full_name = " ".join(order.full_name.split()[:2])
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        print(order_id)
        order = Order.objects.get(pk=order_id)

        order.shipped = not order.shipped
        order.save()

        if Order.shipped:
            messages.success(request, 'Order was shipped')
        else:
            messages.success(request, 'Order was not shipped')
        return redirect('payment:orders')

    return render(request, 'payment/order.html', {'order': order})
