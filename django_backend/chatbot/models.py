from django.db import models

# Create your models here.


class ChatSession(models.Model):
    session_id = models.CharField(max_length=255, unique=True)  # Unique session ID
    created = models.DateTimeField(auto_now_add=True)
    conversation = models.JSONField(
        default=list
    )  # Store conversation as a list of dictionaries

    def __str__(self):
        return f"{self.session_id}: {self.conversation}"
