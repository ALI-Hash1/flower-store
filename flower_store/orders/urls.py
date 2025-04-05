from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('', views.CartView.as_view(), name='cart'),
    path('add/<int:product_id>/', views.CartAddView.as_view(), name='cart_add'),
    path('remove/<int:product_id>/', views.CartRemoveView.as_view(), name='cart_remove'),
    path('create_order/', views.CreateOrderView.as_view(), name='order_create'),
    path('order_detail/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('pay/<int:order_id>/', views.OrderPayView.as_view(), name='order_pay'),
    path('verify/', views.OrderPayVerifyView.as_view(), name='order_verify'),
    path('orders/', views.OrderView.as_view(), name='order_list'),
]
