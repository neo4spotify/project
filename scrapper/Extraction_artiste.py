# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 09:57:20 2019
@author: ALS
"""
import pandas as pd
import time 
tmps1=time.time()

list_name=[]
reader = pd.read_csv("spotify_dataset.csv",sep=',',header=0,chunksize=500,error_bad_lines=False, nrows=1000)
for chunk in reader:
    for artist_name in chunk[' "artistname"'] :
        try:
            row=artist_name
            list_name.append(row)
        except :
            print("error")
    
tmps2=time.time()-tmps1
print(tmps2)

df_name=pd.DataFrame(list_name , columns=["artist_name"])
df_name=df_name.drop_duplicates()
df_name.to_csv("name_spotify_dataset.csv",sep=';',index=False,index_label=False, header=True)    