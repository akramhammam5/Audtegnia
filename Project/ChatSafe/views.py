# steganography/views.py
import os
from django.shortcuts import render
from django.http import HttpResponse
from .forms import AudioWatermarkForm
from pydub import AudioSegment

def hide_text_lsb(audio, text):
    # Convert text to binary representation
    binary_text = ''.join(format(ord(char), '08b') for char in text)

    # Get the raw audio data as a bytearray
    audio_data = bytearray(audio.raw_data)

    # Iterate over the binary text and modify the audio LSB
    for i, bit in enumerate(binary_text):
        index = i * audio.sample_width

        # Clear the least significant bit
        audio_data[index] &= 0b11111110

        # Set the LSB to the bit from the binary text
        audio_data[index] |= int(bit)

    # Create a new AudioSegment using the modified data
    audio_hidden = audio._spawn(audio_data)

    return audio_hidden

def index(request):
    if request.method == 'POST':
        form = AudioWatermarkForm(request.POST, request.FILES)
        if form.is_valid():
            # Extract data from the form
            text_input = form.cleaned_data['text_input']
            audio_file = request.FILES['audio_file']

            # Load the original audio file
            audio = AudioSegment.from_mp3(audio_file.temporary_file_path())

            # Perform LSB steganography
            audio_hidden = hide_text_lsb(audio, text_input)

            # Specify the output path
            output_path = os.path.join('media', 'output_hidden.mp3')

            # Save the modified audio file using LAME (mp3 codec)
            audio_hidden.export(output_path, format="mp3", codec="libmp3lame")

            # Provide the link to the modified file
            return HttpResponse(f'<a href="{output_path}" download>Download Stegged Audio</a>')

    else:
        form = AudioWatermarkForm()

    return render(request, 'index.html', {'form': form})

