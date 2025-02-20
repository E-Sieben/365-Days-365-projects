def count_chars(s: str) -> int:
    return len(s)
def count_words(s: str) -> int:
    return len(s.split(" "))


print(count_chars("I'm 19 letters long"))
print(count_words("I'm 4 word long"))
print(count_words("Can you imagine that this is nine words long?"))