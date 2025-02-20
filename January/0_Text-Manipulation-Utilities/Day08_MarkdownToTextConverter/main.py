import re

def strip_Markdown(path: str) -> str:
    txt = open(path, "r")
    content = txt.read()
    # Regex stolen from the internet, I'm sorry but I don't remember where from
    content = re.sub(r"#+\s", "", content)
    content = re.sub(r"[*+-]\s", "", content)
    content = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", content)
    content = re.sub(r"!?\[(.*?)\][\[\(].*?[\]\)]", r"\1", content)
    content = re.sub(r"`(.*?)`", r"\1", content)
    content = re.sub(r"(\*\*|__)(.*?)\1", r"\2", content)
    content = re.sub(r"(\*|_)(.*?)\1", r"\2", content)
    return content

print(strip_Markdown("January/README.md"))