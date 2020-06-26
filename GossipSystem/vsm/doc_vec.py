import numpy as np
import xml
import sys
import xml.etree.ElementTree as ET
import math
import pickle
import re
from tfidf import TF_IDF, remove_punctuation
import jieba
import os
from argparse import ArgumentParser
import torch

doc_length = torch.load('_data/doclen.pkl')
tf = torch.load('_data/tf.pkl')
df = torch.load('_data/df.pkl')
print("Avg doc len:{}".format(doc_length[-1]))

# Calculate document vector:)
tfidf = TF_IDF(tf, df, doc_length)
print("Voc size:{}".format(len(tfidf.word2idx)))
doc_vector = []
for i in range(len(doc_length)-1):
    if (i+1) % 100 == 0:
        print(i+1)
    doc_vector.append(tfidf.get_doc_vector(i))

doc_vector = np.array(doc_vector)
print(doc_vector.shape)
torch.save(tfidf.idf, '_data/idf.pkl')
torch.save(tfidf.word_voc, '_data/vocab.pkl')
np.save('_data/doc_vector.npy', doc_vector)
print("Finish Calculating Document vector successfully:)")

