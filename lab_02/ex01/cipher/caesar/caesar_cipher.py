from cipher.caesar import ALPHABET

class CaesarCipher:
    def __init__(self):
        self.alphabet = ALPHABET
    
    def encrypt_text(self, text: str, key: int) -> str:
        alphabet_len = len(self.alphabet)
        text = text.upper();
        encryted_text = []
        for letter in text:
            letter_index = self.alphabet.index(letter)
            ouput_index = (letter_index + key) % alphabet_len
            ouput_letter = self.alphabet[ouput_index]
            encryted_text.append(ouput_letter)
        return "".join(encryted_text)
    def decrypt_text(self, text: str, key: int) -> str:
        alphabet_len = len(self.alphabet)
        text = text.upper();
        decrypted_text = []
        for letter in text:
            letter_index = self.alphabet.index(letter)
            ouput_index = (letter_index + key) % alphabet_len
            ouput_letter = self.alphabet[ouput_index]
            decrypted_text.append(ouput_letter)
        return "".join(decrypted_text)
    