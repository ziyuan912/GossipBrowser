import os
import sys
import ast
import json
import torch
import jieba
import zhon.hanzi 

used=set()

def make_info(filename):
    with open(filename) as fd:
        print('load files ...')
        articles = fd.read()
        print('turn to dic ...')
        #articles = ast.literal_eval(articles)
        articles=json.loads(articles)
        articles = articles['articles']
        df = {}#bi 2 cnt
        word2doc = {}#k:bigram V: K:doc id v:count
        doclen = {}
        doc2word = {}
        len_of_articles = len(articles)
        print('start processing data ...')
        num_of_blank_articles=0
        for i in range(len_of_articles):#lise=[articles 1,2,3...]
            print(i/len_of_articles)
            #iterate each article
            words_in_articles=set()
            #articles[i]['content']=articles[i]['content']
            if 'content' not in articles[i]:
                num_of_blank_articles+=1
                continue
            if articles[i]['content']=='':
                num_of_blank_articles+=1
                continue
            index=i-num_of_blank_articles
            seg_list = jieba.cut(articles[i]['content'])
            for word in seg_list:
                if zhon.hanzi.non_stops in word or zhon.hanzi.stops in word:
                    continue     
                words_in_articles.add(word)
                
                if word in word2doc:
                    if index in word2doc[word]:
                        word2doc[word][index]+=1
                    else:
                        word2doc[word][index]=1
                else:
                    word2doc[word]={}
                    word2doc[word][index]=1
                if index not in doclen:
                    doclen[index]=1
                else :
                    doclen[index]+=1
            articles[i]['article_id'] = index
            print(index)
            for term in words_in_articles:
                if term in df:
                    df[term]+=1
                else:
                    df[term]=1
        #print(bi2doc)
    
    hold=0
    for k,v in doclen.items():
        hold += v
    hold /= len(doclen)
    doclen[-1] = hold

    delete_keys = []
    for word, times in df.items():
        if df[word] < 15:
            delete_keys.append(word)
    
    for word in delete_keys:
        del df[word]
        del word2doc[word]

    return word2doc, df, articles, doclen

data_dir = sys.argv[1]
tf, df, articles, doclen = make_info(os.path.join(data_dir, 'gossiping-1-2000.json'))

print(doclen)
print('saving tf ...')
torch.save(tf, os.path.join(data_dir, 'tf.pkl'))
print('saving df ...')
torch.save(df, os.path.join(data_dir, 'df.pkl'))

print('saving doclen')

torch.save(doclen, os.path.join(data_dir,'doclen.pkl'))
#print('num_of_blank_articles',num_of_blank_articles)
print('saving docs')
torch.save(articles, os.path.join(data_dir,'articles.json'))

