#models.py
from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
import base64
import hashlib

class VoiceNote(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_voice_notes')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_voice_notes')
    title = models.CharField(max_length=100, default="Untitled")
    audio_file = models.FileField(upload_to='voice_notes/', null=True, blank=True)  # Save file path in database
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Voice note from {self.sender} to {self.recipient} at {self.created_at}"


class Password(models.Model):
    password = models.CharField(max_length=255)
        
class Chat(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_with_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_with_user2')
    users = models.ManyToManyField(User, related_name='users', blank=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]
        
    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super(Chat, self).save(*args, **kwargs)
        if is_new:
            ChatKey.objects.create(chat=self)
    
class ChatKey(models.Model):
    chat = models.OneToOneField(Chat, on_delete=models.CASCADE, related_name='chat_key')
    key = models.CharField(max_length=100, blank=True)
    key_hash = models.CharField(max_length=256, blank=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = Fernet.generate_key().decode('utf-8')
            self.key_hash = hashlib.sha256(self.key.encode()).hexdigest()
        super(ChatKey, self).save(*args, **kwargs)
    

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    body = models.TextField(blank=True, null=True)  # Allow empty messages for when there's only an audio file
    audio_file = models.FileField(upload_to='messages/', null=True, blank=True)  # Optional field for audio messages
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {'Audio Message' if self.audio_file else self.body}"

    class Meta:
        ordering = ["-created"]
