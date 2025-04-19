from django.urls import path, include
from . import views

app_name = 'home'

bucket_urls = [
    path('', views.BucketView.as_view(), name='bucket'),
    path('delete_object/<key>/', views.DeleteBucketObjectView.as_view(), name='delete_object_bucket'),
    path('download_object/<key>/', views.DownloadBucketObjectView.as_view(), name='download_object_bucket'),
]

urlpatterns = [
    path('', views.HomeView.as_view(), name='home_page'),
    path('bucket/', include(bucket_urls)),
]
