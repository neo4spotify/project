# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 09:01:59 2019
@author: ALS
"""
import spotipy
import spotipy.util as util
import os
import json
import pandas as pd
import math
#mesure de temps
import time 
tmps1=time.time()
# Configuration de l'authentification à l'API Spotify
clientid='??????'
clientsec= '????'
username='??????'
url='http://localhost:8888/'
scope = 'user-top-read'
try:
    token = util.prompt_for_user_token(username,'user-top-read', client_id=clientid,client_secret=clientsec, redirect_uri=url)
except (AttributeError, json.decoder.JSONDecodeError):
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username,'user-top-read', client_id=clientid,client_secret=clientsec, redirect_uri=url))
# Authentification par token
sp = spotipy.client.Spotify(auth=token)

def artist_info(dataset):
    '''
    Input : Programme qui s'applique à la liste de nom d'artiste extraite du fichier spotify
    Output : Enrichi le dataframe avec l'id spotify, le genre et la popularité de l'artiste
    '''
    for name in dataset.artist_name :
        json=sp.search(q='artist:' + str(name), type='artist')
        row={}
        try:
            id_find=json['artists']['items'][0]['id']
            genres_find=json['artists']['items'][0]['genres'] 
            pop_find=json['artists']['items'][0]['popularity']
        except:
            id_find= 'NaN'
        try:
            row={'artist_id':id_find, 'artist_name':name, 'popularity':pop_find, 'genres':genres_find}
            dataset= dataset[dataset.artist_name!=name]
            dataset=dataset.append(row,ignore_index=True)
        except:
            print("fail_info")
    # L'identifiant est essentiel pour les autres requetes
    dataset_notNAN=dataset[dataset.artist_id!='NaN']
    return (dataset_notNAN)
    
def relate_art(artist,dataset): 
    '''
    Input : Id d'un artiste pour lequel on cherche les artistes similaires
    Output : Colonne du dataset d'entrée enrichie des artistes similaires + nouvelle lignes pour ces artistes s'ils n'existaient pas
    '''
    data = sp.artist_related_artists(artist)
    list_related = []
    dict_pop = {}
    dict_id = {}
    dict_genre={}
    for artist_rel in data['artists']:
        list_related.append(artist_rel['name'])
        dict_pop[artist_rel['name']] = artist_rel['popularity']
        dict_id[artist_rel['name']] = artist_rel['id']
        dict_genre[artist_rel['name']] = artist_rel['genres']
    dataset.loc[dataset.artist_id==artist,'related'] = str(list_related)
    
    for artist_rel in list_related:
        if artist_rel not in list(dataset.artist_name) :
            new_row={'artist_name':artist_rel,'popularity':dict_pop[artist_rel],'artist_id':dict_id[artist_rel],'genres':dict_genre[artist_rel]}
            dataset = dataset.append(new_row,ignore_index =True) 
    return(dataset)

def complete_related(dataset): 
    '''
    Si colonne 'related' possède valeur nulle :
        Rajoute la liste des artistes similaires
    '''
    #Séparation en 2 df pour rendre la boucle plus rapide -> Vrai ? 
    to_complete=dataset[dataset.related.isnull()]
    completed=dataset[dataset.related.notnull()]
    for i,artist in to_complete.iterrows():
        data = sp.artist_related_artists(artist.artist_id)
        related_artists = []
        for artist_rel in data['artists']:
            related_artists.append(artist_rel['name'])
        try:
            to_complete.loc[to_complete.artist_id==artist.artist_id,'related'] = str(related_artists)
        except:
            print("fail boucle1")
        dataset=pd.concat([completed,to_complete],ignore_index=True)
    return(dataset)


## __main__ :
dataset=pd.read_csv("name_sportify_dataset.csv",sep=";", header=0,nrows=10)
dataset=artist_info(dataset)
dataset=dataset[dataset.artist_id.notnull()]
# Choix du degré d'éloignement recherché entre les artistes (changer condition sur iter)
iter=0
while iter<1 :  
    for artist_id in dataset["artist_id"]:
        dataset= relate_art(artist_id,dataset)
    iter+=1
tmps2=time.time()-tmps1
print(tmps2)

dataset_complet=complete_related(dataset)
dataset_complet.to_csv("list_10.csv",sep=';',index=False,index_label=False,encoding="utf-8")
tmps3=time.time()-tmps1
print(tmps3)


#from 10rows to 175 = 32sec -> 20sec // 2 boucles-> 1337row = 151sec
#from 50rows to 755 = 150 sec -> 142sec
#From 100rows to 1403 = 268 sec (4,5min)
#From 150rows to 1996 = 52 - 385sec (6,3min)