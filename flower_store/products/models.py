from django.db import models
from accounts.models import User
from django.core.validators import MaxValueValidator
from utils import SEOMixin
from articles.models import Article
from django.conf import settings
import wget


class Product(SEOMixin, models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    available = models.BooleanField(default=True)
    image = models.ImageField()
    price = models.PositiveIntegerField()
    slug = models.SlugField(max_length=255, unique=True)
    minimum_height = models.PositiveSmallIntegerField(blank=True, null=True)
    vase_description = models.TextField()

    DIFFICULTY_CHOICES = (
        ('easy', 'آسان'),
        ('medium', 'متوسط'),
        ('hard', 'سخت'),
    )

    maintenance_level = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)

    def save(self, *args, **kwargs):

        if self.pk:

            old_instance = self.__class__.objects.get(pk=self.pk)

            if old_instance.image == self.image.name:

                path = '/home/ali/flower-store/flower_store/media-files'
                download_path = f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{str(self.image)}"

                try:
                    wget.download(download_path, out=path)
                    print("download the file was successfully done!")
                except Exception as e:
                    print("there was a problem with downloading the file!", e)

        return super().save(*args, **kwargs)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(SEOMixin, models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_comments', blank=True,
                                null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_comments', blank=True,
                                null=True)
    reply = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='answers_comment', blank=True,
                              null=True)
    is_reply = models.BooleanField(default=False)
    author_name = models.CharField(max_length=255)
    comment_text = models.TextField()
    created = models.DateField(auto_now_add=True)
    admin_confirmation = models.BooleanField(default=False)

    def __str__(self):
        if self.product:
            return f'Review by {self.user.phone_number} for {self.product.name}'
        elif self.article:
            return f'Review by {self.user.phone_number} for {self.article.title}'
