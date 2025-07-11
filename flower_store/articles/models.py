from django.utils import timezone
from django.db import models
from accounts.models import User
from django.utils.text import slugify
from utils import SEOMixin
from ckeditor.fields import RichTextField
from django.conf import settings
import wget


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
        ('draft', 'draft storage'),
        ('published', 'publish'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    thumbnail = models.ImageField(blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    allow_comments = models.BooleanField(default=True)

    def save(self, *args, **kwargs):

        if self.pk:

            old_instance = self.__class__.objects.get(pk=self.pk)

            if old_instance.thumbnail == self.thumbnail.name:

                path = '/home/ali/flower-store/flower_store/media-files'
                download_path = f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{str(self.thumbnail)}"

                try:
                    wget.download(download_path, out=path)
                    print("download the file was successfully done!")
                except Exception as e:
                    print("there was a problem with downloading the file!", e)

        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['-publish_date']

    def __str__(self):
        return self.title


class Category(SEOMixin, models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
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
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
