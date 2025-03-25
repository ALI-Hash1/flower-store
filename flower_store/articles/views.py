from django.shortcuts import render
from django.views import View


class ArticleView(View):
    def get(self, request, slug_article):
        pass

    def post(self, request, slug_article):
        pass
