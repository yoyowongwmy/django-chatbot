from django.db import models
# Create your models here.

class Thread(models.Model):
    role = models.CharField(max_length=50)
    content = models.TextField(max_length=225)

class ChatSession(models.Model):
    session_id = models.CharField(max_length=255, unique=True)  # Unique session ID
    conversation = models.JSONField(default=list)  # Store conversation as a list of dictionaries

    def __str__(self):
        return f"{self.session_id}: {self.conversation}"
