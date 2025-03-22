from django.contrib import admin
from .models import Article, Category, Tag

models = (Article, Category, Tag)

for model in models:
    admin.site.register(model)
