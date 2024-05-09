#utils.py
import os
import wave
import argparse
from Crypto.Cipher import AES
from cryptography.fernet import Fernet, InvalidToken
import logging
from .models import ChatKey
import base64



def checkFlip(data,a,b):
	store = data & 12
	if store == 0 and (a == 0 and b == 0):
		return data
	elif store == 4 and (a == 0 and b == 1):
		return data
	elif store == 8 and (a == 1 and b == 0):
		return data
	elif store == 12 and (a == 1 and b == 1):
		return data
	else:
		return data ^ 3


def em_audio(af, string, output):
    waveaudio = wave.open(af, mode='rb')
    frame_bytes = bytearray(list(waveaudio.readframes(waveaudio.getnframes())))
    string = string + int(((2*len(frame_bytes))-(len(string)*8*8))/8) *'#'
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in string])))
    j = 0
    for i in range(0,len(frame_bytes),2):
        a = bits[i]
        b = bits[i+1]
        frame_bytes[j] = checkFlip(frame_bytes[j],a,b)
        frame_bytes[j] = frame_bytes[j] & 243
        if a==0 and b==1:
            frame_bytes[j] = frame_bytes[j] + 4
        elif a==1 and b==0:
            frame_bytes[j] = frame_bytes[j] + 8
        elif a==1 and b==1:
            frame_bytes[j] = frame_bytes[j] + 12
        j = j + 1
    frame_modified = bytes(frame_bytes)
    newAudio = wave.open(output, 'wb')
    newAudio.setparams(waveaudio.getparams())
    newAudio.writeframes(frame_modified)

    newAudio.close()
    waveaudio.close()




def ex_msg(af):
    waveaudio = wave.open(af, mode='rb')
    frame_bytes = bytearray(list(waveaudio.readframes(waveaudio.getnframes())))
    extracted = []
    for i in range(len(frame_bytes)):
        frame_bytes[i] = frame_bytes[i] & 12
        if frame_bytes[i] == 0:
            extracted.append(0)
            extracted.append(0)
        elif frame_bytes[i] == 4:
            extracted.append(0)    
            extracted.append(1) 
        elif frame_bytes[i] == 8:
            extracted.append(1)
            extracted.append(0)
        elif frame_bytes[i] == 12:
            extracted.append(1)
            extracted.append(1)
    string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
    decoded = string.split("###")[0]
    waveaudio.close()
    return decoded
 


def encrypt_message(message, chat):
    chat_key = ChatKey.objects.get(chat=chat)
    print(f"Encryption key: {chat_key.key}")  # Debug: Print encryption key
    cipher_suite = Fernet(chat_key.key.encode())
    encrypted_data = cipher_suite.encrypt(message.encode())
    encoded_data = base64.b64encode(encrypted_data).decode()  # Convert binary data to base64 encoded string
    print(f"Encrypted message (ciphertext): {encoded_data}")  # Debug: Print ciphertext after encryption
    return encoded_data

def decrypt_message(encrypted_message, chat):
    chat_key = ChatKey.objects.get(chat=chat)
    print(f"Decryption key: {chat_key.key}")  # Debug: Print decryption key
    print(f"Encrypted message to decrypt (ciphertext): {encrypted_message}")  # Debug: Print ciphertext before decryption
    cipher_suite = Fernet(chat_key.key.encode())
    try:
        decoded_data = base64.b64decode(encrypted_message.encode())  # Convert base64 encoded string back to binary
        decrypted_data = cipher_suite.decrypt(decoded_data).decode()
        print(f"Decrypted message (plaintext): {decrypted_data}")  # Debug: Print plaintext after decryption
        return decrypted_data
    except InvalidToken:
        return "<Invalid decryption>"
    except Exception as e:
        return f"<Decryption error: {str(e)}>"
    
import requests
from django.conf import settings

def send_password_reset_email(email, token):
    subject = 'Password Reset'
    message = f'Click the following link to reset your password: {settings.BASE_URL}/reset_password_confirm/{token}/'
    requests.post(
        f"https://api.mailgun.net/v3/sandbox3413388955f9434681f8a295c775bbdb.mailgun.org/messages",
        auth=("api", settings.EMAIL_HOST_PASSWORD),
        data={"from": f"ChatSafe <{settings.EMAIL_HOST_USER}>",
              "to": [email],
              "subject": subject,
              "text": message})
