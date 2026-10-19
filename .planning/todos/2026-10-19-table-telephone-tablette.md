# Phase du méchant « Sur la table » : téléphone et tablette (mis de côté le 19/10/2026)

Décision de l'utilisateur, le 19/10/2026, pendant les corrections du mode : « tout ce qui est téléphone et
tablette, on oublie pour le moment », puis « on ajoute ça au backlog ». Les corrections de ce jour (étiquettes de
défense, bandeau déplaçable, ordre des sbires, Renfort, calcul, toast, éventail…) sont testées sur PC seulement
(1280×720). Ce fichier garde ce qui reste à reprendre pour le tactile et les petits écrans.

## À reprendre
- **Mobile portrait (390×844)** : quand une question demande de choisir un défenseur, la table défile toute seule
  jusqu'à la bande « TON HÉROS » pour montrer les cartes à toucher, puis revient (décision du 19/10, tâche T13, non faite).
  Pas de boutons de défense dans le bandeau sur mobile. Vérifier : cartes entièrement visibles, `elementFromPoint`
  au centre de chaque carte, cibles ≥ 44 px.
- **Éventail des améliorations** (T14) : testé sur PC seulement. À vérifier au toucher (cibles ≥ 44 px, nom lisible),
  en tablette 1180×820 et en mobile portrait, y compris sous un allié.
- **Bandeau en colonne sur le côté** (T2) et **pastille Renfort** (T9) : vérifier en tablette et en mobile portrait
  (largeur du bandeau compatible, texte lisible, aucune carte rognée).
- **Petit écran paysage** (1050×480, 844×390) : le héros et la main sortent du cadre au repos ; seuls deux alliés sur
  trois visibles pendant la défense ; le bandeau d'ordre des sbires prend une grande partie de la hauteur.
  « Fin du tour » n'est plus recouvert (T4, vérifié le 19/10) mais le reste du plateau reste à revoir.
- **Lisibilité des cartes** : les plus petites cartes de la table mesurent 49×35 px (PC) et 45×32 px (tablette), le
  texte des sbires n'est lisible qu'avec l'aperçu ; en mobile portrait, passer par l'aperçu.
- **Cibles tactiles** : « Fin du tour » 114×30 px (44 px au toucher depuis T4), boutons du bandeau 32 px sur PC et
  44 px dès qu'un pointeur tactile est détecté.
- **Aperçu au survol** : n'existe pas au toucher ; prévoir l'appui long ou un bouton « Voir la carte ».
- **Vrais appareils** : tout ce qui a été mesuré était une émulation Chromium de bureau (taille + pointeur tactile),
  jamais un téléphone ni une tablette réels.

## Où regarder
- `docs/rapports/phase-mechant-sur-la-table/catalogue-phases/` : captures mobile et tablette du 18/10/2026
  (`12-v-*`), remarques d'ergonomie 8, 9 et 10.
- `docs/rapports/phase-mechant-sur-la-table/corrections-2026-10-19*.md` : rapports des agents (ligne « téléphone/tablette :
  non traité » de chacun).

## Autres points mis en attente par l'utilisateur le même jour
- **« Sur la table » devient « Étape par étape » (T18)** : annulé jusqu'à ce que l'utilisateur ait validé complètement
  la nouvelle version. Les trois choix restent en attendant (Étape par étape, Sur la table, D'un coup).
