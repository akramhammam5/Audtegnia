from django.db import models
from django.contrib.auth.models import User


class AudioMessage(models.Model):
    audio_file = models.FileField(upload_to='audio_messages')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.audio_file.name
        
class Chat(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')
    users = models.ManyToManyField(User, related_name='users', blank=False)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-created"]
    
    

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.body
    
    class Meta:
        ordering = ["-created"]

