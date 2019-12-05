// Import file villes.csv
USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS FROM 'file:///villes.csv'
 	AS ligne FIELDTERMINATOR '|'
    FOREACH(ignoreMe IN CASE WHEN ligne.ville <> '' THEN [1] ELSE [] END |

        MERGE (v:Ville {ville_name: ligne.ville})
        SET v.lat = ligne.lat
        SET v.lng = ligne.lng
    )