import math
import jieba


# 计算每个词出现的次数
def term_frequency(term, document):
    return document.count(term)


# 计算倒排文档频率
def inverse_document_frequency(term, all_documents):
    num_documents_with_term = len([d for d in all_documents if term in d])
    if num_documents_with_term > 0:
        return float(1 + math.log(float(len(all_documents)) / num_documents_with_term))
    else:
        return 0


# 计算余弦相似度
def cosine_similarity(doc1, doc2, all_documents):
    terms_doc1 = set(doc1)
    terms_doc2 = set(doc2)
    common_terms = terms_doc1 & terms_doc2

    numerator = sum(
        [term_frequency(term, doc1) * term_frequency(term, doc2) * inverse_document_frequency(term, all_documents) ** 2
         for term in common_terms])

    denominator = math.sqrt(
        sum([term_frequency(term, doc1) ** 2 * inverse_document_frequency(term, all_documents) ** 2 for term in
             terms_doc1])) * \
                  math.sqrt(
                      sum([term_frequency(term, doc2) ** 2 * inverse_document_frequency(term, all_documents) ** 2 for
                           term in terms_doc2]))

    if denominator == 0:
        return 0
    else:
        return float(numerator) / denominator
#
# 词项频率（Term frequency）：计算文档中每个词出现的次数。
#
# 倒排文档频率（Inverse document frequency）：计算一个词在整个文档集合中出现的频率，并用一个公式将其转换为一个权重，以表示该词在文档中的重要性。
#
# 余弦相似度（Cosine similarity）：比较两个文档之间的相似性，通过计算它们之间共同出现的词项的权重来确定它们之间的相似程度。