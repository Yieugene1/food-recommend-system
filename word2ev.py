# -*- coding: utf-8 -*-

from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
import jieba
import numpy as np


# 美食数据集



# 使用jieba分词将所有单词拆分成标记
tokenized_foods = [jieba.lcut(''.join(food_list)) for food_list in foods]

# 定义Word2Vec模型并训练
model = Word2Vec(sentences=tokenized_foods, window=5, min_count=1, workers=4)

# 将美食向量组成一个向量矩阵
food_vectors = []

for food in foods:
    # 对于每个美食名称，尝试获取其向量表示
    try:
        vector = model.wv[food]
        food_vectors.append(vector)
    except KeyError:
        # 如果该单词不在模型词汇表中，跳过该名称
        continue

if len(food_vectors) == 0:
    print("None of the words in the foods list are present in the model vocabulary.")
else:
    food_vector_matrix = np.vstack(food_vectors)

    # 输入查询文本
    query_text = '饭'

    # 使用jieba分词将查询文本分成单词列表
    query_words = jieba.lcut(query_text)
    # 过滤掉模型词汇表中不存在的单词
    query_words = [word for word in query_words if word in model.wv.key_to_index]
    print('查询文本:')

    print(query_text)
    print('输出前5个:')

    # 判断是否存在有效的单词
    if len(query_words) == 0:
        print("None of the words in the query text are present in the model vocabulary.")
    else:
        # 计算查询文本向量
        query_vectorized = sum([model.wv[word] for word in query_words]) / len(query_words)

        # 计算每个美食与查询文本之间的相似度
        cosine_similarities = cosine_similarity([query_vectorized], food_vector_matrix)[0]
        cosine_similarities = np.squeeze(cosine_similarities)

        # 根据相似度排序并返回推荐结果
        num_recommendations = 6
        related_docs_indices = [i for i in sorted(range(len(cosine_similarities)), key=lambda k: cosine_similarities[k],
                                                  reverse=True)]

        recommended_foods = []
        for rank, index in enumerate(related_docs_indices):
            if rank > 0 and rank <= num_recommendations:
                # 过滤掉空字符串并检查单词是否在Word2Vec模型的词汇表中
                filtered_food_list = [food.strip() for food in foods[index] if food.strip() in model.wv.key_to_index]
                if len(filtered_food_list) > 0:
                    food_str = '，'.join(filtered_food_list)
                    recommended_foods.append(food_str)

        if len(recommended_foods) == 0:
            print("None of the foods in the list match the query text.")
        else:
            recommended_foods = [s.replace('，', '').replace('。', '') for s in recommended_foods]
            print(recommended_foods)
