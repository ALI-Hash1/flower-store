from django.shortcuts import render, redirect
from django.views import View
from . import tasks
from django.contrib import messages
from products.models import Product
from articles.models import Article


class HomeView(View):
    template_name = 'home/home.html'

    def get(self, request):
        product1, product2, product3 = Product.objects.all()[:3]
        articles = Article.objects.all()[:3]
        return render(request, self.template_name,
                      context={'product1': product1, 'product2': product2, 'product3': product3, 'articles': articles})


class BucketView(View):
    template = 'home/bucket.html'

    def get(self, request):
        objects = tasks.all_bucket_objects_task()
        return render(request, self.template, {"objects": objects})


class DeleteBucketObjectView(View):
    def get(self, request, key):
        tasks.delete_object_task.delay(key)
        messages.success(request, 'the file was successfully deleted from the bucket', 'info')
        return redirect("home:bucket")


class DownloadBucketObjectView(View):
    def get(self, request, key):
        tasks.download_object_task.delay(key)
        messages.success(request, "the file was successfully downloaded from the bucket", "success")
        return redirect('home:bucket')
