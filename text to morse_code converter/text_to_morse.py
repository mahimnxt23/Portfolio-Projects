MORSE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..',
    'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..', '1': '.----',
    '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '0': '-----', ' ': ' ',
}


def text_to_morse(text):
    morse_code = ''

    for char in text.upper():
        if char in MORSE_DICT:
            morse_code += MORSE_DICT[char] + ' '
        else:
            morse_code += char + ' '

    return morse_code.strip()


if __name__ == "__main__":
    input_text = input("Enter the text to convert: -> ")
    result = text_to_morse(input_text)
    print(f"Generated output is: {result}")
