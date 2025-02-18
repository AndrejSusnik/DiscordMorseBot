
morse_dict = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.",
    "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
    "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
    "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
    "Y": "-.--", "Z": "--..", "1": ".----", "2": "..---", "3": "...--",
    "4": "....-", "5": ".....", "6": "-....", "7": "--...", "8": "---..",
    "9": "----.", "0": "-----", ".": ".-.-.-", ",": "--..--", "?": "..--..",
}

text_2_morse = {v: k for k, v in morse_dict.items()}

def morse_to_text(str_in_morse):
    morse_chars = str_in_morse.split()
    for i, char in enumerate(morse_chars):
        if char not in text_2_morse:
            return f"Nepričakovan znak {char} na mestu {i + 1}" 

    return ''.join([text_2_morse.get(char, char) for char in str_in_morse.split()]) 

def text_to_morse(string):
    string = string.upper().strip().replace(' ', '')

    return ' '.join([morse_dict.get(char, char) for char in string])