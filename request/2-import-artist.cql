// Import file artists.csv
USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS FROM 'file:///artists.csv'
 	AS ligne FIELDTERMINATOR ';'
    
    MERGE (a:Artist {artist_name: ligne.artist_name})
    SET a.id = ligne.artist_id
    SET a.popularity = ligne.popularity
    FOREACH(genre IN split(ligne.genres, "', '") |
        // In order to remove the [' & '] before the lines
        MERGE(g:Genre {
            genre_name: replace(
                replace(genre, "['", "")
            , "']", "")
            })
        MERGE (a)-[:PLAYS_GENRE]->(g)
    )
    FOREACH(relatedArtist IN split(ligne.related, "', '") |
        // In order to remove the [' & '] before the lines
        MERGE(rA:Artist {
            artist_name: replace(
                replace(relatedArtist, "['", "")
            , "']", "")
            })
        MERGE (a)-[:IS_RELATED_TO]->(rA)
    )
