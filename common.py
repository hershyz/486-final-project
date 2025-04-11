import re

# simple regex-based tokenizer, keeps contraction and lowercase-normalizes words
def simple_tokenizer(text):
    text = text.lower()
    tokens = re.findall(r"\b\w+(?:'\w+)?\b", text)
    return tokens