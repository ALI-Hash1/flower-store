from django.db.models.signals import post_save
from django.dispatch import receiver
from home.tasks import upload_object_task
from .models import Article
import os


@receiver(post_save, sender=Article)
def upload_article_image(sender, **kwargs):
    if kwargs['created'] and kwargs['instance'].thumbnail:
        image_name = kwargs['instance'].thumbnail.path
        is_upload = upload_object_task(image_name, f'article-images/{kwargs["instance"].thumbnail.name}')
        if is_upload:
            os.remove(image_name)
