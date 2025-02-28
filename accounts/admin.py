from django.contrib import admin
from accounts.models import User

from core.admin_utils import avatar_small_preview, avatar_large_preview

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'avatar_preview', 'name', 'is_active', 'is_staff', 'is_superuser')
    list_display_links = list_display
    readonly_fields = ('email', 'name', 'avatar', 'last_login', 'avatar_large_preview', 'created_at', 'updated_at')
    exclude = ('password', 'user_permissions', 'groups')

    fieldsets = (
        ('Personal Information', {
            'fields': ('email', 'name', 'is_active', 'is_staff', 'is_superuser')
        }),
        ('Media', {
            'fields': ('avatar_large_preview',)
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at', 'last_login')
        }),
    )

    def avatar_preview(self, obj):
        return avatar_small_preview(obj)
    avatar_preview.short_description = "Avatar"

    def avatar_large_preview(self, obj):
        return avatar_large_preview(obj)
    avatar_large_preview.short_description = "Avatar Preview"
    