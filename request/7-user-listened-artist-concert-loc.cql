// La localisation des concerts des artistes écoutés par un utilisateur sur l'année 2012
MATCH (u:User)-[:LISTEN_TO]->(s:Song)<-[:PLAYS]-(a:Artist)-[:PLAYS_IN]->(c:Concert)-[:IS_IN]->(v:Ville)
WHERE u.id="9cc0cfd4d7d7885102480dd99e7a90d6"
AND c.date CONTAINS "2012"
return v.ville_name AS ville,
	v.lat AS lat,
    v.lng AS lng,
    count(a) AS compte