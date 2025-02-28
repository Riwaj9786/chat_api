from django.db import models

from core.utils import generate_unique_slug

from accounts.models import User
from core.models import TimeStampedModel

class ChatRoom(TimeStampedModel):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, blank=True, related_name='chat_members')
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, related_name='room_creator')
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self.name)

        super().save(*args, **kwargs)
    

class Message(TimeStampedModel):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='room_messages')
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='message_sender')
    message = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.sender}: {self.created_at}"
