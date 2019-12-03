// Import file concerts.csv
USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS FROM 'file:///concerts.csv'
 	AS ligne FIELDTERMINATOR '|'
    
    MERGE (a:Artist {artist_name: ligne.artist})

    MERGE (c:Concert {
        date: ligne.date,
        nom_concert: ligne.nom_concert,
        salle_concert: ligne.endroit,
        ville: ligne.ville
        })
    MERGE (a)-[:PLAYS_IN]->(c)