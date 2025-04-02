from symtable import Class

from django.contrib import admin
from django.contrib.auth.models import User
from .models import (
    Product,
    Category,
    Customer,
    Order,
    Profile
)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']


class ProfileInline(admin.StackedInline):
    model = Profile


class CustomUserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    inlines = [ProfileInline]


# Register your models here.
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Profile)
