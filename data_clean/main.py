import os
import re

import jieba
import pandas as pd
from zhon.hanzi import punctuation

from logger import StreamLogger
from rich.progress import track

# 高频无意词
WORD = ["年", "月", "日", "还"]


def is_all_chinese(strs):
    for i in strs:
        if not '\u4e00' <= i <= '\u9fa5':
            return False
    return True


def clean(line):
    """对一个文件的数据进行清洗"""
    # 读取文件，并按行保存为list
    # 
    deleteword = open('./deletewords/weibo_deleteword.txt', 'r', encoding='utf-8').readlines()
    pattern_0 = re.compile('#.*?#')  # 在用户名处匹配话题名称
    pattern_1 = re.compile('【.*?】')  # 在用户名处匹配话题名称
    pattern_3 = re.compile('@([\u4e00-\u9fa5\w\-]+)')  # 匹配@
    pattern_4 = re.compile(u'[\U00010000-\U0010ffff\uD800-\uDBFF\uDC00-\uDFFF]')  # 匹配表情
    # pattern_5=re.compile('(.*?)')#匹配一部分颜文字
    pattern_7 = re.compile('L.*?的微博视频')
    pattern_8 = re.compile('（.*?）')
    pattern_9 = re.compile('[0-9]*')  # 匹配数字
    pattern_10 = re.compile('[a-zA-Z]')  # 匹配英文字母
    # pattern_9=re.compile(u"\|[\u4e00-\u9fa5]*\|")#匹配中文

    line = line.replace('O网页链接', '')
    line = line.replace('-----', '')
    line = line.replace('①', '')
    line = line.replace('②', '')
    line = line.replace('③', '')
    line = line.replace('④', '')
    line = line.replace('>>', '')

    line = re.sub(pattern_0, '', line, 0)  # 去除话题
    line = re.sub(pattern_1, '', line, 0)  # 去除【】
    line = re.sub(pattern_3, '', line, 0)  # 去除@

    line = re.sub(pattern_4, '', line, 0)  # 去除表情
    # print(line)
    # line=re.sub(pattern_5, '', line,0) #去除一部分颜文字
    line = re.sub(pattern_7, '', line, 0)
    line = re.sub(pattern_8, '', line, 0)
    line = re.sub(pattern_9, '', line, 0)  # 去掉数字
    line = re.sub(pattern_10, '', line, 0)  # 去掉英文字母

    line = re.sub(r'\[\S+\]', '', line, 0)  # 去除表情符号
    for i in deleteword:
        line = line.replace(i, '')
    return line


def remove_emoji(string):
    # 创建正则表达式对象，匹配所有的表情符号
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    # 使用正则表达式，去除表情符号
    return emoji_pattern.sub(r'', string)


# delete stopwords
def delete_stopwords(sourcedata, dir_path):
    StreamLogger.info("去除停用词")
    filelist = list(filter(lambda x: x.endswith('.txt'), os.listdir(dir_path)))
    for filename in filelist:
        stopword = []
        if filename.endswith('.txt'):
            StreamLogger.info("正在读取停用词文件: " + filename)
            with open('./stopwords/' + filename, 'r', encoding='UTF-8') as f:
                for line in f:
                    stopword.append(line.strip())
        StreamLogger.info("开始去除...")
        StreamLogger.info("sourcedata: " + str(len(sourcedata)) + " | stopwords: " + str(len(stopword)))
        sourcedata = [[word for word in item if word not in stopword] for item in track(sourcedata)]
    return sourcedata


if __name__ == '__main__':
    # 读取Excel文件
    StreamLogger.info("读取Excel文件...")
    excel_name = '气候变化数据清洗rawdata'
    df = pd.read_excel(excel_name + '.xlsx')

    # df change to list
    data = df['微博正文'].values.tolist()
    # 删除标点符号和特殊字符
    StreamLogger.info("删除标点符号和特殊字符")
    data = [re.sub(r'[^\w\s\u4e00-\u9fa5]', '', str(item)) for item in data]

    data = [''.join(item.split()) for item in data]
    for item in track(data):
        for i in punctuation:
            item = item.replace(i, '')

    # 删除emoji表情
    StreamLogger.info("删除emoji表情")
    data = [remove_emoji(item) for item in track(data)]
    StreamLogger.info("清洗数据")
    data = [clean(item) for item in track(data)]
    # 分词
    StreamLogger.info("分词")
    # 筛选汉字
    tmp = []
    for item in track(data):
        tmp_list = []
        # res = [if is_all_chinese(it) it for it in jieba.lcut(item)]
        for it in jieba.lcut(item):
            if is_all_chinese(it) and it not in WORD:
                tmp_list = tmp_list + [it]
        tmp.append(tmp_list)
    data = tmp

    # 去除停用词
    delete_stopwords(data, './stopwords')

    # 添加一列
    df["分词结果"] = data
    StreamLogger.info("保存文件...")
    df.to_excel("clean_" + excel_name + '.xlsx', index=False)
    # df.to_csv("clean_" + excel_name + '.csv', encoding='utf-8', index=False)
