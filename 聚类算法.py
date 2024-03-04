import numpy as np
from sklearn.cluster import KMeans


def diversity_clustering(items, k=8):
    # 将每个物品表示成一个向量
    vectors = []
    for item in items:
        vector = [item['feature1'], item['feature2'], item['feature3']]
        vectors.append(vector)

    # 使用 K-Means 聚类算法将物品划分为 k 个簇
    kmeans = KMeans(n_clusters=k, random_state=0).fit(vectors)
    clusters = [[] for i in range(k)]
    for i, label in enumerate(kmeans.labels_):
        clusters[label].append(items[i])

    # 对每个簇中的物品进行排序，只保留代表性最强的几个物品
    results = []
    for cluster in clusters:
        sorted_cluster = sorted(cluster, key=lambda x: x['score'], reverse=True)[:3]
        results += sorted_cluster

    return results
