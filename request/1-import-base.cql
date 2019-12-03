// Import file base.csv
USING PERIODIC COMMIT 1000
LOAD CSV WITH HEADERS FROM 'file:///base.csv'
 	AS ligne FIELDTERMINATOR ';'
    
    // If there is a playlist name and a track name

    FOREACH(ignoreMe IN CASE WHEN ligne.track_name <> '' THEN [1] ELSE [] END |
        MERGE (u:User {id: ligne.user_id})
        MERGE (s:Song {track_name: ligne.track_name})
        MERGE (a:Artist {artist_name: ligne.artist_name})
        

        FOREACH(ignoreMe IN CASE WHEN ligne.playlist_name <> '' THEN [1] ELSE [] END |
            MERGE (p:Playlist {playlist_name: ligne.playlist_name})
            MERGE (p)-[:CONTAINS]->(s)
        )
        MERGE (u)-[:LISTEN_TO]->(s)
        MERGE (a)-[:PLAYS]->(s)
    )
