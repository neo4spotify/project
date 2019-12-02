MATCH(u:User)-[]->(s:Song)<-[]-(a:Artist)-[]->(g:Genre)
// On enregistre la popularité du genre
WITH g, count(u) AS popularity
SET g.popularity=popularity
RETURN g.genre_name, popularity
ORDER BY popularity DESC