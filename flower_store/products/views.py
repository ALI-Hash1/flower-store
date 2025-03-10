from django.shortcuts import render
from django.views import View
from .models import Product
from django.shortcuts import get_object_or_404


class ProductDetailView(View):
    def get(self, request, slug_product):
        product = get_object_or_404(Product, slug=slug_product)
        return render(request, 'products/product.html', context={'product': product})
