import os
import sys
import torch

data_dir = sys.argv[1]
vectors1 = torch.load(os.path.join(data_dir, 'cluster_vector.pkl'))
vectors2 = torch.load(os.path.join(data_dir, 'second_cluster_vector.pkl'))
vectors3 = torch.load(os.path.join(data_dir, 'third_cluster_vector.pkl'))
vectors4 = torch.load(os.path.join(data_dir, 'fourth_cluster_vector.pkl'))

center1 = torch.load(os.path.join(data_dir, 'center.pkl'))
center2 = torch.load(os.path.join(data_dir, 'second_center.pkl'))
center3 = torch.load(os.path.join(data_dir, 'third_center.pkl'))
center4 = torch.load(os.path.join(data_dir, 'fourth_center.pkl'))

id1 = torch.load(os.path.join(data_dir, 'cluster_id.pkl'))
id2 = torch.load(os.path.join(data_dir, 'second_cluster_id.pkl'))
id3 = torch.load(os.path.join(data_dir, 'third_cluster_id.pkl'))
id4 = torch.load(os.path.join(data_dir, 'fourth_cluster_id.pkl'))

# Cat hierachial cluster document vector to a file
vectors = []
centers = [] 
vectors_id = []

for i in range(len(vectors1)):
    if len(vectors1[i]) < 300 or len(vectors1[i]) > 10000:
        continue
    else:
        vectors.append(vectors1[i])
        centers.append(center1[i])
        vectors_id.append(id1[i])

for i in range(len(vectors2)):
    if len(vectors2[i]) < 300 or len(vectors2[i]) > 6000:
        continue
    else:
        vectors.append(vectors2[i])
        centers.append(center2[i])
        tmp = []
        for j in range(len(vectors2[i])):
            tmp.append(id1[-1][id2[i][j]])
        vectors_id.append(tmp)


for i in range(len(vectors3)):
    if len(vectors3[i]) < 300 or len(vectors3[i]) > 4000:
        continue
    else:
        vectors.append(vectors3[i])
        centers.append(center3[i])
        tmp = []
        for j in range(len(vectors3[i])):
            tmp.append(id1[-1][id2[1][id3[i][j]]])
        vectors_id.append(tmp)

 


for i in range(len(vectors4)):
    if len(vectors4[i]) < 300:
        continue
    else:
        vectors.append(vectors4[i])
        centers.append(center4[i])
        tmp = []
        for j in range(len(vectors4[i])):
            tmp.append(id1[-1][id2[1][id3[1][id4[i][j]]]])
        vectors_id.append(tmp)



for i in range(len(vectors)):
    print(len(vectors[i]))

print(vectors_id)
torch.save(vectors, os.path.join(data_dir, 'final_cluster_vector.pkl'))
torch.save(centers, os.path.join(data_dir, 'final_center.pkl'))
torch.save(vectors_id, os.path.join(data_dir, 'final_cluster_id.pkl'))

