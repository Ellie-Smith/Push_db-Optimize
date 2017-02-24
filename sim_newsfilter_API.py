# coding=utf-8
import json
import numpy
import math
import urllib2
import re

'''
    Created on Feb 22, 2017
    Updated on Feb 23, 2017
    @author: Ellie Smith
    接口说明：
        接口函数：isSimilar()
        输入：item1_id, item1_nlp_info, item2_id, item2_nlp_info
        输出：False(不相似)|True（相似）
'''

#获取
def getFeatures(item_id,item_nlp_info,lang):

    keyword_feature = item_nlp_info['keyword']['feature']
    keywords = [keyword['literal'] for keyword in keyword_feature]
    title = item_nlp_info['title_segment']['segments']
    title_postag = item_nlp_info['title_segment']['postags']

    #提取标题名词
    N_title = []
    if lang == 'indonesian':
        for i in range(0,len(title)):
            if str(title_postag[i]) == 'PROPN' or str(title_postag[i]) == 'NOUN':
                N_title.append(title[i])
    else:
        for i in range(0, len(title)):
            if str(title_postag[i]) == 'NN' or str(title_postag[i]) == 'NNP':
                N_title.append(title[i])
    #过滤关键词bug词汇
    pattern = re.compile('x[0-9A-F]{2}')
    filt_keywords = [keyword for keyword in keywords if not pattern.match(keyword)]


    seg_words = []
    if lang == 'hindi':
        for i in N_title + filt_keywords:  # 加上标题
            for word in i.split():
                seg_words.append(word)
    else:
        for i in N_title + filt_keywords:  # 加上标题
            for word in i.split():
                seg_words.append(str(word).lower())

    return keywords,seg_words,N_title

#余弦相似度（不考虑权重）
def get_cosine(words1,words2):
    word_dict = []
    for word in words1+words2:
        if word not in word_dict:
            word_dict.append(word)

    vec1 = numpy.zeros(len(word_dict))
    vec2 = numpy.zeros(len(word_dict))

    for i in words1:
        index = word_dict.index(i)
        vec1[index] = 1
    for i in words2:
        index = word_dict.index(i)
        vec2[index] = 1

    # 计算两个向量的点积和模
    x = 0
    sq1 = 0
    sq2 = 0
    for i in range(0,len(word_dict)):
        x = x + vec1[i] * vec2[i]
        sq1 = sq1 + vec1[i] * vec1[i]  # pow(a,2)
        sq2 = sq2 + vec2[i] * vec2[i]

    cos = float(x) / (math.sqrt(sq1) * math.sqrt(sq2))
    return cos

#判断两个item是否相似
def isSimilar(item1_id,item1_nlp_info, item2_id, item2_nlp_info,lang):
    # 配置阈值
    if lang == 'indonesian':
        keyword_thres, title_thres, sim = 0.04, 0.08, 0.29
    elif lang == 'hindi':
        keyword_thres, title_thres, sim = 0.04, 0.1, 0.29
    elif lang == 'english':
        keyword_thres, title_thres, sim = 0.04, 0.03, 0.24
    else:
        raise Exception("Language not found")

    #获取需要的特征
    keywords1, seg_words1, title1 = getFeatures(item1_id,item1_nlp_info, lang)
    keywords2, seg_words2, title2 = getFeatures(item2_id,item2_nlp_info, lang)

    # 若关键词数量相差太大则直接跳过
    if abs(len(keywords1) - len(keywords2)) > 3:
        return 0
    # 若第一个关键词相同，则相关度加上相应值
    if len(list(set(keywords1[:1]) & set(keywords2[:1]))) > 0:
        same_first_keyword = keyword_thres
    else:
        same_first_keyword = 0
    # 若标题相似，则相关度加上相应值
    if get_cosine(title1, title2) > 0.2:
        similar_title = title_thres
    else:
        similar_title = 0

    similarity = get_cosine(seg_words1, seg_words2) + same_first_keyword + similar_title
    # print similarity
    if similarity > sim:
        return True
    else:
        return False

# #获取item的nlp_info
# def getNLP_info(item,language):
#     # 获取文章id
#     item_id = item
#
#     if language == 'hindi':  # 印度
#         essayUrl = 'http://iflow-in.napi.ucweb.com/3/classes/recoitem/objects/%s?_app_id=a14ab4f776074435956a5819ec01ca40&_fetch=1' % (
#             str(item_id))
#     elif language == 'indonesian':  # 印尼
#         essayUrl = 'http://napi.ucweb.com/3/classes/recoitem/objects/%s?_app_id=2c1629d6b19741f88a86cc23de5203eb&_fetch=1' % (
#         str(item_id))
#     else:
#         raise Exception("Language not found")
#
#     try:
#         essay = urllib2.urlopen(essayUrl).read()
#         essay_content = json.loads(essay)
#     except:
#         print essayUrl
#         raise Exception("Url not found")
#
#     essay_content = essay_content['data']
#
#     return essay_content['nlp_info']


# if __name__ == '__main__':
#
#     nlpinfo2 = getNLP_info(625273432888426, 'hindi')
#     nlpinfo1 = getNLP_info(603044040924263, 'hindi')
#
#     print isSimilar(603044040924263,nlpinfo1,625273432888426,nlpinfo2,'hindi')

