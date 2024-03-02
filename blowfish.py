from Crypto.Cipher import Blowfish
from Crypto import Random
import os



def pad(text):
    # Add padding to the text to make its length a multiple of 8
    return text + b"\0" * (Blowfish.block_size - len(text) % Blowfish.block_size)

plaintext = input("input text to encrypt:").encode('utf-8')
print("Plaintext:", plaintext)

key = os.urandom(32) # Generate a random 256-bit (32-byte) encryption key for Blowfish
print("Encryption Key:", key)


iv = Random.new().read(Blowfish.block_size) # Generate a random 64-bit (8-byte) Initialization Vector (IV) for CBC mode
print("Initialization Vector (IV):", iv)


cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv) # Create a Blowfish cipher object with the encryption key and IV

# Encrypt the padded plaintext

padded_text = pad(plaintext)
print("padded text:",padded_text)
ciphertext = cipher.encrypt(padded_text)

########################################### ENCRYPTED ###################################################################
 # Decrypt the ciphertext
decipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
decrypted_text = decipher.decrypt(ciphertext)

# Print the results
print("Ciphertext:", ciphertext)
print("Decrypted Text:", decrypted_text.rstrip(b"\0").decode("utf-8"))
