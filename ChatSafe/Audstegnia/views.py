from django.shortcuts import render
from django.http import HttpResponse
from .utils import embed_audio_message

def form_template_view(request):
    if request.method == 'POST':
        audiofile = request.FILES['file']
        secretmsg = request.POST['text']
        outputfile = '/home/elliot/Documents/Grad/Implementation/Virtual/ChatSafe/audio/output.wav'

        success = embed_audio_message(audiofile, secretmsg, outputfile)

        if success:
                return render(request, 'success.html', {'outputfile': outputfile})
        else:
                return render(request, 'error.html')
    return render(request, 'index.html')

