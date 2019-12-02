// Import du fichier artists.csv
USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS FROM 'file:///artists.csv'
 	AS ligne FIELDTERMINATOR ';'
    
    // If there is a track name
    MERGE (a:Artist {artist_name: ligne.artist_name})
    
    // MERGE (u)-[:LISTEN_TO]->(s)
    // MERGE (p)-[:CONTAINS]->(s)
    // MERGE (a)-[:PLAYS]->(s)
