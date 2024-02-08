import os
import time
import pygame
import numpy as np

# By Alexander Andersen

# Disable the welcome message from pygame
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

# Initialize pygame and its mixer
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

print("Welcome to Morse Code Translator by Alexander Andersen")

# Morse Code Dictionary
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 
    'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--', 
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', 
    '9': '----.', '0': '-----', ', ': '--..--', '.': '.-.-.-', '?': '..--..', 
    '/': '-..-.', '-': '-....-', '(': '-.--.', ')': '-.--.-'
}

# Function to encode text to Morse code
def text_to_morse(text):
    morse_code = ''
    for letter in text.upper():
        if letter in MORSE_CODE_DICT:
            morse_code += MORSE_CODE_DICT[letter] + ' '
        else:
            morse_code += ' '
    return morse_code.strip()

# Function to decode Morse code to text
def morse_to_text(morse_code):
    text = ''
    words = morse_code.split('   ')
    for word in words:
        for symbol in word.split():
            for letter, morse in MORSE_CODE_DICT.items():
                if morse == symbol:
                    text += letter
        text += ' '
    return text.strip()

# Function to play Morse code sound
def play_morse_sound(morse_code):
    frequency = 1000  # Sound frequency in Hz
    dit_length = 100  # Duration of a 'dit' in milliseconds
    dah_length = 300  # Duration of a 'dah' in milliseconds
    pause_length = 100  # Duration of the pause between sounds
    sample_rate = 44100  # Sample rate in Hz

    # Function to generate a sound array for a given duration
    def generate_tone(duration):
        t = np.linspace(0, duration / 1000, int(sample_rate * duration / 1000), endpoint=False)
        wave = 0.5 * np.sin(2 * np.pi * frequency * t)
        return np.repeat(wave.reshape(-1, 1), 2, axis=1)  # Convert to 2D array for stereo

    sound_dit = pygame.mixer.Sound(array=generate_tone(dit_length).astype(np.float32))
    sound_dah = pygame.mixer.Sound(array=generate_tone(dah_length).astype(np.float32))

    for symbol in morse_code:
        if symbol == '.':
            sound_dit.play()
            time.sleep(dit_length / 1000.0)
        elif symbol == '-':
            sound_dah.play()
            time.sleep(dah_length / 1000.0)
        time.sleep(pause_length / 1000.0)

# Main function to interact with the user
def main():
    choice = input("Choose the type of translation (1 for Text to Morse, 2 for Morse to Text): ")
    if choice == '1':
        text = input("Enter the text to be translated into Morse: ")
        morse_code = text_to_morse(text)
        print("Translation to Morse:", morse_code)
        if input("Do you want to play the Morse sound? (yes/no): ").lower() == 'yes':
            play_morse_sound(morse_code)
    elif choice == '2':
        morse = input("Enter the Morse code to be translated into text: ")
        text = morse_to_text(morse)
        print("Translation to text:", text)
        if input("Do you want to play the Morse sound? (yes/no): ").lower() == 'yes':
            play_morse_sound(morse)
    else:
        print("Invalid choice. Please choose 1 or 2.")

# Run the main function
if __name__ == "__main__":
    main()
