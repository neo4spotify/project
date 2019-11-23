import pandas as pd
import time 
tmps1=time.time()
df = pd.read_csv("../data/df_200x2iter.csv",sep=";")

chksize, n = 10000, 40000
reader = pd.read_csv("spotify_dataset.csv",sep=',', header=0, chunksize=chksize, error_bad_lines=False, nrows=n)

df_result=pd.DataFrame()
list_name=list(df.artist_name)

i=1
for chunk in reader :
    mask = (chunk[' "artistname"'] in list_name).all(out=True , axis=1)
    df_result=chunk[mask]
    df_result.to_csv("../data/chunks.csv",sep=';',mode='a',index=False,index_label=False)
    print(i)
    i+=1
      
tmps2=time.time()-tmps1
print(f"for {n/chksize} chunks: {itmps2} sec")