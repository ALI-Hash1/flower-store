from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from .models import User, OtpCode
from django.contrib.auth.models import Group


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('phone_number', 'is_admin')
    list_filter = ('is_admin',)
    ordering = ('email',)
    fieldsets = (
        ('User Information', {'fields': ('phone_number', 'password', 'last_login', 'email')}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'groups', 'user_permissions', 'is_superuser')})
    )
    add_fieldsets = (
        ('Add User', {'fields': ('phone_number', 'password1', 'password2')}),
        ('Email', {'fields': ('email',)})
    )
    search_fields = ('email', 'phone_number')
    filter_horizontal = ('groups', 'user_permissions')
    readonly_fields = ('last_login', )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields['is_superuser'].disabled = True
        return form


admin.site.register(User, UserAdmin)
admin.site.register(OtpCode)