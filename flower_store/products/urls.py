from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    path('<slug:slug_product>/', views.ProductDetailView.as_view(), name='detail_view'),
]
