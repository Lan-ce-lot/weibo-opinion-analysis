# python3
#coding='utf-8'
from importlib import reload
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from gensim import corpora,similarities,models
from gensim.models import LdaModel
from gensim.corpora import Dictionary
#from ldamattle import LdaMallet#导入mallet

import pyLDAvis.gensim_models
import sys
sys.path.append('..')
from logger.config import StreamLogger
import matplotlib.pyplot as plt
from gensim.models import CoherenceModel

from rich.progress import track
# from LDA import infile,deal,run,save_visual

def infile(fliepath):
    #输入分词好的TXT，返回train
    '''
    all=[]
    with open(fliepath,'r',encoding='utf-8')as f:
        all_1=list(f.readlines())#列表
        for i in all_1:#一句
            i=i.strip()#去除占位符
            if i:
                all=all+i.split(' ')

    #字典统计词频
    dic={}
    for key in all:
        dic[key]=dic.get(key,0)+1
    #print(dic)
    #清除词频低的词
    all_2=[]#低词频列表
    for key,value in dic.items():
        if value<=5:
            all_2.append(key)
    '''
    StreamLogger.info('formatting data...')
    train = []
    with open(fliepath,'r',encoding='utf-8') as f:
        # f to string
        for i in f.readlines():
            i = i.strip()
            i = i.replace("'", '')
            i = i.replace(' ', '')
            # i = i.replace('\n', '')
            new_line=[]
            if len(i)>1:
                i = i.strip().split(',')
                for w in i:
                    if len(w)>1:
                        new_line.append(w)
            train.append(new_line)
    return train

def deal(train):
    #输入train，输出词典,texts和向量
    StreamLogger.info('creating dictionary...')
    id2word = corpora.Dictionary(train)     # Create Dictionary
    texts = train                           # Create Corpus
    corpus = [id2word.doc2bow(text) for text in texts]   # Term Document Frequency

    #使用tfidf
    tfidf = models.TfidfModel(corpus)
    corpus = tfidf[corpus]

    id2word.save('tmp/deerwester.dict') #保存词典
    corpora.MmCorpus.serialize('tmp/deerwester.mm', corpus)#保存corpus

    return id2word,texts,corpus

'''
# Build LDA model
lda_model = LdaModel(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=10, 
                                           random_state=100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=10,
                                           alpha='auto',
                                           per_word_topics=True)
# Print the Keyword in the 10 topics
print(lda_model.print_topics())
doc_lda = lda_model[corpus]
'''

def run(corpus_1,id2word_1,num,texts):
    StreamLogger.info('running LDA...')
    #标准LDA算法
    lda_model = LdaModel(corpus=corpus_1, 
                         id2word=id2word_1,
                        num_topics=num,
                       passes=60,
                       alpha=(50/num),
                       eta=0.01,
                       random_state=42)
    # num_topics：主题数目
    # passes：训练伦次
    # num：每个主题下输出的term的数目
    #输出主题
    #topic_list = lda_model.print_topics()
    #for topic in topic_list:
        #print(topic)
    # 困惑度
    perplex=lda_model.log_perplexity(corpus_1)  # a measure of how good the model is. lower the better.
    # 一致性
    coherence_model_lda = CoherenceModel(model=lda_model, texts=texts, dictionary=id2word_1, coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()
    #print('\n一致性指数: ', coherence_lda)   # 越高越好
    return lda_model,coherence_lda,perplex

def save_visual(lda,corpus,id2word,name):
    #保存为HTML
    d=pyLDAvis.gensim_models.prepare(lda, corpus, id2word)
    pyLDAvis.save_html(d, name+'.html')#可视化


#超参搜索的形式探索最佳主题数,对于暴力搜索可以一开始设置区间较大，步伐较大，目的是锁定大致区间范围，而后在小区间范围内精细化搜索。
def compute_coherence_values(dictionary, corpus, texts,start, limit, step):
    """
    Compute c_v coherence for various number of topics

    Parameters:
    ----------
    dictionary : Gensim dictionary
    corpus : Gensim corpus
    texts : List of input texts
    limit : Max num of topics

    Returns:
    -------
    model_list : List of LDA topic models
    coherence_values : Coherence values corresponding to the LDA model with respective number of topics
    """
    StreamLogger.info('computing coherence values...')
    coherence_values = []
    perplexs=[]
    model_list = []
    for num_topic in track(range(start, limit, step)):
        #模型
        lda_model,coherence_lda,perplex=run(corpus,dictionary,num_topic,texts)
        #lda_model = LdaModel(corpus=corpus,num_topics=num_topic,id2word=dictionary,passes=50)
        model_list.append(lda_model)
        perplexs.append(perplex)#困惑度
        #一致性
        #coherence_model_lda = CoherenceModel(model=lda_model, texts=texts, dictionary=dictionary, coherence='c_v')
        #coherence_lda = coherence_model_lda.get_coherence()
        coherence_values.append(coherence_lda)

    return model_list, coherence_values,perplexs

def show_1(dictionary,corpus,texts,start,limit,step):
    #从 5 个主题到 30 个主题，步长为 5 逐次计算一致性，识别最佳主题数
    StreamLogger.info("开始计算一致性")
    model_list, coherence_values,perplexs = compute_coherence_values(dictionary, corpus,texts, start, limit, step)
    #输出一致性结果
    n=0
    # rich progress bar

    for m, cv in zip(perplexs, coherence_values):
        print("主题模型序号数",n,"主题数目",(n+4),"困惑度", round(m, 4), " 主题一致性", round(cv, 4))
        n=n+1
    #打印折线图
    x = list(range(start, limit, step))
    #困惑度
    plt.plot(x, perplexs)
    plt.xlabel("Num Topics")
    plt.ylabel("perplex  score")
    plt.legend(("perplexs"), loc='best')
    plt.show()
    #一致性
    plt.plot(x, coherence_values)
    plt.xlabel("Num Topics")
    plt.ylabel("Coherence score")
    plt.legend(("coherence_values"), loc='best')
    plt.show()
    
    return model_list

def choose(model_list,n):
    # 选择最佳主题并输出，一致性最高的
    optimal_model = model_list[n]
    model_topics = optimal_model.show_topics(formatted=False)
    #print(model_topics)
    return optimal_model

#反过来给每个博文打上主题标签
def format_topics_sentences(optimal_model, corpus, texts):
    # Init output
    sent_topics_df = pd.DataFrame()
    # Get main topic in each document
    for i, row in enumerate(optimal_model[corpus]):
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = optimal_model.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

    # Add original text to the end of the output
    contents = pd.Series(texts)
    sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)

    return sent_topics_df

