ENG_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
RUS_LETTERS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ0123456789'


def enc_dec_replace(text):
    enc_dec_text = ''
    for letter in text:
        result = letter
        if letter in ENG_LETTERS:
            result = ENG_LETTERS[35 - ENG_LETTERS.index(letter)]
        elif letter in ENG_LETTERS.lower():
            result = ENG_LETTERS.lower()[35 - ENG_LETTERS.lower().index(letter)]
        elif letter in RUS_LETTERS:
            result = RUS_LETTERS[42 - RUS_LETTERS.index(letter)]
        elif letter in RUS_LETTERS.lower():
            result = RUS_LETTERS.lower()[42 - RUS_LETTERS.lower().index(letter)]
        enc_dec_text += result

    return enc_dec_text


def enc_dec_shift(text, key, mode='enc'):
    if mode == 'dec' and key:
        key = -key
    elif not key:
        print('key is not correct')
        return
    enc_dec_text = ''
    for letter in text:
        result = letter
        if letter in ENG_LETTERS:
            result = ENG_LETTERS[(ENG_LETTERS.index(letter) + key) % 36]
        elif letter in ENG_LETTERS.lower():
            result = ENG_LETTERS.lower()[(ENG_LETTERS.lower().index(letter) + key) % 36]
        elif letter in RUS_LETTERS:
            result = RUS_LETTERS[(RUS_LETTERS.index(letter) + key) % 43]
        elif letter in RUS_LETTERS.lower():
            result = RUS_LETTERS.lower()[(RUS_LETTERS.lower().index(letter) + key) % 43]
        enc_dec_text += result

    return enc_dec_text
