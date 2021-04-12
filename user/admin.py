from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from user.models import User
from django.contrib.auth.models import Group
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        ('Login Credential', {'fields': ('email', 'password')}),
        ('Profile', {'fields': ('first_name', 'last_name', 'avatar', 'is_active', 'is_superuser')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'avatar', 'is_superuser', 'is_staff'),
        }),
    )
    readonly_fields = ('width', 'height')
    list_filter = ()
    filter_horizontal = ()
    search_fields = ('email',)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_superuser', 'is_active')

admin.site.unregister(Group)