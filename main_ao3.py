# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 15:28:02 2022

@author: antoi
"""
import os 
os.chdir('C:/Users/antoi/.spyder-py3/ao3')
from ao3 import * 
from commentary_ao3 import * 
from metadata_ao3 import * 
import json 
from progress.bar import Bar


tag_list = ['Bruce Wayne',
'Pocket Monsters | Pokemon - All Media Types',
'Naruto',
'Final Fantasy Series',
'Fullmetal Alchemist - All Media Types',
'僕のヒーローアカデミア | Boku no Hero Academia | My Hero Academia',
'Avatar: The Last Airbender',
'Marvel Cinematic Universe',
'Captain America - All Media Types',
'Marvel',
'Teen Wolf (TV)',
'Harry Potter - J*d* K*d* Rowling',
'Star Wars - All Media Types',
'Star Trek',
'Doctor Who',
'Sherlock (TV)']

#Naruto

for tag in tag_list : 
    id_ao3(tag , url_base_search , nb_page)
    
    with open('a3_id_' +  tag.split(' ')[0] +  '.txt') as f:
        id_to_scrap = f.readlines()
    
    bar = Bar('Metada_Processing', max=len(id_to_scrap))
    
    for ID in id_to_scrap : 
        time.sleep(3)
        result_metadata = parse_data(str(ID[:-1]), headers)
        bar.next()
        with open('result_ao3_metadata_' + str(ID[:-1]) + '.json', 'w') as fp:
            json.dump(result_metadata, fp , default=str)
            
    
    id_comments= id_to_scrap[:10]
    bar = Bar('Metada_Processing', max=len(id_comments))
    
    
    for ID in id_comments:
         try : 
             result_comments = {'ID' : ID , 'Fandom' : tag ,  'Comments' : main_comment(str(ID[:-1]), headers)}
         except : 
             time.sleep(10)
             try  : 
                 result_comments = {'ID' : ID , 'Fandom' : tag ,  'Comments' : main_comment(str(ID[:-1]), headers)}
             except :
                 pass 
         bar.next()
         with open('result_ao3_comments_' + str(ID[:-1]) + '.json', 'w') as fp:
             json.dump(result_comments, fp , default=str)
    