def show_2(optimal_model, corpus, texts,name):
    #输出每个博文的主题标签，以便计算热度
    df_topic_sents_keywords = format_topics_sentences(optimal_model, corpus, texts)
    # 格式化
    df_dominant_topic = df_topic_sents_keywords.reset_index()
    df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text']
    #打印
    df_dominant_topic.head(10)
    #保存
    df_dominant_topic.to_excel('推文话题标签\\'+name+'.xlsx')

    return df_topic_sents_keywords

def show_3(df_topic_sents_keywords,name):
    #展示各个主题的关键词列表以及每个主题的代表性新闻内容
    sent_topics_sorteddf_mallet = pd.DataFrame()
    sent_topics_outdf_grpd = df_topic_sents_keywords.groupby('Dominant_Topic')
    for i, grp in sent_topics_outdf_grpd:
        sent_topics_sorteddf_mallet = pd.concat([sent_topics_sorteddf_mallet, 
                                             grp.sort_values(['Perc_Contribution'], ascending=[0]).head(1)], 
                                            axis=0)
    # Reset Index    
    sent_topics_sorteddf_mallet.reset_index(drop=True, inplace=True)
    # Format
    sent_topics_sorteddf_mallet.columns = ['Topic_Num', 'Topic_Perc_Contrib', 'Keywords', 'Text']
    # Show
    sent_topics_sorteddf_mallet.to_excel('主题关键词\\'+name+'.xlsx')

def show_4(df_topic_sents_keywords,name):
    #LDA 给出的标签下，各个主题的新闻数以及占比情况,利于计算热度
    # Number of Documents for Each Topic
    topic_counts = df_topic_sents_keywords['Dominant_Topic'].value_counts()
    # Percentage of Documents for Each Topic
    topic_contribution = round(topic_counts/topic_counts.sum(), 4)
    # Topic Number and Keywords
    topic_num_keywords = df_topic_sents_keywords[['Dominant_Topic', 'Topic_Keywords']].drop_duplicates().reset_index(drop=True)
    # Concatenate Column wise
    df_dominant_topics = pd.concat([topic_num_keywords, topic_counts, topic_contribution], axis=1)
    # Change Column names
    df_dominant_topics.columns = ['Dominant_Topic', 'Topic_Keywords', 'Num_Documents', 'Perc_Documents']
    df_dominant_topics.sort_values(by="Dominant_Topic", ascending=True, inplace=True)
    # Show
    print(df_dominant_topics)
    #保存
    df_dominant_topics.to_excel('主题新闻数\\'+name+'.xlsx')
    return df_dominant_topics

if __name__ == '__main__':
    # with open('气候变化202101.txt','r',encoding='utf-8') as f:
    filename = '气候变化202101.txt'
    train = infile(filename)
    name=filename.replace('.txt','')#后续结果文件名
    # print(train)
    StreamLogger.info('数据读取完成')
    # StreamLogger.info(train[:10])
    id2word,texts,corpus=deal(train)  
    model_list=show_1(id2word,corpus,texts,4,16,1)#找出困惑度和主题一致性最佳的，最好是不超过20个主题数,10个为宜
    n=input('输入指定模型序号，以0为第一个: ')#还是需要手动，权衡比较
    optimal_model=choose(model_list,int(n))
    #主题列表
    topic_list = optimal_model.print_topics()
    #保存主题
    
    # f=open('主题txt\\'+name+'.txt','w',encoding='utf-8')
    with open(name+'_topic.txt','w',encoding='utf-8') as f:
        for t in topic_list:
            f.write(' '.join(str(s) for s in t) + '\n')
    df_topic_sents_keywords=show_2(optimal_model,corpus,texts,name)
    show_3(df_topic_sents_keywords,name)
    df_dominant_topics=show_4(df_topic_sents_keywords,name)
    save_visual(optimal_model,corpus,id2word,name)#可视化
