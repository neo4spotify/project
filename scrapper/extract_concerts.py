# %% Imports
import pandas as pd
import grequests
from bs4 import BeautifulSoup
import time
import csv
import urllib.parse


# %% Constants
INPUT_PATH = "data/chunks.csv"
OUTPUT_PATH = "data/concerts.csv"
# %% Read artists
df = pd.read_csv(INPUT_PATH, sep=";")
artists = df[' "artistname"'].unique()

# %% Def functions


def chunks(l, n):
    """Divise une liste en une liste de chunk

    Arguments:
        l {list} -- La liste à découper 
        n {int} -- La taille maximale de chaque chunk

    Returns:
        [list] -- la liste de chunks
    """
    n = max(1, n)
    return (l[i:i+n] for i in range(0, len(l), n))


def scrapArtist(responses):
    """Gère les retours HTTP des concerts des artiste et enregistre les données dans un fichier CSV

    Arguments:
        responses {list} -- La liste des réponses HTTP à traiter
    Returns:
        [list] -- [une liste d'informations sur les concerts]
    """
    numberCorrect = 0
    result = []
    for r in responses:
        try:
            if str(r) != 'None':
                soup = BeautifulSoup(r.text, 'lxml')
                for row in soup.findAll('table')[0].tbody.findAll('tr'):
                    first_column = row.findAll('td')[0].contents
                    second_column = row.findAll('td')[1].find(
                        "strong").find("a").contents
                    third_column = row.findAll('td')[2].findAll("a")
                    fourthColumn = row.findAll('td')[3].findAll("a")
                    res = [urllib.parse.unquote(
                        r.url[63:]), first_column[0][0:12], second_column[0]]
                    if len(third_column) > 0:
                        res.append(third_column[0].contents[0])
                    else:
                        res.append("NA")
                    if len(fourthColumn) > 0:
                        res.append(fourthColumn[0].contents[0])
                    else:
                        res.append("NA")
                    result.append(res)
                numberCorrect += 1
        except:
            try:
                print(f"URL en erreur : {r.url}")
            except:
                print("Erreur inconnue")

    print(f"Correctly scrapped {numberCorrect} artists")
    return result


# %% build requests
for chunk in chunks(artists, 20):
    start = time.time()
    urls = []
    df = pd.DataFrame([], columns=["artist", "date",
                                   "nom_concert", "endroit", "ville"])
    for artist in chunk:
        u = f"https://www.concertarchives.org/concerts?utf8=%E2%9C%93&search={artist}"
        urls.append(u)
    rs = (grequests.get(u) for u in urls)
    responses = grequests.map(rs)
    print(time.time()-start)
    artistData = scrapArtist(responses)
    df = pd.DataFrame([], columns=["artist", "date",
                                   "nom_concert", "endroit", "ville"])
    artistData = scrapArtist(responses)
    for line in artistData:
        df.loc[len(df)] = line
    df.to_csv(OUTPUT_PATH, sep='|', mode='a',
              header=False, index_label=False)
