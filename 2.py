import requests
import time
from pyquery import PyQuery as pq
import re
from urllib.parse import urlencode
import csv
 
base_url="https://book.douban.com/subject/27614904/comments/new?p="
 
headers={
 'Cookie':'"bid=r23sYcJjE7M; douban-fav-remind=1; ll="108288"; __utmc=30149280; _ga=GA1.2.801253780.1539013028; ps=y; push_noty_num=0; push_doumail_num=0; __utmv=30149280.14175; gr_user_id=b57fcf68-9a41-4ca6-926c-96f4f9032432; _vwo_uuid_v2=D30CE869A83F1DB8F9C84C711E9384DB8|ff924a5e3d4f893d6804df891b6eac0e; ct=y; __utmz=30149280.1544371627.11.10.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/login; ap_v=0,6.0; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1544534073%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DX4Zy9_ahj7t1b1pWbEgFP0-TqK3PK0Kh0MADWXe0Q7P4URxTeI7BBaF7HnoLiYXy%26wd%3D%26eqid%3D8a17aced0000a220000000025c0d20bd%22%5D; _pk_ses.100001.8cb4=*; __utma=30149280.801253780.1539013028.1544371627.1544534080.12; __utmt=1; _gid=GA1.2.427362289.1544534091; _gat_UA-7019765-1=1; ck=Av0B; _pk_id.100001.8cb4=05aa1ea65bfceefe.1539013027.12.1544534112.1544373066.; __utmb=30149280.6.10.1544534080',
   }
 
def save_to_csv(list):
    with open('E:/test.csv','a',encoding='utf-8',newline='')as f:
        print(list)
        headers = ['Symbol']
        rows = [(list)]
        writer = csv.writer(f)
        #writer.writerow(headers)
        writer.writerow(rows)

def save_to_txt(list):
    with open("E:/test.txt","a",encoding='utf-8') as f:
        f.write(list)
 
def parse_content(html):
    doc = pq(html)  # 得到网页源码
    contents = doc('.comment-item p').items()
    return contents
 
def get_page_html(page):
    pages='%d' %page
    url=base_url+pages
    html=get_html(url)
    return html
 
#解析html页面
def get_html(url):
    print('crawing ', url) # 输出正在爬去的url
    response = requests.get(url,headers=headers)
    time.sleep(1)  # 暂停一秒
    return response.text
 
#获取总的评论的条数
def parse_comment(html):
    doc=pq(html) # 得到网页源码
    num=doc('div.nav-tab.title_line.clearfix > span#total-comments').text()#获取span标签的内容
    num=re.findall('\d+',num)[0]
    return num
 
def main():
    comment_list=[]
    print("start")
    index_html=get_html("https://book.douban.com/subject/27614904/comments/new")
    total_num=parse_comment(index_html)
    print ("共有%s条评论" %total_num)
    pagenum=int(total_num)/20+1
    print("共有%d页"%pagenum)
    for page in range(1, int(pagenum)):
         #print('page= '+str(page))
         save_to_txt("-------------------第%s页--------------------------------------"%str(page))
         page_html=get_page_html(page)
         if page_html:
             contents=parse_content(page_html)
             for content in contents:
                 save_to_csv(content.text())
    
 
 
 
if __name__=="__main__" :
    main()
