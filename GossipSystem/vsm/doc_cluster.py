import jieba
import os
import sys
import torch
import numpy as np 
from sklearn.cluster import KMeans

#sets=[set(),set()...]
# topic: 政治, 體育, 娛樂, 社會, 教育, 科技, 國際
topic1 = ['高雄','韓國','韓國瑜','總統','罷免','市長','韓粉','報復','高雄市','高市', '台北市', '蔡英文', '民進黨', '國民黨', '柯文哲', '大巨蛋', '台中', '時代力量', '國昌', '其邁', '北市', '同路人', '發大財', '支那', '五毛', '選舉', '投票']

topic2 = ['籃球','棒球', '足球', 'NBA','nba','ＮＢＡ','鬥牛', '體育署', 'SBL', '581', 'sbl', 'HBL', 'hbl', 'ABL', 'abl', '富邦', '夢想家', '湖人', '裕隆', '公鹿', '快艇', '爪爪', '吱吱', '兄弟', '樂天', '洋基', '紅襪', '太空人', '封館','奧蘭多','迪士尼','佛州','停賽','復賽']

topic3 = ['羅志祥', '莎莎', '愛莉', '愛力', '周揚青', '愷樂', '蝴蝶', '吳宗憲', '館長', '反骨', '阿翔', '謝忻', '周杰倫', '黑人', '范范', '大S', '小S', '劈腿', '多P', '子瑜', 'AV']

topic4 = ['精神','失調','砍人','死刑','思覺','同婚', '外遇', '綠帽', '幻覺', '刺殺', '墮胎', '種族', '酒駕', '超速', '通姦', '除罪', '大法官', '法官', '釋憲', '法匠', '殺人', '家暴', '暴力', '隨機']

topic5 = ['台灣大學','台大','臺灣大學','臺大','資工','資工系','資訊','資訊系','資訊工程','資訊工程學系','資訊工程系','研究所','台大資工', '教育部', '教育', '交大', '清大', '成大', '112', '114', '學店', '大葉', '外文', '法律', '育達', '常春藤', '教授', '陽交', '醫科', '醬料', '雄中', '建中', '北一', '附中', '松山', '高中', '大學']

topic6 = ['蘋果', 'iphone', 'iPhone', '愛鳳', '台積電', '台積', '聯發科', '三星', 'Samsung', '特斯拉', 'Mac', '華碩', 'HTC', 'Google' , '郭台銘', '張忠謀', '郭董', '鴻海', '富士康', '雅虎', '大立光', '谷歌', '華為', '小米']

topic7 = ['病毒', 'COVID-19', '武漢', '肺炎', '新冠', '冠狀', '川普', '韭菜', '匪諜', '小粉紅', '粉紅', '小熊', '維尼', '習近平', '黑人', '中共', '繞台', '抗議', '暴動', '川粉', '金正恩', '北韓', '南韓', '日本', '安倍', '歐洲', '非洲']

sets=[topic7, topic6, topic5, topic4, topic3, topic2, topic1]

def clustering(vectors, idf, vocab):
    vectors = np.array(vectors[1])
    m, n = vectors.shape
    print(m, n)
    '''
    centers=[]
    for i in range(len(sets)):
        tmp = np.zeros([n])
        for term in sets[i]:
            if term in vocab:
                index = vocab.index(term)
                tmp[index]=idf[term]####
        centers.append(tmp)
    centers = np.array(centers)
    '''
    kmeans = KMeans(n_clusters=3, random_state=0).fit(vectors)
    pred = kmeans.predict(vectors)
    vec_class=[[] for _ in range(3)]
    vec_class_id = [[] for _ in range(3)]
    for i in range(m):
        vec_class[pred[i]].append(vectors[i])
        vec_class_id[pred[i]].append(i)
    
    centers = []
    for i in range(3):
        print(len(vec_class_id[i]))
        centers.append(np.mean(np.array(vec_class[i]), axis=0))
    
    return centers, vec_class, vec_class_id

data_dir = sys.argv[1]
vectors = torch.load(os.path.join(data_dir, 'third_cluster_vector.pkl'))
#vectors = np.load(os.path.join(data_dir, 'doc_vector.npy'))
idf = torch.load(os.path.join(data_dir, 'idf.pkl'))
vocab = torch.load(os.path.join(data_dir, 'vocab.pkl'))

centers, cluster_vector, vec_class_id = clustering(vectors, idf, vocab)
torch.save(centers, os.path.join(data_dir, 'fourth_center.pkl'))
torch.save(cluster_vector, os.path.join(data_dir, 'fourth_cluster_vector.pkl'))
torch.save(vec_class_id, os.path.join(data_dir, 'fourth_cluster_id.pkl'))

