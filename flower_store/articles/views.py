from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from products.forms import CommentCreateForm
from django.shortcuts import get_object_or_404
from .models import Article
from products.models import Comment
from django.contrib import messages
from django.shortcuts import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class ArticleView(View):
    form_class = CommentCreateForm

    def setup(self, request, *args, **kwargs):
        self.article = get_object_or_404(Article, slug=kwargs['slug_article'])
        self.comments = self.article.article_comments.filter(is_reply=False)
        return super().setup(request, *args, **kwargs)

    def get(self, request, slug_article):
        return render(request, 'articles/article.html',
                      context={'article': self.article, 'comments': self.comments, 'form': self.form_class})

    @method_decorator(login_required)
    def post(self, request, slug_article):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.article = self.article
            new_comment.save()
            messages.success(request, 'your comment submitted successfully', 'success')
            return redirect(reverse('articles:article', args=(slug_article,)))
        return render(request, 'articles/article.html',
                      context={'article': self.article, 'comments': self.comments, 'form': self.form_class})


class ArticleReplyCommentView(LoginRequiredMixin, View):
    def post(self, request, article_id, comment_id):
        form_class = CommentCreateForm
        article = get_object_or_404(Article, id=article_id)
        comment = get_object_or_404(Comment, id=comment_id)
        all_comment = article.article_comments.filter(is_reply=False)
        form = form_class(request.POST)
        if form.is_valid():
            reply_comment = form.save(commit=False)
            reply_comment.user = request.user
            reply_comment.article = article
            reply_comment.reply = comment
            reply_comment.is_reply = True
            reply_comment.save()
            messages.success(request, 'پاسخ شما با موفقیت ثبت شد.', 'success')
            return redirect(reverse('articles:article', args=(article.slug,)))
        return render(request, 'articles/article.html',
                      context={'form': form, 'article': article, 'comments': all_comment})


class ShowArticlesView(View):
    def get(self, request):
        articles = Article.objects.all()
        paginator = Paginator(articles, 3)
        page = request.GET.get('page', 1)
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            # اگر شماره صفحه عددی نبود، صفحه اول را برگردانید
            articles = paginator.page(1)
        except EmptyPage:
            # اگر شماره صفحه خارج از محدوده بود، صفحه‌ی آخر را برگردانید
            articles = paginator.page(paginator.num_pages)
        return render(request, "articles/all-view-articles.html", context={'articles': articles, 'paginator': paginator})
