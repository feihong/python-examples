import random
from urllib.request import urlopen

def generate_chinese_characters(n):
    text = urlopen('http://voachinese.com').read().decode('utf-8')
    chars = set((c for c in text if 0x4e00 <= ord(c) <= 0x9fff))
    chars = list(chars)
    for i in range(n):
        yield random.choice(chars)
