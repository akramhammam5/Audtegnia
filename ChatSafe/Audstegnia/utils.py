import os
import wave

def embed_audio_message(audiofile, secretmsg, outputfile):
    try:
        waveaudio = wave.open(audiofile, mode='rb')
        frame_bytes = bytearray(list(waveaudio.readframes(waveaudio.getnframes())))
        secretmsg = secretmsg + int((len(frame_bytes)-(len(secretmsg)*8*8))/8) *'#'
        bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in secretmsg])))
        for i, bit in enumerate(bits):
            frame_bytes[i] = (frame_bytes[i] & 254) | bit
        frame_modified = bytes(frame_bytes)
        with wave.open(outputfile, 'wb') as fd:
            fd.setparams(waveaudio.getparams())
            fd.writeframes(frame_modified)
        waveaudio.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

