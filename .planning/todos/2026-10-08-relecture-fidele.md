# Relecture et spectateur : voir 100 % de ce que le joueur a vu

**RETIRÉ du backlog le 21/10/2026** (item 5), décision de l'utilisateur.

Demande du 08/10/2026 : « le but, c'est vraiment de voir 100 % ce que le
joueur a vu quand il jouait ». Constaté : en relecture, les fenêtres (jouer
une carte, payer...) ne s'affichent pas, et la barre de lecture cache la main.

## Décisions (questions une à une, 08/10/2026)

1. **Fenêtres** : affichées exactement comme pour le joueur, non cliquables,
   avec son choix surligné.
2. **Sélection en cours** : chaque clic dans une fenêtre est rejoué (une carte
   cochée, décochée, puis le bouton validé).
3. **Barre de lecture** : se cache toute seule après 2 s sans bouger la souris,
   revient quand on approche du bas ou à chaque touche du clavier.
4. **Clavier** : Espace lecture/pause, ← → action précédente/suivante,
   Maj+← → round précédent/suivant, + et - vitesse.
5. **Action suivante** : saute jusqu'à la prochaine décision d'un joueur.
6. **Vitesse** : temps réel, pauses de plus de 5 s ramenées à 2 s, x2 x4.
7. **Point de vue** : suit automatiquement le joueur qui a la main ; le choix
   manuel « Vue » reste, et tient jusqu'au retour à « Auto ».
8. **Loupe** : les survols de cartes du joueur sont rejoués (même carte, même
   moment, même durée).
9. **Piles** : l'ouverture d'une pile (défausse, recherche, rencontre) est
   rejouée, avec le défilement dedans.
10. **Réglages** : ceux du joueur (mode de phase, sobre, animations, taille des
    cartes, thème, côté des améliorations...) et leurs changements en cours de
    partie, SAUF la langue, qui reste celle de celui qui regarde.
11. **Taille d'écran** : celle du joueur, mise à l'échelle dans l'écran de
    celui qui regarde ; le curseur tombe au bon endroit.
12. **Messages et menus** : les messages passagers ET ses menus (clic droit,
    Réglages, Aide) sont rejoués.
13. **Aussi** : ses sons à son volume (coupables), ses glisser-déposer (la
    carte qui suit la souris), le défilement de sa main et du journal,
    l'écran de fin tel qu'il l'a vu (récompenses de campagne comprises).
14. **Direct** : le mode spectateur en direct montre la même chose que la
    relecture, au moment où le joueur le fait.

## Contraintes

- Les anciennes relectures restent lisibles : sans les nouvelles lignes, elles
  montrent ce qu'elles peuvent (les fenêtres, sans le choix).
- Le choix surligné et tout ce qui est nouveau ne valent que pour les parties
  jouées après la mise en ligne.
- Le volume enregistré grossit : mesurer la taille d'un fichier d'une partie
  type avant et après.

## Avancement

Mécanisme commun (08/10/2026) : le plateau du joueur publie ce qu'il voit par
`POST /set_vu` (un genre par information, `server_get.set_vu`), le moteur le
relaie au spectateur (`GET /get_vus`) et l'enregistre (ligne « v » du
.marvelreplay). Côté plateau : `vu-partage.ts` (publier / `useVuDuJoueur`).
Le spectateur et la relecture dessinent le plateau dans un CADRE (iframe) à la
taille de l'écran du joueur, avec ses réglages en mémoire (`cadre-joueur.ts`,
`CadreJoueur.tsx`), derrière une vitre qui arrête les clics
(`vitre-spectateur.ts`).

- [x] 1. Fenêtres affichées (`aNous` vrai pour le siège affiché, gardes
  `!spectateur` retirées : menu de carte, barre d'action, fin de tour), vitre.
- [x] 2. Sélection rejouée clic par clic (genre `sel`, `useInteraction`
  reçoit la sélection du joueur). Le choix final reste affiché jusqu'à la
  question suivante (pas de genre `rep` séparé : la sélection + l'onde du
  clic le montrent).
- [x] 3. Barre qui se cache (2 s, revient en bas ou au clavier).
- [x] 4. Clavier (Espace, ← →, Maj+← →, + -), relayé depuis le cadre.
- [x] 5. Action suivante = prochaine décision (`Lecteur.decisions`).
- [x] 6. Temps réel, temps morts > pause max ramenés à 2 s, ENTRE deux
  événements (un clic après 20 s de réflexion reste à sa place) ; la pause
  garde l'instant entre deux trames.
- [x] 7. Vue Auto (qui a la main) + choix manuel tenu.
- [x] 8. Loupe (survol et fiche Ctrl+I), genre `loupe`.
- [x] 9. Piles ouvertes (genre `pile`) et défilements (genre `defil`,
  `defilement-partage.ts`, toute boîte qui défile).
- [x] 10. Réglages hors langue (genre `regl`, copie en mémoire dans le cadre).
- [x] 11. Taille d'écran (genre `ecran`, cadre mis à l'échelle).
- [x] 12. Messages (bulle de refus du glisser, genre `msg`) et menus
  (Réglages, Menu, journal, aides : genre `menu` ; mode manuel : clic droit,
  menu de table, piles, avis, catalogue, fin, mulligan : genre `manu`).
- [x] 13. Sons au volume du joueur (ses réglages), glisser (genre `glis`),
  écran de fin tel qu'il l'a vu (ses boutons, inertes).
- [x] 14. Direct = relecture : même cadre, mêmes genres, lus sur `/get_vus`.

### Vu au navigateur (08/10/2026, moteur d'essai, `ui-check/tests/zz-relecture-fidele.spec.ts`)

Joueur en 1280×720, spectateur et relecture en 1600×900 :
- cadre à 1280×720 mis à l'échelle ×1,21 ; volume du joueur (37) lu dans le cadre ;
- loupe, menu de carte (« Jouer »), fenêtre de paiement de Lance-toile avec
  Énergie cochée : identiques chez le joueur, en direct et en relecture
  (mêmes cartes cochées) ; main remontée par le survol du joueur ;
- un clic du spectateur ne ferme pas la fenêtre (vitre + cadre insensible) ;
- relecture : fenêtre du mulligan et du paiement, barre cachée après 2 s puis
  revenue en bas, → saute à la décision suivante, + passe en ×2 ; aucune erreur ;
- un saut ne rejoue plus l'annonce « Round 1 / Spider-Man » (SplashTour).

Taille : partie d'essai 100 020 octets bruts (10,2 ko gzip), dont 2 716 de
lignes « v » (2,7 %).

### Reste

- [ ] Non vu en vrai : mode manuel regardé (clic droit, piles), glisser,
  défilement de la main, réglages changés en cours de partie (le cadre se
  remonte alors), direct à plusieurs joueurs, tablette et téléphone.
- [ ] Le survol à l'intérieur d'une pile ouverte (son aperçu propre) n'est pas
  rejoué ; les hauts faits / récompenses de campagne pas à pas non plus.
- [ ] Le curseur et donc le survol CSS disparaissent 5 s après le dernier
  mouvement (péremption des curseurs) : un joueur immobile sur sa main la voit
  redescendre chez le spectateur.
