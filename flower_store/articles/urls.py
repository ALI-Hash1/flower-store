from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    path('all_articles/', views.ShowArticlesView.as_view(), name='all_articles'),
    path('<slug:slug_article>/', views.ArticleView.as_view(), name='article'),
    path('reply/<int:article_id>/<int:comment_id>/', views.ArticleReplyCommentView.as_view(), name='reply_comments'),
]
