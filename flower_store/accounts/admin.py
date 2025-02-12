from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from .models import User
from django.contrib.auth.models import Group


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('phone_number', 'is_admin')
    list_filter = ('is_admin',)
    ordering = ('email',)
    fieldsets = (
        ('User Information', {'fields': ('phone_number', 'password', 'last_login')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')})
    )
    add_fieldsets = (
        (None, {'fields': ('phone_number', 'email', 'password1', 'password2', 'is_admin')})
    )
    search_fields = ('email', 'phone_number')
    filter_horizontal = ()


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
