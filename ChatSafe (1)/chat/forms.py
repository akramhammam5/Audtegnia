# myapp/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import VoiceNote

class EditUsernameForm(forms.ModelForm):
    username = forms.CharField(label='New Username', max_length=150)

    class Meta:
        model = User
        fields = ['username']


class PasswordResetForm(forms.Form):
    email = forms.EmailField()
    



class VoiceNoteForm(forms.ModelForm):
    class Meta:
        model = VoiceNote
        fields = ['recipient', 'audio_file']

