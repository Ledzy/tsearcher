import pandas as pd
import jieba
import math
import jieba.analyse



class Word():
    def __init__(self):
        self.filename_idx = [] #(文件idx)
        self.document_idx = {} #(文件idx: (出现次数，出现位置(list)))

    @property
    def appeared_files(self):
        return len(self.filename_idx)
    
    @property
    def appeared_documents(self):
        return len(self.document_idx)

    def __repr__(self):
        return f"appeared files:{self.appeared_files}; appeared documents{self.appeared_documents}"

class Document_idx():
    def __init__(self):
        self.count = 0
        self.pos = []



def get_index(df):
    index = {}
    for i,row in df.iterrows():
        filename = row['file_name']
        text = row['text']
        name_words = list(jieba.cut(filename, cut_all=True, HMM=True))
        document_words = list(jieba.cut(text, cut_all=True, HMM=True))
        for word in name_words:
            if word in index:
                index[word].filename_idx.append(i)
            else:
                index[word] = Word()
                index[word].filename_idx.append(i)

        for pos, word in enumerate(document_words):
            if word in index:
                if i in index[word].document_idx:
                    index[word].document_idx[i].count += 1
                    index[word].document_idx[i].pos.append(pos)
                
                else:
                    index[word].document_idx[i] = Document_idx()
                    index[word].document_idx[i].count += 1
                    index[word].document_idx[i].pos.append(pos)
            else:
                index[word] = Word()
                index[word].document_idx[i] = Document_idx()
                index[word].document_idx[i].count += 1
                index[word].document_idx[i].pos.append(pos)
    return index

def BM25_one_word(word,document_idx,index,df,avg_document_len,document_count,qtf=1,k1=1,b=1):
    if word not in index: return 0
    if document_idx not in index[word].document_idx: return 0
    
    tf = index[word].document_idx[document_idx].count
    doc_len = len(df.at[document_idx,'text'])
    word_doc_count = index[word].appeared_documents

    word_weight = (document_count-word_doc_count+0.5)/(word_doc_count+0.5)
    score = k1*tf/(tf*(1-b+b*doc_len/avg_document_len)) * math.log(word_weight,2)

    return score
    
def BM25(sentence,document_idx,index,df,avg_document_len,document_count):
    seg_list = jieba.lcut(sentence,cut_all=False)
    score = 0
    for word in seg_list:
        score += BM25_one_word(word,document_idx,index,df,avg_document_len,document_count)
    return score

def get_documents(sentence,index,document_count,df,avg_document_len,top_count=10):
    scores = {}
    sentence = seg_sentence(sentence)

    for document_idx in range(document_count):
        scores[document_idx] = BM25(sentence,document_idx,index,df,avg_document_len,document_count)

    ordered_scores = sorted(scores.items(),key=lambda x: x[1], reverse=True)[:50]
    
    top_documents_idx = list(zip(*ordered_scores))[0]
    
    #找到数量最多的科目，只显示该科目的搜索结果
    subject_count = {}
    for idx in top_documents_idx:
        subject = df.at[idx,'subject']
        subject_count[subject] = subject_count.get(subject,0) + 1

    target_subject = "数学"
    for key in subject_count.keys():
        if subject_count[key] > subject_count[target_subject]:
            target_subject = key
    
    top_documents_idx = list(filter(lambda idx: df.at[idx,'subject']==target_subject ,top_documents_idx))[:top_count]

    return top_documents_idx

def stopwordslist(filepath):  
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]  
    return stopwords  
  
# 对句子进行分词  
def seg_sentence(sentence):  
    sentence_seged = jieba.cut(sentence.strip())  
    outstr = ''  
    for word in sentence_seged:
        if word not in stopwords:  
            if word != '\t':  
                outstr += word  
                outstr += " "  
    return outstr  

stopwords = stopwordslist('stopwords.txt')  # 这里加载停用词的路径  

if __name__ == "__main__":
    query = "传感器是如何工作的"
    df = pd.read_csv('teaching_outline.csv')
    document_count = df.shape[0]
    avg_document_len = df['text'].str.len().mean()
    index = get_index(df)
    print(get_documents(query,index,document_count,df,avg_document_len))