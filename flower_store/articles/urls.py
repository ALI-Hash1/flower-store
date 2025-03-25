from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    path('<slug:slug_article>/', views.ArticleView.as_view(), name='article'),
]
