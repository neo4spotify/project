import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from neo4j import GraphDatabase
import squarify
import geopandas

def readHead(fileName, delimiter=";"):
    df = pd.read_csv(fileName, delimiter=delimiter, header=0)
    return df.head(3)

def visualiserVilles(df, alpha=0.2):
    df=df.copy()
    df = df.dropna()
    df['lat'] = pd.Series(pd.to_numeric(df['lat'],errors='coerce'))
    df['lng'] = pd.Series(pd.to_numeric(df['lng'],errors='coerce'))
    gdf = geopandas.GeoDataFrame(
    df, geometry=geopandas.points_from_xy(df.lng, df.lat))
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    gdf.plot(ax=world.plot(), color='red', alpha=alpha, markersize=gdf['compte']/gdf['compte'].max()*100)
    



if __name__ == "__main__":
    print("Imports réalisés")
