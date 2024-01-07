from django.db import models

# Create your models here.
class Mp3File(models.Model):
    original_file = models.FileField(upload_to='mp3_uploads/')
    modified_file = models.FileField(upload_to='modified_mp3/', blank=True)
    hidden_text = models.TextField()

