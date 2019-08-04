import sys
import torch
import argparse
import hashlib
import os
import numpy as np
import data
from data import Corpus
from torch.optim import SGD, Adam
from splitcross import SplitCrossEntropyLoss
from model import RNNModel
from parse_arg import *
from utils import batchify, get_batch, repackage_hidden
 
#load the model
model_path = os.path.join(os.getcwd(),"models","3layer_1000_epoch.pt")
mode = "english"
data_path = "./data/penn"
torch.nn.Module.dump_patches = True #ensure the loaded model maintain the topology


def get_df(text):
    fn = 'corpus.{}.data'.format(hashlib.md5(args.data.encode()).hexdigest())
    if args.philly:
        fn = os.path.join(os.environ['PT_OUTPUT_DIR'], fn)
    if os.path.exists(fn):
        print('Loading cached dataset...')
        corpus = torch.load(fn)
    else:
        print('Producing dataset...')
        corpus = data.Corpus(data_path,mode=mode)
        torch.save(corpus, fn)

    ntokens = len(corpus.dictionary)

    #initialize the model
    model = RNNModel(args.model, ntokens, args.emsize, args.nhid, args.chunk_size, args.nlayers,
                           args.dropout, args.dropouth, args.dropouti, args.dropoute, args.wdrop, args.tied)


    with open(model_path,"rb") as f:
        model, criterion, optimizer = torch.load(f)

    #prepare data
    eval_batch_size = 10
    test_batch_size = 1
    train_data = batchify(corpus.train, args.batch_size, args)
    val_data = batchify(corpus.valid, eval_batch_size, args)
    test_data = batchify(corpus.test, test_batch_size, args)

    def idx2text(index):
        global corpus
        text = [corpus.dictionary.idx2word[idx] for idx in index]
        text = " ".join(text)
        return text

    def text2idx(text,mode="chinese"):
        global corpus
        if mode == "chinese":
            idx = [corpus.dictionary.word2idx.get(word,corpus.dictionary.word2idx['K']) for word in text]
        else:
            idx = [corpus.dictionary.word2idx.get(word,corpus.dictionary.word2idx['<unk>']) for word in text.split()]
        return idx

    idx = torch.tensor(text2idx(text,mode=mode)).unsqueeze(dim=-1).cuda()
    # seq_len = idx.size(0)
    hidden = model.init_hidden(args.batch_size)
    hidden = repackage_hidden(hidden)
    output, hidden, distances = model(idx, hidden, return_d=True)


    target_layer = 2
    target_idx = 0


    df = distances[0].cpu().data.numpy()

    target_text = [word for word in texts]
    df = df[target_layer,:,target_idx]

    return df