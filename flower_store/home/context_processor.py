from django.conf import settings


def path_image_site(request):
    return {'host_name': f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/"}
