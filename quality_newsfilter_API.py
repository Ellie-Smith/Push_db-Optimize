# coding=utf-8

'''
    Created on Feb 22, 2017
    Updated on Feb 23, 2017
    @author: Ellie Smith
    接口说明：
        接口函数：isLowquality()
        输入：item_id, nlp_info, raw_item
        输出：False(不过滤)|True（过滤）
'''

def Content_segment(nlp_info):
    content = []
    content_seg = nlp_info['content_segment']
    for seg in content_seg:
        content.extend(seg['segments'])
    return content

def Image(raw_item):
    return raw_item['image']

def isLowquality(item_id,nlp_info,raw_item):
    # content = Content_segment(nlp_info)
    # image = Image(raw_item)
    if len(Content_segment(nlp_info)) <= 20 and len(Image(raw_item)) == 0:
        return True
    else:
        return False
