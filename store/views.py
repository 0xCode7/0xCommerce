from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib import messages
from unicodedata import category
from django.db.models import Q

from .models import (
    Product,
    Category
)


# Create your views here.
def index(request):
    category_name = request.GET.get('category')
    products = Product.objects.all().order_by('-is_sale')
    categories = Category.objects.filter(product__in=products).distinct()
    if category_name:
        category_name = category_name.replace('-', ' ')
        category = get_object_or_404(Category, name=category_name)
        products = products.filter(category=category)
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'store/index.html', context)


def about(request):
    categories = Category.objects.all()
    return render(request, 'store/about.html', {'categories': categories})


def product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product
    }
    return render(request, 'store/product.html', context)


def search(request):
    if request.method == 'POST':
        search = request.POST['search']
        context = {}
        results = Product.objects.filter(Q(name__icontains=search) | Q(description__icontains=search))
        if not results:
            messages.info(request, "Product Doesn't Exists...")
            return render(request, 'store/search.html')

        context['products'] = results
        return render(request, 'store/search.html', context)

    return render(request, 'store/search.html')
