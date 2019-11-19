import spotipy
import spotipy.util as util
import os
import json
import pandas as pd
import math
import time 

def auth():
    '''
    Generate token for authentification for Spotidy API
    '''
    clientid='????'
    clientsec= '????'
    username='????'
    url='????'
    scope = 'user-top-read'

    try:
        token = util.prompt_for_user_token(username,'user-top-read', client_id=clientid,client_secret=clientsec, redirect_uri=url)
    except (AttributeError, json.decoder.JSONDecodeError): 
        os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(username,'user-top-read', client_id=clientid,client_secret=clientsec, redirect_uri=url)
    return(token)

# Global variable
col_artists ='artists'
col_item='items'
col_id='id'
col_genres='genres'
col_popularity='popularity'
col_name='name'
col_related='related'
limit_related=10

def artist_info(dataset):
    ''' Based on the name, find ID, popularity and genres of an artist defined by Spotify
    Arguments: Dataframe including a column "artist_name"
    Returns : A dataframe with added columns "artist_id", "popularity" and "genres"
    '''
    global col_artists 
    global col_item
    global col_id
    global col_genres
    global col_popularity
    for name in dataset.artist_name :
        json=sp.search(q='artist:' + str(name), type='artist')
        row={}
        try:
            id_find=json[col_artists ][col_item][0][col_id]
            genres_find=json[col_artists][col_item][0][col_genres] 
            pop_find=json[col_artists][col_item][0][col_popularity]
        except:
            id_find= 'NaN'
        row={'artist_id':id_find, 'artist_name':name, 'popularity':pop_find, 'genres':genres_find}
        dataset= dataset[dataset.artist_name!=name]
        dataset=dataset.append(row,ignore_index=True)
    # ID is essential for other spotify queries
    dataset_notNAN=dataset[dataset.artist_id!='NaN']
    return (dataset_notNAN)
    
def relate_art(artist,dataset): 
    ''' Add related artists and add new rows for new artists
    Arguments: The dataframe and the id of an artist on which we're looking for related artists
    Returns: Dataframe with added column "related" and new rows for related artists not present in the dataframe
    '''
    global col_artists 
    global col_id
    global col_genres
    global col_popularity
    global col_name
    global col_related
    global limit_related
    list_related = []
    dict_pop = {}
    dict_id = {}
    dict_genre={}
    data = sp.artist_related_artists(artist)
    nb=0
    # Limit of 10 or below related artists for performance
    while ( (nb < len(data[col_artists])) and (nb < limit_related) ):     
        dict_pop[data[col_artists][nb][col_name]] = data[col_artists][nb][col_popularity]
        dict_id[data[col_artists][nb][col_name]] = data[col_artists][nb][col_id]
        dict_genre[data[col_artists][nb][col_name]] = data[col_artists][nb][col_genres]
        try:
            list_related.append(data[col_artists][nb][col_name])
        except:
            print(str(data[col_artists][nb][col_name]) + 'no related')
        nb+=1
    dataset.loc[dataset.artist_id == artist , col_related] = str(list_related) 
       
    for artist_rel in list_related:
        if artist_rel not in dataset.artist_name :
            new_row={'artist_name':artist_rel, 'popularity':dict_pop[artist_rel], 'artist_id':dict_id[artist_rel], 'genres':dict_genre[artist_rel]}
            dataset = dataset.append(new_row,ignore_index =True) 
    return(dataset)

def complete_related(dataset): 
    ''' Fullfil "related" column without adding new rows
    Arguments: Dataframe with some artists whom don't have related artists
    Returns: Dataframe with every value complete
    '''
    global col_artists 
    global col_name
    global col_related
    global limit_related
    # Separation into 2 dataframe for optimization 
    to_complete=dataset[dataset.related.isnull()]
    completed=dataset[dataset.related.notnull()]
    for i,artist in to_complete.iterrows():
        data = sp.artist_related_artists(artist.artist_id)
        related_artists = []
        nb=0
        # Limit of 10 or below related artists for performance
        while ( (nb < len(data[col_artists])) and (nb < limit_related) ): #
            try:
                related_artists.append(data[col_artists][nb][col_name])
            except:
                related_artists = []
            nb+=1
        to_complete.loc[to_complete.artist_id == artist.artist_id , col_related] = str(related_artists)
    dataset=pd.concat([completed,to_complete],ignore_index=True)
    return(dataset)

    
if __name__ == '__main__':
    # Authentification by token
    token=auth()
    sp = spotipy.client.Spotify(auth=token)

    tmps1=time.time()
    dataset=pd.read_csv("./data/name_spotify_dataset.csv",sep=";", header=0,nrows=200)
    dataset=artist_info(dataset)
    # iter refers to the degree of distance between artists (for iter=2 -> related of related artists)
    iter=0
    while iter<1 :  
        for artist_id in dataset["artist_id"]:
            dataset= relate_art(artist_id,dataset)
        iter+=1
        
    dataset.to_csv("./data/df_incomplete.csv",sep=';',index=False,index_label=False,encoding="utf-8")
    tmps2=time.time()-tmps1
    print(tmps2)

    dataset_complet=complete_related(dataset)
    dataset_complet.to_csv("./data/df_.csv",sep=';',index=False,index_label=False,encoding="utf-8")
    tmps3=time.time()-tmps1
    print(tmps3)

