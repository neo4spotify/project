CREATE CONSTRAINT ON (u:User) ASSERT u.id IS UNIQUE; 
CREATE CONSTRAINT ON (s:Song) ASSERT s.track_name IS UNIQUE; 
CREATE CONSTRAINT ON (a:Artist) ASSERT a.artist_name IS UNIQUE; 
CREATE CONSTRAINT ON (p:Playlist) ASSERT p.playlist_name IS UNIQUE; 
CREATE CONSTRAINT ON (g:Genre) ASSERT g.genre_name IS UNIQUE; 
CREATE CONSTRAINT ON (v:Ville) ASSERT v.ville_name IS UNIQUE; 
CREATE CONSTRAINT ON (c:Concert) ASSERT (c.date, c.nom_concert) IS NODE KEY
