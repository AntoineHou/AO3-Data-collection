# -*- coding: utf-8 -*-
"""
Created on Fri May 27 16:40:04 2022

@author: antoi
"""
import requests 
from bs4 import BeautifulSoup
import time 
from progress.bar import Bar

url_base_search = 'https://archiveofourown.org/tags/{}/works?commit=Sort+and+Filter&page={}&work_search%5Bcomplete%5D=T&work_search%5Bcrossover%5D=F&work_search%5Bdate_from%5D=&work_search%5Bdate_to%5D=&work_search%5Bexcluded_tag_names%5D=&work_search%5Blanguage_id%5D=en&work_search%5Bother_tag_names%5D=&work_search%5Bquery%5D=&work_search%5Bsort_column%5D=hits&work_search%5Bwords_from%5D=&work_search%5Bwords_to%5D='
nb_stories = int(1000)/10

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


def get_stories_ids (url_base , page ,tag) :
    page=requests.get(url_base.format(tag ,str(page)))
    soup = BeautifulSoup(page.text,"html.parser")
    stories = soup.find_all('ol')[1]
    stories = stories.find_all('li')
    stories = str(stories).split('id')
    stories = [i for i in stories if i.startswith('="work_')]
    stories_id = []
    for items in stories : 
        stories_id.append(int(find_between(items , '="work_' , '"')))
    print(page  )
    print('------------------------------------------------')
    print(stories_id)
    return stories_id

def id_ao3 (tag , url_base , nb_page ):
    s=[]
    bar = Bar('Processing', max=nb_page)
    for i in list(range(1,nb_page+1, 1 )):
            s.extend(get_stories_ids(url_base_search , i , tag))
            
            time.sleep(5)
    with open(r'a3_id_' + tag.split(' ')[0]+  '.txt', 'w') as fp:
        for item in s:
            fp.write("%s\n" % item)


