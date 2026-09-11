# Les cartes de statut (Stunned, Confused, Tough) sont floues en jeu

**Remonté par un joueur (Manu, Discord) le 11/09/2026**, capture à l'appui :
« ce truc est trooop flou. Là dans le screenshot on arrive à lire, mais dans le
jeu c'est pas simple ». La capture montre la carte d'état « Stunned » en grand
sur le plateau, texte à peine lisible.

## Ce qu'on sait

- Le plateau agrandit les cartes au survol et en grand ; les scans de statut
  viennent de `assets/pics/` (300 px de large pour les officielles) et sont
  étirés bien au-delà.
- `tools/telecharger_scans_hd.py` ne télécharge les HD que pour les types
  Hero, AlterEgo, Villain et MainScheme (`TYPES`, ligne ~41) : les cartes de
  statut n'en font pas partie, et `Cache.LoadImageHD` ne les sert donc jamais
  en HD.
- Les trois cartes d'état sont partagées par toutes les parties : trois
  fichiers à traiter, pas une collection.

## Par où commencer

1. Identifier les `card_id` des trois statuts et vérifier ce que `assets/pics`
   et `assets/pics-fr` contiennent pour elles (taille réelle).
2. Soit ajouter le type des statuts à `TYPES` de `telecharger_scans_hd.py`
   (si les serveurs d'images les servent en HD), soit déposer une fois pour
   toutes trois scans HD à la main dans `assets/pics-hd/`.
3. Vérifier à l'œil dans le plateau, en grand, que le texte est lisible.
