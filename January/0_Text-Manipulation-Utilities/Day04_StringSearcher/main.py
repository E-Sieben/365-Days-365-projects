def searchText(s: str, path: str) -> list[int, int]:
    occurences: list[int, int] = []
    txt = open(path, "r")
    content = txt.read()
    for i, word in enumerate(content.split()):
        if word == s:
            occurences.append(i)
    return occurences

print("Found as Words:", searchText("file", "January/0_Text-Manipulation-Utilities/Day04_StringSearcher/test.txt"))