# audiowatermark/forms.py
from django import forms

class AudioWatermarkForm(forms.Form):
    text_input = forms.CharField(label='Text Input', max_length=100)
    audio_file = forms.FileField(label='MP3 File')
