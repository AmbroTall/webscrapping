name_words = "ROBERTS JOSEPH".lower().split()

def names_match(text_words):
    name_word_count = sum(1 for word in name_words if word in text_words)
    return name_word_count >= 2

print(names_match('joseph steven roberts45mar'))