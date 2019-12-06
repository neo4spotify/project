// Les villes les plus influente proportionnellement au nombre d'écoute
MATCH (v:Ville)<-[:IS_IN]-(c:Concert)<-[:PLAYS_IN]-(a:Artist)-[:PLAYS]->(s:Song)<-[:LISTEN_TO]-(u:User)
RETURN v.ville_name AS ville,
    v.lat AS lat,
    v.lng AS lng,
    COUNT(DISTINCT u) AS compte
ORDER BY compte DESC
LIMIT 10