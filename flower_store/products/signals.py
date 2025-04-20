from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from home.tasks import upload_object_task, delete_object_task
from .models import Product
from django.conf import settings
import os


@receiver(post_save, sender=Product)
def upload_product_image(sender, instance, created, **kwargs):
    if instance.image:
        if not created:
            key = instance.image.name
            if instance.old_image != key:
                delete_key = instance.old_image
                delete_object_task(str(delete_key))

        image_name = instance.image.path
        key = f'{instance.image.name}'
        is_upload = upload_object_task(image_name, key)
        if is_upload:
            os.remove(image_name)
            instance.image = f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{key}"


@receiver(pre_save, sender=Product)
def handle_product_image_change(sender, instance, **kwargs):
    if instance.id in [p.id for p in Product.objects.all()]:
        instance.old_image = Product.objects.get(id=instance.id).image
