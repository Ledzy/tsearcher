import os

def process_one_file(path):
    corpus = {}
    with open(path,"r",encoding="utf-8") as f:
        text = f.readlines()
        text = "".join([line for line in text if line != "\n"])
        for word in text:
            corpus[word] = corpus.get(word,1)+1
    
    new_text = ""
    for word in text:
        processed_word = word if corpus[word] > 50 else "K"
        if not (is_Chinese(word) or word == "\n" or word == "K"): processed_word = " "
        if word.isdigit(): processed_word = "N"
        new_text += processed_word
    
    with open(path+"_processed","w",encoding="utf-8") as f:
        f.write(new_text)

def process(path):
    file_name = ['train.txt','valid.txt','test.txt']
    file_path = [os.path.join(path, file_) for file_ in file_name]
    for p in file_path:
        process_one_file(p)

def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

process(".\\chinese")