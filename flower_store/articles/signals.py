from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from home.tasks import upload_object_task, delete_object_task
from .models import Article
from django.conf import settings
import os


@receiver(post_save, sender=Article)
def upload_article_image(sender, instance, created, **kwargs):
    if instance.thumbnail:
        if not created:
            key = instance.thumbnail.name
            if instance.old_thumbnail != key:
                delete_key = instance.old_thumbnail
                delete_object_task(str(delete_key))

        thumbnail_name = instance.thumbnail.path
        key = f'{instance.thumbnail.name}'
        is_upload = upload_object_task(thumbnail_name, key)
        if is_upload:
            os.remove(thumbnail_name)
            instance.thumbnail = f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{key}"


@receiver(pre_save, sender=Article)
def handle_product_image_change(sender, instance, **kwargs):
    if instance.id in [p.id for p in Article.objects.all()]:
        instance.old_thumbnail = Article.objects.get(id=instance.id).thumbnail
