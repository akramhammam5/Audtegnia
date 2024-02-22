from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64

# AES encryption function
def encrypt_aes(plaintext, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return ciphertext

# Rearrange the cipher text
def rearrange_cipher(ciphertext):
    return ciphertext[::-1]

# Input text
text = input("Enter text to encrypt: ")

# Secret key
key = b'12345678901234567890123456789012'  # 32-byte key for AES-256

# Encrypt the text
encrypted_text = encrypt_aes(text, key)

# Rearrange the cipher text
rearranged_encrypted_text = rearrange_cipher(encrypted_text)

print("Original encrypted text:", base64.b64encode(encrypted_text).decode())
print("Rearranged encrypted text:", base64.b64encode(rearranged_encrypted_text).decode())

