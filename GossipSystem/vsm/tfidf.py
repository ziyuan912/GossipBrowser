import numpy as np
import xml
import sys
import xml.etree.ElementTree as ET
import math
import pickle
import re
import jieba
def remove_punctuation(line):
    rule = re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]")
    line = rule.sub('',line)
    return line

class TF_IDF():
    def __init__(self, tf, df, doc_length, stopwords=None, narr=False):
        
        self.tf = tf
        self.df = df
        self.idf = {}
        self.idx2word = {}
        self.word2idx = {}
        self.word_voc = []
        self.doc_length = doc_length

        word_count = 0
        for word, df in self.df.items():
            self.idf[word] = math.log10(30000 / df)
            self.idx2word[word_count] = word
            self.word2idx[word] = word_count
            word_count += 1
            self.word_voc.append(word)
    
    def tf_idf(self, index, word):
        k1 = 1.5
        b = 0.75
        if index in self.tf[word]:
            return self.tf[word][index]*self.idf[word]* (k1+1) / (self.tf[word][index] + k1 * (1-b+b*self.doc_length[index]/self.doc_length[-1]))
        else:
            return 0
    
    def get_doc_vector(self, index):
        return  [1*self.tf_idf(index, w) if w in self.tf else 0 for w in self.word_voc]
    

