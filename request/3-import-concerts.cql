// Import file concerts.csv
USING PERIODIC COMMIT 500
LOAD CSV FROM 'file:///concerts.csv'
 	AS ligne FIELDTERMINATOR '|'
    
    MERGE (a:Artist {artist_name: ligne[1]})

    MERGE (c:Concert {
        date: ligne[2],
        nom_concert: ligne[3],
        salle_concert: ligne[4],
        ville: ligne[5]
        })
    MERGE (a)-[:PLAYS_IN]->(c)