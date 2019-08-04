import matplotlib.pyplot as plt 
import numpy as np 
import torch

class Word_token(object):
    def __init__(self, word, avg_di, count, avg_df=None):
        self.avg_di = avg_di
        self.count = count
        self.avg_df = avg_df

    def __repr__(self):
        return f"avg_di:{self.avg_di}, count:{self.count}"

class Tokenizer(object):
    def __init__(self,token_dict):
        self.token_dict = token_dict

    """ total words count, including repetitive words"""
    @property
    def word_count(self):
        count = 0
        for token in self.token_dict:
            count += token.count
        return count

    """get words with top_count di/df"""
    def top_words(self, mode="di", top_count=-1, reverse=True, filter_thres=None):
        target_dict = self.token_dict.copy()
        if filter_thres is not None:
            target_dict = dict(filter(lambda token: token[1].count>filter_thres,target_dict.items()))
            
        if mode == "di":
            return sorted(target_dict.items(), \
                key=lambda item: item[1].avg_di,reverse=reverse)[:top_count]
            
        assert mode == "df", "mode should be either di or df"
        return sorted(target_dict.items(), \
                key=lambda item: item[1].avg_df,reverse=reverse)[:top_count]

texts = torch.load("texts.pt")
output = np.load("output.npy")
distances = torch.load("distances.pt")
df = distances[0].cpu().data.numpy()
di = distances[1].cpu().data.numpy()

# word2avgdi = {}
# target_layer = 2

# for sen_idx, target_text in enumerate(texts):
#     for word_idx, word in enumerate(target_text.split()):
#         if word in word2avgdi:
#             word = word2avgdi[word]
#             word.avg_di = (word.avg_di + di[target_layer, word_idx, sen_idx]) / (word.count+1)
#             word.count += 1
#         else:
#             word_token = Word_token(word, di[target_layer, word_idx, sen_idx],1)
#             word2avgdi[word] = word_token

# tokenizer = Tokenizer(word2avgdi)
# print(tokenizer.top_words(top_count=10,reverse=True))
# font_name = 'SIMHEI' 
# plt.rcParams['font.family'] = font_name #用来正常显示中文标签 
# plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

target_idx = 0
max_layer = 3
start = 0
end = None
target_layer = 2
mode = "english"

if mode == "chinese":
    target_text = [word for word in texts]
else:
    target_text = [word for word in texts.split()]
    

plt.figure(figsize=(12,8),dpi=100)
colors = ["red","orange","green"]
# for i, target_layer in enumerate(range(0,max_layer)):
plt.plot(di[target_layer,start:end,target_idx],label=f"Di,layer:{target_layer+1}")
plt.plot(df[target_layer,start:end,target_idx],label=f"Df,layer:{target_layer+1}",linestyle="--")

plt.legend(loc="best")
plt.title("ranking visualization",fontsize=15)
plt.xlabel("input sentence",fontsize=15)
plt.xticks(np.arange(len(target_text)),target_text,rotation=30)
# plt.savefig(f'texts_outputs\\{f"l{target_layer+1}"+"_".join(target_text)}.png')
plt.show()