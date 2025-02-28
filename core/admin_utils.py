from django.utils.html import format_html

def avatar_small_preview(obj):
    if obj.avatar:
        return format_html(
            '<img src="{}" style="height: 50px; width:50px; border-radius: 50%; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">',
            obj.avatar.url
        )
    return "No Image"

def avatar_large_preview(obj):
    if obj.avatar:
        return format_html(
            '<img src="{}" style="height: 200px; width:200px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">',
            obj.avatar.url
        )
    return "No Image"