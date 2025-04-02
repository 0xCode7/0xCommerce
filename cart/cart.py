from django.template.context_processors import request

from store.models import Product, Profile


class Cart():
    def __init__(self, request):
        self.session = request.session
        self.request = request

        # Get the current session key if it exists
        cart = self.session.get('session_key')

        # If the session key does not exist, create a new session key
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        #  Make the cart is available on all views
        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        try:
            quantity = int(quantity)
        except ValueError:
            raise ValueError(f"Invalid quantity value: {quantity}")

        if product_id in self.cart:
            self.cart[product_id] += int(quantity)
        else:
            self.cart[product_id] = int(quantity)
        self.session.modified = True

        if self.request.user.is_authenticated:
            user_profile = Profile.objects.get(user=self.request.user)
            current_cart = str(self.cart)

            user_profile.cart = current_cart.replace("\'", '\"')

            user_profile.save()

    def remove(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True

    def __len__(self):
        return len(self.cart)

    def get_products(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            product.quantity = self.cart[str(product.id)]

        return products

    def get_total_price(self):
        products_ids = self.cart.keys()
        products = Product.objects.filter(id__in=products_ids)

        cartProducts = self.cart
        total = 0

        for key, value in cartProducts.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total += (product.sale_price * value)
                    else:
                        total += (product.price * value)

        return total

    def update(self, product_id, quantity):
        product_id = str(product_id)
        quantity = int(quantity)

        cart = self.cart

        cart[product_id] = quantity

        self.session.modified = True
        if self.request.user.is_authenticated:
            user_profile = Profile.objects.get(user=self.request.user)
            current_cart = str(self.cart)

            user_profile.cart = current_cart.replace("\'", '\"')
            user_profile.save()

        return self.cart

    def delete(self, product_id):
        product_id = str(product_id)

        cart = self.cart

        cart.pop(product_id)
        self.session.modified = True

        if self.request.user.is_authenticated:
            user_profile = Profile.objects.get(user=self.request.user)
            current_cart = str(self.cart)

            user_profile.cart = current_cart.replace("\'", '\"')
            user_profile.save()
        return self.cart

    def clear(self):
        self.cart.clear()
        self.session.modified = True

        if self.request.user.is_authenticated:
            user_profile = Profile.objects.get(user=self.request.user)
            user_profile.cart = "{}"
            user_profile.save()
