from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    path('<slug:slug_product>/', views.ProductDetailView.as_view(), name='detail_view'),
    path('reply/<int:product_id>/<int:comment_id>/', views.ProductReplyCommentView.as_view(), name='reply_comments'),
]
