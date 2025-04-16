from django.utils import timezone
from django.db import models
from accounts.models import User
from django.utils.text import slugify
from utils import SEOMixin
from ckeditor.fields import RichTextField


class Article(SEOMixin, models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_articles')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, verbose_name="دسته‌بندی")
    tags = models.ManyToManyField('Tag', blank=True, verbose_name="تگ ‌ها")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = RichTextField()
    publish_date = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    STATUS_CHOICES = [
        ('draft', 'پیش‌ نویس'),
        ('published', 'منتشر شده'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    thumbnail = models.ImageField(upload_to='articles-thumbnails/', blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    allow_comments = models.BooleanField(default=True)

    class Meta:
        ordering = ['-publish_date']
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"

    def __str__(self):
        return self.title


class Category(SEOMixin, models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(SEOMixin, models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "تگ"
        verbose_name_plural = "تگ‌ ها"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
