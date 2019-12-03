# %% libs
import pandas as pd
import os
# %% Constants
COL_ARTIST = ' "artistname"'
OUTPUT_PATH = "data/base.csv"
# %% ETL init

if os.path.exists(OUTPUT_PATH):
    os.remove(OUTPUT_PATH)

df = pd.read_csv("data/df_200x2iter.csv", sep=";")

chksize = 10000
reader = pd.read_csv("scrapper/spotify_dataset.csv", sep=',',
                     header=0, chunksize=chksize, error_bad_lines=False)

list_name = list(df.artist_name)

i = 1
# %%
for chunk in reader:

    df_result = chunk[chunk[COL_ARTIST].isin(list_name)]
    df_result.to_csv(OUTPUT_PATH, sep=';', mode='a',
                     index=(i == 0), index_label=False)
    print(f"iteration number {i}")
    i += 1
    if i>450:
        break
# %%
