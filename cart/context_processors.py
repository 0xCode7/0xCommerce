from .cart import Cart


#  Create a context processor to make the cart available on all views
def cart(request):
    cart = Cart(request)
    return {'cart': cart}
