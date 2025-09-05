from do_an_1 import *

from docx import Document
import re

dict_file = "VDic_uni.docx"
doc = Document(dict_file)

# 1. read file doc line-by-line, đọc từng chữ
words = []

def process_dict(path):
    doc = Document(path)
    paras = []

    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            parts = text.split("\t")
            words.append(parts[0])
        paras.append(text)
    return paras


paragraphs = process_dict(dict_file)
print(f"Từ điển có: {len(paragraphs)}")
# print(paragraphs[:5])   # list of strings
# print(words[:3])

# 2. tách ra nếu cần thiết 
syllables = []
for word in words:
    syllable_split = re.split(r"[\s\-]+", word)
    for syllable in syllable_split:
        syllables.append(syllable)
print(f"Có {len(syllables)} âm tiết")

# 3. process từng âm tiết -> nếu process dc thì thêm nó vào list [âm tiết TV], 0 thì thêm vào list [ko phải âm tiết TV]
valid_syllables = []
invalid_syllables = []

for syllable in syllables:
    try:
        print("======")
        print("word: " + syllable)
        print(VietnameseSyllable(syllable).info())
        ipa = VietnameseSyllable(syllable).to_ipa()
        valid_syllables.append((syllable, ipa))
    except InvalidSyllableError:
        invalid_syllables.append(syllable)
    
# if __name__ == "__main__":
#     results = process_dict("viet_dict.docx")
#     for word, ipa in results:
#         print(f"{word} -> {ipa}")