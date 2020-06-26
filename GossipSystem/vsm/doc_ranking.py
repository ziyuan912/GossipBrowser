import jieba
import sys
import os
import torch
import numpy as np

def calculate_doc_ranking(query, doc_vector, idf, vocab, relevance_feedback=False):
    # word segmentation
    seg_list = jieba.cut(query)
    query_tf = {}
    for word in seg_list:
        if word not in query_tf:
            query_tf[word] = 1
        else:
            query_tf[word] += 1    
    
    # Create query vector
    query_vec = []
    for w in vocab:
        if w in idf and w in query_tf:
            query_vec.append(query_tf[w] * idf[w])
        else:
            query_vec.append(0)

    # Calculate cosine similarity
    cos_sim_list = []
    query_vec = np.array(query_vec)
    for j in range(len(doc_vector)):
        cos_sim = np.dot(doc_vector[j], query_vec) / (np.linalg.norm(doc_vector[j]) * np.linalg.norm(query_vec) + 1e-8)
        cos_sim_list.append(cos_sim)

    cos_sim_arr = np.array(cos_sim_list)
    ind = np.argpartition(cos_sim_arr, -10)[-10:]
    sort_ind = ind[np.argsort(cos_sim_arr[ind])][::-1]

    return sort_ind

if __name__ == '__main__':
    query = input()

    model_dir = sys.argv[1]
    doc_vector = np.load(os.path.join(model_dir, 'doc_vector.npy'))
    idf = torch.load(os.path.join(model_dir, 'idf.pkl'))
    vocab = torch.load(os.path.join(model_dir, 'vocab.pkl'))

    doc_ranking = calculate_doc_ranking(query, doc_vector, idf, vocab)
    print("Doc Ranking: {}".format(doc_ranking))

    articles = torch.load(os.path.join(model_dir, 'articles.pkl'))
    for index in list(doc_ranking):
        print(articles[index]['article_title'])

