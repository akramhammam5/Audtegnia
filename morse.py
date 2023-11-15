import sys
import base64
import urllib.parse


MORSE_CODE_DICT = {'A': '.-', 'B': '-...',
                  'C': '-.-.', 'D': '-..', 'E': '.',
                  'F': '..-.', 'G': '--.', 'H': '....',
                  'I': '..', 'J': '.---', 'K': '-.-',
                  'L': '.-..', 'M': '--', 'N': '-.',
                  'O': '---', 'P': '.--.', 'Q': '--.-',
                  'R': '.-.', 'S': '...', 'T': '-',
                  'U': '..-', 'V': '...-', 'W': '.--',
                  'X': '-..-', 'Y': '-.--', 'Z': '--..',
                  '1': '.----', '2': '..---', '3': '...--',
                  '4': '....-', '5': '.....', '6': '-....',
                  '7': '--...', '8': '---..', '9': '----.',
                  '0': '-----', ',': '--..--', '.': '.-.-.-',
                  '?': '..--..', '/': '-..-.', '-': '-....-',
                  '(': '-.--.', ')': '-.--.-', ' ': '/'}  # Adding space as '/' for better visibility
MORSE_CODE = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z', '.----': '1', '..---': '2', '...--': '3', '....-': '4',
    '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9',
    '-----': '0', '--..--': ',', '.-.-.-': '.', '..--..': '?',
    '-..-.': '/', '-....-': '-', '-.--.': '(', '-.--.-': ')',
    '.-..-.': '"', '.----.': "'", '---...': ':', '-.-.-.': ';',
    '-...-': '=', '.-.-.': '+', '-....-': '-', '..--.-': '_',
    '.-...': '&', '.--.-.': '@', '...-..-': '$', '.-.-..': '!'
}


def decrypt_morse_code(ciphertext):
    words = ciphertext.split(' / ')
    plaintext = ""
    for word in words:
        letters = word.split()
        for letter in letters:
            if letter in MORSE_CODE:
                plaintext += MORSE_CODE[letter].lower()
            else:
                plaintext += '?'
        plaintext += ' '
    return plaintext.strip()


def text_to_morse(text):
    morse_code = ''
    for char in text.upper():
        if char in MORSE_CODE_DICT:
            morse_code += MORSE_CODE_DICT[char] + ' '
        else:
            morse_code += ' '

    return morse_code

if __name__ == "__main__":
    args = sys.argv

    try:
        if len(args) > 1:
            if args[1] == '-m' or args[1] == '--mode':
                if len(args) > 2:
                    mode = args[2]
                    if mode not in ['e', 'd']:
                        raise ValueError("Invalid mode. Use 'e' for encoding or 'd' for decoding.")
                    if len(args) > 4 and args[3] == '-i':
                        ciphertext = args[4]
                        print("Input mode:", mode)  # Print the selected mode
                        print("Input ciphertext:", ciphertext)  # Print the user input
                        if mode == "e":
                            decoded_text = text_to_morse(ciphertext)
                            if decoded_text:
                                print("Decoded plaintext:", decoded_text)
                        elif mode == "d":
                            decoded_text = decrypt_morse_code(ciphertext)
                            if decoded_text:
                                print("Decoded plaintext:", decoded_text)
                    else:
                        raise ValueError("Invalid input. Use '-i' followed by the input text.")
                else:
                    raise ValueError("Mode argument is missing. Use 'e' for encoding or 'd' for decoding.")
            else:
                raise ValueError("Invalid argument. Use '-m' or '--mode'.")
        else:
            raise ValueError("Please provide arguments.")
    except Exception as e:
        print(f"[-] {e}")