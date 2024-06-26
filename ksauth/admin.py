from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username','email', 'password')}),
        ('Personal info', {'fields': ('first_name','phone_number', 'user_ratings')}),
        ('Admin Status', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('User groups and permissions', {'fields': ('groups', 'user_permissions',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)

# Unregister the provided model admin
from django.contrib.auth.models import Group
admin.site.unregister(User)
admin.site.unregister(Group)

# Re-register UserAdmin
admin.site.register(User, UserAdmin)
admin.site.register(Group)