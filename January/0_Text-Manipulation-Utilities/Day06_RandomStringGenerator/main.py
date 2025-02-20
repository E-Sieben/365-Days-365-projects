def generate_random_string(l: int) -> str:
    from random import choice
    from string import ascii_letters
    o = ""
    i = 0
    while i < l:
        o = o + choice(ascii_letters)
        i += 1
    return o

print(generate_random_string(3))