#utils.py
import os
import wave
import argparse
from Crypto.Cipher import AES
from cryptography.fernet import Fernet, InvalidToken
import logging
from .models import ChatKey
import base64
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad


def em_audio(af, string, output, password):
    waveaudio = wave.open(af, mode='rb')
    frame_bytes = bytearray(list(waveaudio.readframes(waveaudio.getnframes())))
    string = string + int((len(frame_bytes) - (len(string) * 8 * 8)) / 8) * '#'
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in string])))
    for i, bit in enumerate(bits):
        frame_bytes[i] = (frame_bytes[i] & 254) | bit
    frame_modified = bytes(frame_bytes)
    with wave.open(output, 'wb') as fd:
        fd.setparams(waveaudio.getparams())
        fd.writeframes(frame_modified)
    waveaudio.close()



def ex_msg(af, password):
    waveaudio = wave.open(af, mode='rb')
    frame_bytes = bytearray(list(waveaudio.readframes(waveaudio.getnframes())))
    extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
    string = "".join(chr(int("".join(map(str, extracted[i:i + 8])), 2)) for i in range(0, len(extracted), 8))
    msg = string.split("###")[0]
    waveaudio.close()
    return msg
 


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
