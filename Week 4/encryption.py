def encrypt(text, shift=3):
    """
    Simple Caesar cipher encryption
    """
    result = ""
    for char in text:
        if char.isalpha():
            ascii_offset = ord('a') if char.islower() else ord('A')
            result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
        else:
            result += char
    return result

def decrypt(text, shift=3):
    """
    Simple Caesar cipher decryption
    """
    return encrypt(text, 26 - shift)  # Using the property that decrypt is encrypt with reverse shift