def to_caesar_cypher(s: str, move: int = 1) -> str:
    from string import ascii_lowercase, ascii_uppercase
    s: list[str] = list(s)
    a: list[str] = list(ascii_lowercase)
    A: list[str] = list(ascii_uppercase)
    o: list[str] = []
    for letter in s:
        if letter not in (a+A):
            o.append(letter)
        elif letter in a:
            try:
                o.append(a[a.index(letter) + move])
            except IndexError:
                o.append(a[a.index(letter) + move - 26])
        else:
            try:
                o.append(A[A.index(letter) + move])
            except IndexError:
                o.append(A[A.index(letter) + move - 26])
    return "".join(o)

print(to_caesar_cypher("Hello World!"))