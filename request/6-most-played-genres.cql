// The 30 most listened genres
MATCH(u:User)-[:LISTEN_TO]->(s:Song)<-[:PLAYS]-(a:Artist)-[:PLAYS_GENRE]->(g:Genre)
WITH g, count(u) AS popularity
SET g.popularity=popularity
RETURN g.genre_name, popularity
ORDER BY popularity DESC