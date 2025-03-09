from django.contrib import admin
from .models import Product, Category, Comment, DiscountCode


new_models = [Product, Category, Comment, DiscountCode]

for model in new_models:
    admin.site.register(model)
