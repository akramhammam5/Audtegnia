from django.shortcuts import render
from django.http import HttpResponse
from .utils import *
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from base64 import b64encode, b64decode

encryption_key = "mysecretkey"




def hide(request):
    if request.method == 'POST':
        audiofile = request.FILES.get('file')
        secretmsg = request.POST.get('text')
        outputfile = '/home/elliot/Documents/Grad/Implementation/Virtual/ChatSafe/audio/output.wav'
        
        if audiofile and secretmsg and outputfile:
            try:
                em_audio(audiofile, secretmsg, outputfile)
                return render(request, 'success.html')
            except Exception as e:
                return render(request, 'error.html', {'error_message': f"Error embedding message: {str(e)}"})
    
    return render(request, 'index.html')

def extract(request):
    if request.method == 'POST':
        audiofile = request.FILES.get('file')
        if audiofile:
            try:
                extracted_message = ex_msg(audiofile)
                return render(request, 'extracted_message.html', {'secret_message': decrypted})
            except Exception as e:
                return render(request, 'error.html', {'error_message': f"Error extracting message: {str(e)}"})
    
    return render(request, 'Decode.html')

