# myapp/forms.py
from django import forms
from django.contrib.auth.models import User

class EditUsernameForm(forms.ModelForm):
    username = forms.CharField(label='New Username', max_length=150)

    class Meta:
        model = User
        fields = ['username']


class PasswordResetForm(forms.Form):
    email = forms.EmailField()
