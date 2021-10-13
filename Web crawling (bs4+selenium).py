#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import sys
import urllib.request
import requests

news_data = []
page_count = 3

client_id = "69o6i0JqwgpLM5a5v4NN"
client_secret = "dFeCQMyNQd"
encText = urllib.parse.quote("파이썬")

for idx in range(page_count):
    # json 결과
    url = "https://openapi.naver.com/v1/search/news?query=" + encText + "&start=" + str(idx * 10 + 1)
    # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if(rescode==200):
    #    response_body = response.read()
        result = requests.get(response.geturl(),
                              headers={"X-Naver-Client-Id":client_id,
                                       "X-Naver-Client-Secret":client_secret}
                             )
        news_data.append(result.json())
    #    print(response_body.decode('utf-8'))
    else:
        print("Error Code:" + rescode)


# In[2]:


#print(news_data)
print(len(news_data))
#print(news_data[0])
#print(news_data[0]['items'])
#print(len(news_data[0]['items']))
#print(news_data[0]['items'][2])
#print(news_data[0]['items'][7]['link'])


# In[3]:


naver_news_link = []

for page in news_data:
    #print(page)
    page_news_link = []
    
    for item in page['items']:
        #print(item)
        temp_link = item['link']
        #print(temp_link)
        if "naver" in temp_link:
            page_news_link.append(temp_link)
    
    naver_news_link.append(page_news_link)
        

# 사이트 확인하기에 편한 코드 구조.
for page in naver_news_link:
    for link in page:
        print(link)


# In[4]:


import pandas as pd
import numpy as np
from selenium import webdriver
from tqdm import tqdm_notebook
import requests
import pickle
import re
import ast

from bs4 import BeautifulSoup 
from urllib.request import urlopen
import urllib
import time


# In[5]:


# 가상 크롬드라이버를 불러옴.
# 윈도우 10의 경우 chromedriver.exe
driver = webdriver.Chrome('driver/chromedriver')


# In[3]:


naver_news_title = []
naver_news_content = []


for n in tqdm_notebook(range(len(naver_news_link))):
    #print(n)
    news_page_title = []
    news_page_content = []
    
    for idx in tqdm_notebook(range(len(naver_news_link[n]))):
        
        
    ########### 긁어온 URL로 접속하기 ############    
        try:
            driver.get(naver_news_link[n][idx])
            print(naver_news_link[n][idx])
            
        except:
            print("Timeout!")
            continue
        
        
        try:
            response = driver.page_source
            
        except UnexpectedAlertPresentException:
            driver.switch_to_alert().accept()
            print("게시글이 삭제된 경우입니다.")
            continue
        
        soup = BeautifulSoup(response, "html.parser")
        
        ###### 뉴스 타이틀 긁어오기 ######
        
        title = None
        
        try:
            item = soup.find('div', class_="article_info")
            title = item.find('h3', class_="tts_head").get_text()
            #print(title)

        except:
            title = "OUTLINK"
        
        #print(title)
        news_page_title.append(title)
        
        
        ###### 뉴스 본문 긁어오기 ######
        
        doc = None
        text = ""
                
        data = soup.find_all("div", {"class" : "_article_body_contents"})
        if data:
            for item in data:

                text = text + str(item.find_all(text=True)).strip()
                text = ast.literal_eval(text)
                doc = ' '.join(text)
   
        else:
            doc = "OUTLINK"
            
        news_page_content.append(doc.replace('\n', ' '))

                
    naver_news_title.append(news_page_title)
    naver_news_content.append(news_page_content)

    time.sleep(2)
    
    
print(naver_news_title[0])
print("==================================")
print(naver_news_content[0])


# In[7]:


print(naver_news_title[0])


# In[8]:


print(naver_news_content[0])


# In[9]:


print(len(naver_news_title[0]))
print(len(naver_news_content[0]))


# In[10]:


with open("naver_news_title.pk", "wb") as f:
    pickle.dump(naver_news_title, f)
    
with open("naver_news_content.pk", "wb") as f:
    pickle.dump(naver_news_content, f)

