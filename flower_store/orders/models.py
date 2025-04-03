from django.db import models
from accounts.models import User
from products.models import Product
from django.core.validators import MaxValueValidator


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('paid', '-updated')

    def __str__(self):
        return f'{self.user} - {self.id}'

    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveSmallIntegerField(default=1, validators=(MaxValueValidator(20),))

    def __str__(self):
        return f'there is {self.product.name} in order with {self.order.id} id'

    def get_cost(self):
        return self.product.price * self.quantity
