# %% 
API_KEY = "YOUR_API_KEY"
#%%
import googlemaps
import pandas as pd
gmaps = googlemaps.Client(key=API_KEY)

# %%
data=[]
df = pd.read_csv("data/concerts.csv", header=0, delimiter="|")
for ville in df.ville.unique():
    try:
        geocode_result = gmaps.geocode(ville)
        loc = geocode_result[0]["geometry"]["location"]
        data.append([ville, loc['lat'], loc['lng']])
    except:
        print("error")
# %%
locs = pd.DataFrame(data)
locs.columns = ["ville", "lat", "lng"]

locs.to_csv("data/villes.csv", sep="|")
locs.head()



# %%
