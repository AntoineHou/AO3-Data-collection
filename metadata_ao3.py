import AO3
import time
import urllib.request
from bs4 import BeautifulSoup
import os
import json
os.chdir('C:/Users/antoi/.spyder-py3/ao3')

def get_work (work_id) : 
    work = AO3.Work(work_id)
    work.load_chapters()
    return work

headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'}

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def get_chapter_update (work_id , headers) : 
    try : 
        req = urllib.request.Request('https://archiveofourown.org/works/{}/navigate'.format(work_id), headers=headers)
        time.sleep(5)
        resp = urllib.request.urlopen(req)
        bs = BeautifulSoup(resp, 'lxml')
        dates = bs.find_all(class_ = 'datetime')
        dates_str=[]
        for d in dates : 
            dates_str.append(find_between(str(d),'(',')'))
        return dates_str 
    except :
        return None 

def parse_data (work_id,headers) : 
    
    time.sleep(5)
    
    try : 
        work = get_work(work_id)
        
        DICT_DATA = {'ID' : work_id ,'Authors' : None, 'Publishing Date' : None, 'Last Edit Date' :None 
                     ,'Bookmarks' :None, 'Comments' :None , 'Chapter' :None , 'Fandom' :None
                     , 'Hits' : None , 'Kudos': None , 'Words' : None , 'Dates_Update_Chapter': None}
        AUTHORS = []
        if work.authors : 
            for a in work.authors : 
                try : 
                    AUTHORS.append(a.username)
                except :
                    pass
                
        FANDOMS = []
        
        if work.fandoms : 
            for a in work.fandoms : 
                try : 
                    FANDOMS.append(a)
                except : 
                    pass 
                
        DICT_DATA['Dates_Update_Chapter'] = get_chapter_update(work_id , headers)
                
        DICT_DATA['Authors'] = AUTHORS        
        DICT_DATA['Fandom'] = FANDOMS
        
        if work.date_published : 
            DICT_DATA['Publishing Date']  = work.date_published
            
        if work.date_edited and work.date_edited != work.date_published : 
            DICT_DATA['Last Edit Date']  = work.date_edited
        
        if work.bookmarks : 
            DICT_DATA['Bookmarks'] = work.bookmarks
        
        if work.comments : 
            DICT_DATA['Comments'] = work.comments
            
        if work.expected_chapters : 
            DICT_DATA['Chapter'] = work.expected_chapters
        
        if work.expected_chapters : 
            DICT_DATA['Chapter'] = work.expected_chapters
            
        if work.hits : 
            DICT_DATA['Hits'] = work.hits
            
        if work.kudos : 
            DICT_DATA['Kudos'] = work.kudos
            
        if work.words : 
            DICT_DATA['Words'] = work.words
            
        return DICT_DATA
    except : 
        return {}

# open file with work_id
with open('a3_id_Marvel.txt') as f:
    work_id = f.readlines()

for i in work_id :
    i = i[:-1]
    dict_data = parse_data(i,headers)
    # export data in a json file
    
    name = "data_Marvel_" + str(i) + ".json"
    
    with open(name, "w") as outfile:
        json.dump(dict_data, outfile ,default=str)
    print('Work_id : {}'.format(i))
    print('Data : {}'.format(dict_data))
    print('\n')
    time.sleep(5)