import os
import wave
import argparse

def em_audio(af, string, output):
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



def ex_msg(af):
    waveaudio = wave.open(af, mode='rb')
    frame_bytes = bytearray(list(waveaudio.readframes(waveaudio.getnframes())))
    extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
    string = "".join(chr(int("".join(map(str, extracted[i:i + 8])), 2)) for i in range(0, len(extracted), 8))
    msg = string.split("###")[0]
    waveaudio.close()
    return msg

def encrypt_text(text, key):
    # Ensure the key is 32 bytes (256 bits) long
    key = key.ljust(32, b'\0')[:32]
    
    # Generate a random IV (Initialization Vector)
    iv = os.urandom(16)
    
    # Create an AES cipher object with CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Add padding to the plaintext
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(text.encode('utf-8')) + padder.finalize()
    
    # Encrypt the padded data
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    # Combine the IV and ciphertext
    encrypted_text = iv + ciphertext
    
    # Encode the result in base64 for easier representation
    return b64encode(encrypted_text).decode()

def decrypt_text(encrypted_text, key):
    # Ensure the key is 32 bytes (256 bits) long
    key = key.ljust(32, b'\0')[:32]
    
    # Decode the base64 encoded input
    encrypted_text = b64decode(encrypted_text)
    
    # Extract the IV and ciphertext
    iv = encrypted_text[:16]
    ciphertext = encrypted_text[16:]
    
    # Create an AES cipher object with CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    # Decrypt the ciphertext
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    
    # Remove the padding
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    
    # Decode the bytes to get the original text
    return unpadded_data.decode('utf-8')



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
