from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatMessage(models.Model):
    message = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now=False, auto_created=True, auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    # TODO: Move this to different Table
    is_read = models.BooleanField(default=False)
