INSERT  Or ignore INTO oeuvre_categorie(id_oeuvre,id_categorie)
SELECT id,8 FROM oeuvre WHERE nom LIKE "%noël%"