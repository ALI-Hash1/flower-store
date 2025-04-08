from django.contrib import admin
from .models import Product, Category, Comment
from django.utils.html import format_html

new_models = [Product, Category]

for model in new_models:
    admin.site.register(model)


class ConfirmationStatusFilter(admin.SimpleListFilter):
    title = 'comment situation'  # عنوانی که در پنل ادمین نمایش داده می‌شود
    parameter_name = 'confirmation_status'  # پارامتر مورد استفاده در URL

    def lookups(self, request, model_admin):
        # تعریف گزینه‌های فیلتر
        return (
            ('accepted', 'کامنت‌های تاییدشده ✅'),
            ('not_reviewed', 'کامنت‌های بررسی‌نشده ⚠️'),
        )

    def queryset(self, request, queryset):
        # فیلتر کردن بر اساس انتخاب کاربر
        if self.value() == 'accepted':
            return queryset.filter(admin_confirmation=True)
        if self.value() == 'not_reviewed':
            return queryset.filter(admin_confirmation=False)
        return queryset  # اگر هیچ فیلتری انتخاب نشده، همه کامنت‌ها نمایش داده می‌شوند


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_filter = (ConfirmationStatusFilter,)


