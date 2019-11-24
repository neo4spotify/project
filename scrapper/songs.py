# %% Imports
import pandas as pd
import grequests
from bs4 import BeautifulSoup
import time
import csv
import urllib.parse


# %% Constants
OUTPUT_PATH = "data/chunks.csv"
# %%
df = pd.read_csv(OUTPUT_PATH, sep=";")
artists = df[' "artistname"'].unique()

# %%
def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in range(0, len(l), n))

def scrapArtist(responses):
    numberCorrect = 0
    for r in responses:
        # print(str(r))
        result=[]
        try:
            if str(r) != 'None':
                soup = BeautifulSoup(r.text, 'lxml')
                for row in soup.findAll('table')[0].tbody.findAll('tr'):
                    first_column = row.findAll('td')[0].contents
                    second_column = row.findAll('td')[1].find(
                        "strong").find("a").contents
                    third_column = row.findAll('td')[2].findAll("a")
                    fourthColumn = row.findAll('td')[3].findAll("a")
                    res = [urllib.parse.unquote(r.url[63:]), first_column[0][0:12], second_column[0]]
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
    with open("concerts.csv", "a", encoding="utf-8") as fp:
        for line in result:
            wr = csv.writer(fp, dialect='excel')
            wr.writerow(line)
            
    print(f"Correctly scrapped {numberCorrect} artists")







# %% build requests
for chunk in chunks(artists[0:500], 20):
    start = time.time()
    urls = []
    for artist in chunk:
        u = f"https://www.concertarchives.org/concerts?utf8=%E2%9C%93&search={artist}"
        urls.append(u)
    rs = (grequests.get(u) for u in urls)
    responses = grequests.map(rs)
    print(time.time()-start)
    scrapArtist(responses)
# %%

