import random
from urllib.request import urlopen


def generate_chinese_characters(n):
    text = urlopen('http://voachinese.com').read().decode('utf-8')
    chars = set((c for c in text if 0x4e00 <= ord(c) <= 0x9fff))
    chars = list(chars)
    for i in range(n):
        yield random.choice(chars)


EYES = "^ᵒ♥•ಠ°ಥ・$'"
MOUTHS = '_◡ᴥ□Д益ェω∀'
FACES = '()[]{}《》【】||'
FACES = [FACES[i:i+2] for i in range(0, len(FACES), 2)]

def generate_emoticons(n):
    for i in range(n):
        eye = random.choice(EYES)
        mouth = random.choice(MOUTHS)
        left, right = random.choice(FACES)
        yield ''.join((left, eye, mouth, eye, right))
