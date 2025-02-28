from django.contrib import admin

from chat.models import ChatRoom, Message


class MembersInline(admin.TabularInline):
    model = ChatRoom.members.through
    extra=0
    can_delete=False
    verbose_name = "Member"
    readonly_fields = ('user',)
    

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at')
    list_display_links = list_display
    exclude = ('members',)
    readonly_fields = ('slug', 'created_by')
    inlines = (MembersInline,)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('room', 'sender', 'message', 'created_at')
    list_display_links = list_display
    ordering = ('-created_at',)