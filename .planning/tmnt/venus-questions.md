# Venus (TMNT Heroes v3, Inkwire) : questions en attente

Aucune question n'a pu etre posee a l'utilisateur pendant la construction (agent en parallele,
16/10/2026). Chaque lecture RETENUE provisoirement est marquee `TODO-QUESTION` dans le script.
Source des scans : `TMNT Heroes-20261014T200300Z-1-001.zip` / `TMNT Heroes/Venus v3/`
(copie versionnee : `.planning/tmnt/pics-venus/`).

## Q1 : « (to a maximum of 6) » sur * Venus (tv001a), a quoi s'applique le plafond ?

- **Carte** : `tv001a` * Venus (face heros), script `Fusion/marvel-lcg-src/src/cards/pack/venus/venus/tv001a.py`
  (`TODO-QUESTION Q1`).
- **Scan** : `TMNT Heroes/Venus v3/0 Venus Hero.png`.
- **Texte anglais exact** : « Action: Place 1 dredge counter on Venus for each ELEMENT upgrade you
  control (to a maximum of 6). (Limit once per round.) »
- **Lectures** :
  1. **(retenue, recommandee) Plafond du STOCK** : Venus ne porte jamais plus de 6 compteurs de
     dragage ; l'Action ne pose que ce qui tient (2 deja + 6 ELEMENT en jeu -> 6, pas 8). C'est le
     sens de « to a maximum of 3 » de la rage de Raphael (decision du 15/10/2026) et la seule lecture qui
     a un effet : il n'existe que 6 ameliorations ELEMENT, donc plafonner le nombre pose
     par activation ne changerait jamais rien.
  2. Plafond PAR ACTIVATION seulement : au plus 6 compteurs poses par Action, sans limite du stock
     (6 + 6 = 12 compteurs possibles sur deux rounds).
  3. Aucun plafond reel (le « 6 » rappelle simplement le nombre de cartes ELEMENT du paquet).
- **Ce que ca change en jeu** : lecture 1 borne les economies de compteurs a 6 (plus de 6 compteurs
  inutilisables a accumuler) ; lecture 2 permet de les accumuler au-dela de 6 en rejouant l'Action
  chaque round.
- **Cas** : `[venus] tv001a Venus : plafond de 6 sur le STOCK ... [TODO-QUESTION Q1]`.

## Q2 : icone Hazard imprimee sur l'obligation Faulty Creation (tv015)

- **Carte** : `tv015` Faulty Creation (obligation), `desc.Hazard = "1"`.
- **Scan** : `TMNT Heroes/Venus v3/Venus Bad Stuff/Venus Obligation.png` (icone au centre du cadre de
  texte, en bas : carte inclinee + croix).
- **Texte anglais exact** : « Give to the Bonnie player. You may flip to alter-ego form. Alter-Ego
  Action: Exhaust Bonnie -> remove Faulty Creation from the game. » (aucune phrase de regle, l'icone
  seule).
- **Lectures** :
  1. **(retenue, recommandee) L'icone est celle du jeu : Hazard 1**, comparee par decoupe a `01107`
     Breakin' & Takin' (identique) ; tant que l'obligation est en jeu, elle compte comme une icone
     Hazard (une carte Rencontre supplementaire par phase du mechant).
  2. Decor du gabarit de l'auteur (le meme glyphe est sur Jasper Barlow's Lab, ou il est voulu) : aucune
     icone, l'obligation ne fait rien d'autre.
- **Ce que ca change en jeu** : lecture 1 punit le joueur tant qu'il n'a pas paye l'Action d'alter-ego
  (une carte Rencontre de plus chaque round) ; lecture 2 non. Aucune obligation officielle ne porte d'icone.
- **Cas** : `[venus] tv015 Faulty Creation : icone HAZARD imprimee ...`.

## Q3 : « each [wild] resource used to pay for this card » (tv005 Eldritch Lance)

- **Carte** : `tv005` Eldritch Lance, script `.../venus/venus/tv005.py`.
- **Scan** : `TMNT Heroes/Venus v3/Venus Deck/5 Eldritch Lance.png`.
- **Texte anglais exact** : « Hero Action (attack): Deal 5 damage to an enemy. This attack gains overkill.
  Draw 1 card for each [wild] resource used to pay for this card. »
- **Lectures** :
  1. **(retenue, recommandee) Toutes les ressources wild produites par les cartes depensees** pour
     payer (`effect.GetPaidResources().g`, meme lecture que `tr006` « paid with [physical] » et
     toutes les cartes du moteur) : payee par Evanescence (GGG) + Energy (YY) = 3 cartes, meme si le cout
     (4) n'avait besoin que d'une ressource wild de plus.
  2. Seulement les wild reellement necessaires au cout (3 wild + 1 energie = 3 aussi ici, mais
     Evanescence + Evanescence = 4 et non 6) : le surplus ne compte pas.
- **Ce que ca change en jeu** : lecture 2 plafonne la pioche au cout (jamais plus de 4 cartes) ;
  lecture 1 permet 6 cartes en payant avec deux Evanescence.
- **Cas** : `[venus] tv005 Eldritch Lance : payee par Evanescence (GGG) + Energy (YY) ...`.

## Notes sans question (pour memoire)

- `Arc Nova` imprime « VENUS (2/16) » : coquille de l'auteur (les 15 scans sont numerotes 1 a 15).
- Paires de cartes a illustration continue : voir le rapport final (candidates `tv011` Dragon Scale /
  `tv014` Turtle Shell, scans 12 et 15) : RIEN n'est declare, a confirmer par l'utilisateur.

## REPONSES DE L'UTILISATEUR (16/10/2026)

- **Q1** : plafond du STOCK de Venus (lecture retenue, confirmee). Rien a changer.
- **Q2** : l'icone est un vrai Hazard 1 (lecture retenue, confirmee). Rien a changer.
- **Q3** : seulement les ressources wild NECESSAIRES au cout (PAS la lecture retenue) : `min(wild payees, cout paye)`, jamais le surplus. tv005 corrige, cas « deux Evanescence : 4 cartes et non 6 » vu rouge puis vert.
- **Paire Dragon Scale (tv011) + Turtle Shell (tv014)** : l'utilisateur a refusé le panorama (cartes séparées, illustration non vraiment continue). Rien n'est déclaré dans `panorama-jumelles.ts`.
