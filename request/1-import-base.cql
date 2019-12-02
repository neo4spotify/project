// Import du fichier base.csv
USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS FROM 'file:///base.csv'
 	AS ligne FIELDTERMINATOR ';'
    
    // If there is a track name
    FOREACH(ignoreMe IN CASE WHEN ligne.track_name = null THEN [1] ELSE [] END |
        MERGE (u:User {id: ligne.user_id})
        MERGE (s:Song {track_name: ligne.track_name})
        MERGE (a:Artist {artist_name: ligne.artist_name})
        MERGE (p:Playlist {playlist_name: ligne.playlist_name})
        
        MERGE (u)-[:LISTEN_TO]->(s)
        MERGE (p)-[:CONTAINS]->(s)
        MERGE (a)-[:PLAYS]->(s)
    )
