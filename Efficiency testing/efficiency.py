from Crypto.Cipher import Blowfish
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import timeit
import os
def padd(text):
    # Add padding to the text to make its length a multiple of 8
    return text + b"\0" * (Blowfish.block_size - len(text) % Blowfish.block_size)

def encrypt_decrypt_input_blowfish(plaintext):
   
    # Generate a random 256-bit (32-byte) encryption key for Blowfish
    key = os.urandom(32)

    # Generate a random 64-bit (8-byte) Initialization Vector (IV) for CBC mode
    iv = Random.new().read(Blowfish.block_size)

    # Create a Blowfish cipher object with the encryption key and IV
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)

    # Encrypt the padded plaintext
    padded_text = padd(plaintext)

    ciphertext = cipher.encrypt(padded_text)

    # Decrypt the ciphertext
    decipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    decrypted_text = decipher.decrypt(ciphertext)

    if decrypted_text.rstrip(b"\0").decode("utf-8") != plaintext.decode("utf-8"):
        print("Decryption failed"  )
   
def encrypt_decrypt_input_aes(plaintext):
    # Generate a random 256-bit (32-byte) encryption key for AES
    key = os.urandom(32)

    # Generate a random 128-bit Initialization Vector (IV) for AES in CBC mode
    iv = Random.new().read(AES.block_size)

    # Create an AES cipher object with the encryption key and IV
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Encrypt the padded plaintext
    padded_text = pad(plaintext, AES.block_size)
    ciphertext = cipher.encrypt(padded_text)

    # Decrypt the ciphertext
    decipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_text = unpad(decipher.decrypt(ciphertext), AES.block_size)

    if decrypted_text.decode("utf-8") != plaintext.decode("utf-8"):
        print("Decryption failed" )

#function to read input data from the file
def read_input_from_file(file_path):
    with open(file_path, 'rb') as file:
        return file.read()
    
if __name__=='__main__':

    iterations = 100000
    file_path = 'encryption msg test.txt'
    userinput = read_input_from_file(file_path)

    print('\nEvaluating Blowfish Implementation...')
    
    encrypt_decrypt_input_blowfish(userinput) # Warm-up

    blowtime = timeit.timeit(lambda: encrypt_decrypt_input_blowfish(userinput), number=iterations)
    blowtime /= iterations

    print('\nEvaluating AES Implementation...')
    encrypt_decrypt_input_aes(userinput) # Warm-up

    aestime = timeit.timeit(lambda: encrypt_decrypt_input_aes(userinput), number=iterations)
    aestime /= iterations

    print(f'\nNumber of Iterations: {iterations}')
    print(f'Size of Input Data: {len(userinput)} bytes')
    print('Average Blowfish Time: {:.6f} microseconds'.format(blowtime * 1e6))
    print('Average AES Time: {:.6f} microseconds'.format(aestime * 1e6))

    percent_difference = abs((blowtime - aestime) / ((blowtime + aestime) / 2)) * 100
    if blowtime < aestime:
        print('Blowfish is faster by {:.2f}% than AES.'.format(percent_difference))
    elif blowtime > aestime:
        print('AES is faster by {:.2f}% than Blowfish.'.format(percent_difference))
    else:
        print('Both algorithms have similar running times.')
