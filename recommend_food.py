import math

class UserCF:
    def __init__(self, data):
        self.users = data

    # 计算两个用户之间的皮尔逊相关系数
    def pearson(self, user1, user2):
        # 找到两个用户共同评价过的商品
        common_items = {}
        for item in self.users[user1]:
            if item in self.users[user2]:
                common_items[item] = 1

        n = len(common_items)

        # 如果没有共同评价过的商品，返回 0
        if n == 0:
            return 0

        # 计算评分的平均值
        ave1 = sum([self.users[user1][item] for item in common_items]) / n
        ave2 = sum([self.users[user2][item] for item in common_items]) / n

        # 计算分子和分母
        numerator = sum([(self.users[user1][item] - ave1) * (self.users[user2][item] - ave2) for item in common_items])
        denominator = math.sqrt(sum([(self.users[user1][item] - ave1) ** 2 for item in common_items])) * \
                      math.sqrt(sum([(self.users[user2][item] - ave2) ** 2 for item in common_items]))

        # 如果分母为 0，返回 0
        if denominator == 0:
            return 0

        return numerator / denominator

    # 根据用户的评分数据，计算每个用户与其他用户的相似度
    def similarity_matrix(self):
        matrix = {}
        for user1 in self.users:
            for user2 in self.users:
                if user1 != user2:
                    matrix.setdefault(user1, {})
                    matrix[user1].setdefault(user2, 0)
                    matrix[user1][user2] = self.pearson(user1, user2)
        return matrix

    # 根据相似度矩阵和给定的用户，推荐商品
    def recommend(self, user, sim_matrix):
        scores = {}
        total_sims = {}

        # 遍历与该用户具有相似性的所有用户
        for u in sim_matrix:
            if u != user:
                sim = sim_matrix[u][user]

                # 只考虑与该用户相似度为正数的用户
                if sim > 0:
                    for item in self.users[u]:
                        if item not in self.users[user] or self.users[user][item] == 0:
                            scores.setdefault(item, 0)
                            scores[item] += sim * self.users[u][item]
                            total_sims.setdefault(item, 0)
                            total_sims[item] += sim

        # 计算每个商品的推荐得分
        rankings = []
        for item, score in scores.items():
            if total_sims[item] != 0:
                rankings.append((item, round(score / total_sims[item], 2)))

        # 根据推荐得分排序，返回前 n 个商品作为推荐结果
        rankings.sort(key=lambda x: -x[1])
        return rankings
