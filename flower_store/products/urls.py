from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    path('all-products/', views.ShowAllProducts.as_view(), name='all_products'),
    path('reply/<int:product_id>/<int:comment_id>/', views.ProductReplyCommentView.as_view(), name='reply_comments'),
    path('<slug:slug_product>/', views.ProductDetailView.as_view(), name='detail_view'),
]
