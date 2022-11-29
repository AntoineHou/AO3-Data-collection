# -*- coding: utf-8 -*-
"""
Created on Tue May 31 15:01:00 2022

@author: antoi
"""

import urllib.request
import time 
from bs4 import BeautifulSoup
import xml.etree.ElementTree 
from time import strptime

headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'}

def remove_tags(text):
    text = ''.join(xml.etree.ElementTree.fromstring(text).itertext())
    return text.replace('\n' ,'')


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def open_fic(work_id, headers):
    time.sleep(5)
    url = 'https://archiveofourown.org/works/' + work_id + '?view_adult=true&show_comments=true&view_full_work=true'
    try : 
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req)
        bs = BeautifulSoup(resp, 'html.parser')
    except :
        try  : 
            print("HTTP Error.")
            time.sleep(5)
            req = urllib.request.Request(url, headers=headers)
            resp = urllib.request.urlopen(req)
            bs = BeautifulSoup(resp, 'html.parser')
        except :
            bs = ''
        
    time.sleep(5)
    return bs


def page_limit (bs): 
    if int(bs.find('li', {'class':'next'}).previous_sibling.previous_sibling.text) and int(bs.find('li', {'class':'next'}).previous_sibling.previous_sibling.text) == 1 : 
        return 1
    elif int(bs.find('li', {'class':'next'}).previous_sibling.previous_sibling.text) and int(bs.find('li', {'class':'next'}).previous_sibling.previous_sibling.text) > 1  : 
        return 2
    else : 
        return 0

def compile_comments(bs):
    l_comments = {}
    div = bs.find_all('li' , {'role' : "article"})
    for result in div:  
        try : 
            user = find_between(str(result.find('a')) , '/users/' , '/pseuds/')
            text = remove_tags(str(result.find('blockquote', {'class':'userstuff'})))
            id_ = find_between(str(result.find('li')) , ';id=' , '&')
            date= str(strptime(remove_tags(str(result.find('abbr' , {'class' : 'month'}))),'%b').tm_mon)+'-'+remove_tags(str(result.find('span' , {'class' : 'date'})))+'-'+remove_tags(str(result.find('span' , {'class' : 'year'})))
            if 'Parent Thread' in str(result)  : 
                parent=find_between(str(result) , '<li><a href="/comments/' , '">Thread</a></li>')
                parentality = 'Response'
            else : 
                parent = None 
                parentality = 'Parent'
            l_comments [id_] = {'text' : text , 'parentality' : parentality , 'parent' : parent, 'date': date  , 'user' : user}     
        except xml.etree.ElementTree.ParseError : 
            print("XML_Parsing_Error")
    return l_comments


def turn_page_comments(bs, work_id, headers, start_page = 1):
    page_limit = int(bs.find('li', {'class':'next'}).previous_sibling.previous_sibling.text)
    pages= list(range(1, page_limit+1))
    out = {}
    for i in pages :
        url = 'https://archiveofourown.org/works/' + work_id + '?page=' + str(i) + '&show_comments=true&view_adult=true&view_full_work=true'
        try:
            time.sleep(6)
            req = urllib.request.Request(url, headers=headers)
            resp = urllib.request.urlopen(req)
            bs = BeautifulSoup(resp, 'lxml')
            
            out.update(compile_comments(bs))
        except :
            time.sleep(6)
            print("Error_Page_"+str(i))
    return out

def main_comment (work_id , headers) : 
    bs = open_fic(work_id , headers)
    limit = int(page_limit(bs))
    if limit == 2 : 
        t=turn_page_comments(bs ,work_id , headers , 1)
    elif  limit == 1: 
        t=compile_comments(bs)
    else : 
        t = []
    return t

