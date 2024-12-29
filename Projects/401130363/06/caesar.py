def caesar_encode(text, shift):
    encoded_text = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            encoded_text.append(chr((ord(char) - base + shift) % 26 + base))
        else:
            encoded_text.append(char)
    return ''.join(encoded_text)


def caesar_decode(text, shift):
    return caesar_encode(text, -shift)
