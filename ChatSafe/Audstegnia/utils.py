import os
import wave
import argparse

def em_audio(af, string, output):
  try:
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
  except Exception as e:
   print(f"Error in em_audio: {e}")



def ex_msg(af):
    waveaudio = wave.open(af, mode='rb')
    frame_bytes = bytearray(list(waveaudio.readframes(waveaudio.getnframes())))
    extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
    string = "".join(chr(int("".join(map(str, extracted[i:i + 8])), 2)) for i in range(0, len(extracted), 8))
    msg = string.split("###")[0]
    waveaudio.close()
    return msg

def encrypt_text(text, key):
    key = key.ljust(32, b'\0')[:32]
    iv = b'\0' * 16  # Use a constant IV for simplicity, consider using a random IV in production
    
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(text.encode('utf-8')) + padder.finalize()
    
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    return b64encode(ciphertext).decode()

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
