from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet


key = Fernet.generate_key()
cipher_suite = Fernet(key)

def encrypt_message(message):
    encrypted_message = cipher_suite.encrypt(message.encode())
    return encrypted_message

def decrypt_message(encrypted_message):
    decrypted_message = cipher_suite.decrypt(encrypted_message)
    return decrypted_message.decode()


class VoiceNote(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_voice_notes')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_voice_notes')
    title = models.CharField(max_length=100,default="Untitled")
    audio_file = models.FileField(upload_to='voice_notes/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Voice note from {self.sender} to {self.recipient} at {self.created_at}"

    def get_common_chat_users(self):
        # Get the chat instance where both sender and recipient are participants
        sender_chat = Chat.objects.filter(users=self.sender)
        recipient_chat = Chat.objects.filter(users=self.recipient)
        common_users = sender_chat.filter(users=self.recipient)
        return common_users
        
class Chat(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')
    users = models.ManyToManyField(User, related_name='users', blank=False)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-created"]
    
    

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) ->str:
        return self.body
    
    class Meta:
        ordering = ["-created"]

