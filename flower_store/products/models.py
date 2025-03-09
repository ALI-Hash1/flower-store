from django.db import models
from accounts.models import User
from django.core.validators import MaxValueValidator


class Product(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='image-products/')
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

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_comments')
    reply = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='answers_comment', blank=True,
                              null=True)
    is_reply = models.BooleanField(default=False)
    author_name = models.CharField(max_length=255)
    comment_text = models.TextField()
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.email} for {self.product.name}'


class DiscountCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.PositiveSmallIntegerField(MaxValueValidator(100))
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
