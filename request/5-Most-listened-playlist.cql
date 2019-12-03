// The 30 most listened playlist with the number of plays
MATCH(u:User)-[:LISTEN_TO]->(s:Song)<-[:CONTAINS]-(p:Playlist)
WITH p, count(u) AS popularity
RETURN p.playlist_name AS playlist_name, popularity
ORDER BY popularity DESC
LIMIT 30