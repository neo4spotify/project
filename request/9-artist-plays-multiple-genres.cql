// Les artistes qui jouent à la fois de l'indietronica, de la folk-pop et de l'escape room (?).
MATCH (g:Genre)<-[:PLAYS_GENRE]-(a:Artist)
WHERE g.genre_name="folk-pop"
    WITH a
    MATCH (g:Genre)<-[:PLAYS_GENRE]-(a:Artist)
    WHERE g.genre_name="indietronica"
        WITH a
        MATCH (g:Genre)<-[:PLAYS_GENRE]-(a:Artist)
        WHERE g.genre_name="escape room"
        RETURN DISTINCT a.artist_name AS name, a.popularity AS popularity