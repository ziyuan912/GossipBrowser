import jieba
import sys
import os
import torch
import numpy as np
import json

def query_clustering(query, cluster_vec):
    cos_sim_list = []
    for i in range(len(cluster_vec)):
        cos_sim = np.dot(cluster_vec[i], query) / (np.linalg.norm(cluster_vec[i]) * np.linalg.norm(query) + 1e-8)
        cos_sim_list.append(cos_sim)
    
    print(cos_sim_list) 
    max_id = cos_sim_list.index(max(cos_sim_list))
    return max_id

def calculate_doc_ranking(query, doc_vector, relevance_feedback=False):
    # Calculate cosine similarity
    cos_sim_list = []
    for j in range(len(doc_vector)):
        cos_sim = np.dot(doc_vector[j], query) / (np.linalg.norm(doc_vector[j]) * np.linalg.norm(query) + 1e-8)
        cos_sim_list.append(cos_sim)
    #print(cos_sim_list)
    cos_sim_arr = np.array(cos_sim_list)
    ind = np.argpartition(cos_sim_arr, -15)[-15:]
    sort_ind = ind[np.argsort(cos_sim_arr[ind])][::-1]
    
    if len(np.where(cos_sim_arr[sort_ind[:15]] == 0)[0]) == 0:
        return sort_ind[:10], sort_ind[10:]
    else:
        max_len = np.where(cos_sim_arr[sort_ind[:10]] == 0)[0][0]
        if max_len <= 10:
            return sort_ind[:max_len], []
        return sort_ind[:10], sort_ind[10:max_len]

def get_query_vector(query, vocab, idf):
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
    
    return np.array(query_vec)


def load_model():
    # model_dir = sys.argv[1]
    model_dir = "/Users/jeffreychen/Documents/GossipBrowser/GossipSystem/vsm/IR-Gossip-data/"
    #doc_vector = np.load(os.path.join(model_dir, 'doc_vector.npy'))
    idf = torch.load(os.path.join(model_dir, 'idf.pkl'))
    vocab = torch.load(os.path.join(model_dir, 'vocab.pkl'))

    center = torch.load(os.path.join(model_dir, 'final_center.pkl'))
    cluster_vector = torch.load(os.path.join(model_dir, 'final_cluster_vector.pkl'))
    cluster_id = torch.load(os.path.join(model_dir, 'final_cluster_id.pkl'))

    return idf, vocab, center, cluster_vector, cluster_id


def cal(query, idf, vocab, center, cluster_vector, cluster_id):
    query = get_query_vector(query, vocab, idf)
    max_cluster_id = query_clustering(query, center)

    cluster_ranking, recommend = calculate_doc_ranking(query, cluster_vector[max_cluster_id])
    
    doc_ranking = []
    for idx in cluster_ranking:
        doc_ranking.append(cluster_id[max_cluster_id][idx])

    for idx in recommend:
        doc_ranking.append(cluster_id[max_cluster_id][idx])

    return doc_ranking


if __name__ == '__main__':
    query = input()

    model_dir = sys.argv[1]
    #doc_vector = np.load(os.path.join(model_dir, 'doc_vector.npy'))
    idf = torch.load(os.path.join(model_dir, 'idf.pkl'))
    vocab = torch.load(os.path.join(model_dir, 'vocab.pkl'))

    center = torch.load(os.path.join(model_dir, 'final_center.pkl'))
    cluster_vector = torch.load(os.path.join(model_dir, 'final_cluster_vector.pkl'))
    cluster_id = torch.load(os.path.join(model_dir, 'final_cluster_id.pkl'))

    query = get_query_vector(query, vocab, idf)
    max_cluster_id = query_clustering(query, center)

    cluster_ranking, recommend = calculate_doc_ranking(query, cluster_vector[max_cluster_id])
    
    #print("Doc Ranking: {}".format(doc_ranking))
 
    with open(os.path.join(model_dir, 'articles.json'), 'r') as f:
        articles = json.loads(f.read())
    
    doc_ranking = []
    for idx in cluster_ranking:
        doc_ranking.append(cluster_id[max_cluster_id][idx])

    title = [""] * len(doc_ranking)
    content = [""] * len(doc_ranking)
    for article in articles:
        if "article_id" not in article:
            continue
        if article['article_id'] in doc_ranking:
        #print(doc_vector[index][66196])
            index = doc_ranking.index(article['article_id'])
            title[index] = article['article_title']
            content[index] = article['content']
   
    for i in range(len(doc_ranking)):
        print(title[i])
        print(content[i])

