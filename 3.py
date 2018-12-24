import codecs 
import re
import csv
import os 
import jieba
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image 
from urllib import request 
from bs4 import BeautifulSoup as bs 
from wordcloud import WordCloud,ImageColorGenerator
import matplotlib
import numpy


def read_file_as_str(file_path): 
# 判断路径文件存在
    if not os.path.isfile(file_path): 
        raise TypeError(file_path + " does not exist") 
    all_the_text = open(file_path,encoding='utf-8').read() 
    #print(all_the_text) 
    return all_the_text
	
def clean(string):
    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    filterdata = re.findall(pattern, string)
    cleaned_comments = ''.join(filterdata)
    #print(cleaned_comments)
    return cleaned_comments

def split(cleaned_comments):
    segment = jieba.lcut(cleaned_comments)
    words_df = pd.DataFrame({'segment': segment})
    stopwords = pd.read_csv("D:/stop.txt", index_col=False, quoting=3, sep="\t", names=['stopword'], encoding='utf-8') 
    words_df = words_df[~words_df.segment.isin(stopwords.stopword)]
    print(words_df)
    return words_df



def draw(words_df):
    bg_pic = numpy.array(Image.open("abc2.jpg"))
    words_stat = words_df.groupby(by=['segment'])['segment'].agg({"计数": numpy.size})
    words_stat = words_stat.reset_index().sort_values(by=["计数"], ascending=False)
    wordcloud = WordCloud( font_path="simhei.ttf", background_color="white", max_font_size=100, width = 2000, height = 1800, mask = bg_pic, mode = "RGBA" )
    word_frequence = {x[0]: x[1] for x in words_stat.head(1000).values}
    wordcloud = wordcloud.fit_words(word_frequence) 
    image_colors = ImageColorGenerator(bg_pic) # 根据图片生成词云颜色 
    plt.imshow(wordcloud) #显示词云图片
    plt.axis("off") #显示坐标轴
    plt.show()
    wordcloud.to_file('show_Chinese.png') # 把词云保存下来
	
def main():
    original_text=read_file_as_str('D:/test.txt')
    cleaned_text=clean(original_text)
    splited_text=split(cleaned_text)
    draw(splited_text)
	
if __name__=="__main__" :
    main()