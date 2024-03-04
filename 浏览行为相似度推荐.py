import numpy as np

# 定义数据集
dataset = {
    'user1': [['music', 'movies', 'sports'],['food', 'movies', 'travel'],['music', 'books', 'fashion']],
    'user2': [['music', 'movies', 'sports'],['sports', 'food', 'fashion'],['sports', 'food', 'fashion']],
    'user4': [['music', 'books', 'fashion'],['music', 'books', 'fashion'],['sports', 'food', 'fashion']],
}

# 将数据集转换为特征向量
def transform(dataset):
    items = []
    for user in dataset:
        for item in dataset[user]:
            if item not in items:
                items.append(item)
    features = np.zeros((len(dataset), len(items)))
    for i, user in enumerate(dataset):
        for item in dataset[user]:
            j = items.index(item)
            features[i][j] = 1
    return features

# 计算余弦相似度
def cosine_similarity(features, i, j):
    dot_product = np.dot(features[i], features[j])
    norm_i = np.linalg.norm(features[i])
    norm_j = np.linalg.norm(features[j])
    return dot_product / (norm_i * norm_j)

# 推荐算法
def content_based_recommendation(user, dataset):
    features = transform(dataset)
    similarities = []
    for i in range(len(dataset)):
        if list(dataset.keys())[i] != user:
            similarities.append(cosine_similarity(features, i, list(dataset.keys()).index(user)))
        else:
            similarities.append(0)
    idx = np.argmax(similarities)
    recommended_user = list(dataset.keys())[idx]
    return dataset[recommended_user]

# 测试算法
user = 'user1'
print(content_based_recommendation(user, dataset))

