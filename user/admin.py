from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from user.models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        ('Login Credential', {'fields': ('email', 'password')}),
        ('Profile', {'fields': ('first_name', 'last_name', 'avatar')}))

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'avatar', 'is_superuser', 'is_staff'),
        }),
    )
    readonly_fields = ('width', 'height')
    list_filter = ()
    filter_horizontal = ()
    search_fields = ('email', )