from django.shortcuts import render, redirect
from django.views import View
from . import tasks
from django.contrib import messages


class HomeView(View):
    template_name = 'home/home.html'

    def get(self, request):
        return render(request, self.template_name)


class BucketView(View):
    template = 'home/bucket.html'

    def get(self, request):
        objects = tasks.all_bucket_objects_task()
        return render(request, self.template, {"objects": objects})


class DeleteBucketObjectView(View):
    def get(self, request, key):
        tasks.delete_object_task.delay(key)
        messages.success(request, 'فایل از باکت با موفقیت حذف شد', 'info')
        return redirect("home:bucket")


class DownloadBucketObjectView(View):
    def get(self, request, key):
        tasks.download_object_task.delay(key)
        messages.success(request, "فایل با موفقیت دانلود شد", "success")
        return redirect('home:bucket')
