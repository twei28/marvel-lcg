# Table personnalisable par briques : décisions du 05/10/2026 (questions une à une)

Point de départ : la table (disposition.ts, EditeurTable.tsx) n'a que 9 zones fixes. Certaines
mélangent plusieurs types de cartes (`terrain-combat` = alliés + sbires engagés + environnement,
`terrain-soutien` = héros + soutiens + obligations). Le joueur veut pouvoir les séparer et les
regrouper à volonté.

## Décisions

- La table est faite de BRIQUES. Une zone est un assemblage de briques, avec un titre automatique
  (« Héros et soutiens » devient « Héros » + « Soutiens » quand on les sépare, et inversement).
- Briques : Héros, Soutiens, Alliés, Méchant, Sbires, Environnements, Manigance principale,
  Manigances annexes. Les piles (rencontre, héros), « Mises de côté / autres piles » et la Main
  restent comme aujourd'hui. Les améliorations restent collées à leur carte.
- Geste : dans l'éditeur, chaque brique est une pastille dans sa zone. On la glisse vers un endroit
  libre = nouvelle zone avec son titre ; on la glisse sur une autre zone = fusion, titre « X et Y ».
- Multijoueur : UNE brique par type, rangée par joueur à l'intérieur (pas de brique par joueur).
- Dans une zone fusionnée : ordre fixe du jeu (Héros, Soutiens, Alliés, Méchant, Sbires...), une
  seule taille de cartes pour la zone (à la séparation, chaque brique reprend la taille de la zone).
- Table d'origine IDENTIQUE à celle d'aujourd'hui (rien ne change à l'écran sans réglage).
- Tables déjà enregistrées : CONVERTIES (les nouvelles briques restent dans la zone dont elles
  viennent), pas de remise à zéro.
- Zone vide en partie : invisible mais la place est gardée (visible dans l'éditeur seulement).
- Grille : « plus fine » demandé, MAIS l'éditeur est déjà en 12 x 8 (seule l'origine historique est
  en 4 x 4). À re-valider avec 12 briques à placer.

## Impacts repérés (code lu, rien modifié)

- `disposition.ts` : `ZONES` fixe (9 clés), `MINIMUMS`, `estValide`, `ecrireTable`/`lireTable`
  (texte compact `12x8|...` en 9 zones, partagé avec le serveur). À remplacer par des zones
  composées de briques, avec conversion de l'ancien format.
- `server_get.py` `_table_valide` : valide le texte compact. À aligner.
- `zones.ts` : `terrain-combat` et `terrain-soutien` sont construits d'un bloc (alliés, engagés,
  environnement ; héros, soutiens, obligations, résolution). Il faut des briques séparées
  (Héros distinct de Soutiens, Alliés / Sbires / Environnement distincts) tout en gardant les
  secteurs du glisser-déposer du mode manuel (`CLE_PILE_ENGAGES`, `groupesPiles`, `data-zone`).
- `Board.tsx` : rend une zone par emplacement avec `zone-<cle>` et `data-zone` ; `board.css` /
  `bande-manigances.css` posent les aires de grille par nom de zone.
- `EditeurTable.tsx` : seulement déplacer / redimensionner 9 zones ; à étendre au glisser de briques.
- Téléphone : inchangé.

## Étapes prévues

1. Modèle pur (briques, zones, titre automatique, fusion / séparation, conversion de l'ancien
   format) + tests. Aucun changement à l'écran.
2. Rendu : le plateau construit ses zones depuis les briques ; origine identique (tests de
   comparaison existants) ; mode manuel intact.
3. Éditeur : pastilles de briques, glisser dehors / dessus.
4. Serveur : validation du nouveau format, conversion des tables du compte.
5. Gate : vitest, tsc, build, capture de l'éditeur et d'une table éclatée sur le moteur d'essai.

## Avancement (05/10/2026, soir) : étapes 1 à 5 FAITES, non commité, non déployé

*06/10/2026 : commité dans `3a6afcf0` et déployé le 05/10 (file d'attente). Le mode manuel sur une
table éclatée n'est toujours pas vérifié : prévu au lot 2 de `docs/superpowers/plans/2026-10-06-mode-manuel-comme-octgn.md`.*

- Étape 1 : `table-briques.ts` (12 briques, zones, fusion / séparation, `deposerBrique`, texte compact, conversion de l'ancien format). `disposition.ts` supprimé.
- Étape 2 : `table-rendu.ts` (`assemblerZones`), `Board.tsx`, `zones.ts`, `bande-manigances.css`. Une zone qui reprend un emplacement d'origine entier est rendue telle quelle (origine identique).
- Étape 3 : `EditeurTable.tsx` (pastilles, glisser dehors = séparer, dessus = fusionner).
- Étape 4 : `server_get.py` `_table_valide` accepte l'ancien et le nouveau format ; `test_preferences_serveur.py` 19/19.
- Étape 5 : tsc propre, vitest 223 fichiers / 2577 tests verts, build + verifier-sortie OK, captures sur le moteur d'essai (origine identique, sbires sortis, fusion manigances).
- Zone mixte manigance principale + annexes : titre et cartes calés à droite, comme les deux zones d'origine. Voulu, pas corrigé.

Reste : mode manuel (`data-zone`, `data-pile`) à regarder sur une table éclatée dans une vraie partie ; déploiement seulement sur « déploie ». Il emmènerait aussi les bulles d'arts alternatifs (e0955eb8), `palettes-heros-corrections.json` et `prepare.html`. La validation serveur doit partir avec le plateau.
