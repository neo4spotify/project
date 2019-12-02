// Import du fichier artists.csv
USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS FROM 'file:///artists.csv'
 	AS ligne FIELDTERMINATOR ';'
    
    // If there is a track name
    MERGE (a:Artist {artist_name: ligne.artist_name})
    
    // MERGE (u)-[:LISTEN_TO]->(s)
    // MERGE (p)-[:CONTAINS]->(s)
    // MERGE (a)-[:PLAYS]->(s)


Elvis Costello;2BGRfQgtzikz1pzAD0kaEn;
['art rock', 'dance rock', 'folk', 'folk rock', 'mellow gold', 'new wave pop', 'permanent wave', 'power pop', 'pub rock', 'rock', 'roots rock', 'singer-songwriter'];
60.0;
['Elvis Costello & The Attractions', 'Squeeze', 'Joe Jackson', 'Nick Lowe', 'Graham Parker', 'XTC', 'Elvis Costello & The Imposters', 'Marshall Crenshaw', 'Graham Parker & The Rumour', 'Big Star']