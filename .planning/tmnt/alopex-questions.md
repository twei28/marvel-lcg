# Alopex (TMNT, `ta`) : questions en attente de l'utilisateur

Format : card_id, scan, texte anglais exact, lectures possibles (la recommandée en
premier). Chaque lecture provisoire est marquée `TODO-QUESTION` dans le script.
Scans versionnés : `.planning/tmnt/pics-alopex/<card_id>.jpg` ; originaux dans le zip
« TMNT Heroes / Alopex v3 ».

## Q1. ta001a Alopex (Matagi) : « find Prey » quand Prey est déjà en jeu

- Scan : `.planning/tmnt/pics-alopex/ta001a.jpg` (zip : `0 Alopex Hero.png`).
- Texte : « *Matagi* — **Forced Response**: After you attack an enemy or thwart a
  scheme, find Prey and attach it to that enemy or scheme. »
- Contexte : Prey (ta011) est mise de côté au Setup et y retourne quand elle quitte
  le jeu. Si Prey est déjà attachée à A et qu'Alopex attaque B :
  1. **(retenue, provisoire)** « find » = chercher parmi les cartes de côté : Prey en
     jeu n'est pas trouvable, elle reste sur A (collante jusqu'à ce qu'A soit vaincu
     ou contré). Cas `[alopex] ta001a Matagi : Prey DEJA en jeu...`.
  2. Prey se déplace sur B (l'attache est refaite à chaque attaque/contre).
  3. Autre (préciser).
- Effet en jeu : 1 = Prey reste longtemps sur la même cible, Kabuki/Kama se
  déclenchent à sa mort ; 2 = Prey suit la dernière cible, elle ne quitte le jeu que
  si la cible disparaît juste après.

## Q2. ta002 Nobody : « thwarts a scheme with Prey attached, cloak her » quand le contre vide la manigance

- Scan : `.planning/tmnt/pics-alopex/ta002.jpg` (zip : `Alopex Deck/1 Nobody.png`).
- Texte : « [star] **Response**: After Nobody thwarts a scheme with Prey attached,
  cloak her. » (et « ... attacks an enemy with Prey attached, daze that enemy »).
- Contexte : si le contre retire la dernière menace, la manigance est vaincue et Prey
  part de côté AVANT la fenêtre de Réponse.
  1. **(retenue, provisoire)** l'état « avec Prey attachée » est lu AU MOMENT du
     contre : Nobody est camouflée quand même.
  2. Lu APRÈS le contre : Prey a disparu avec la manigance, rien ne se passe.
  3. Autre.
- Pour l'attaque : l'ennemi vaincu n'existe plus, donc rien à étourdir dans les deux
  lectures (pas de divergence).

## Q3. ta006 Sniff Out Trouble : « Reveal that card → draw 2 cards and ready each KAMA »

- Scan : `.planning/tmnt/pics-alopex/ta006.jpg`.
- Texte : « **Hero Action**: Discard cards from the encounter deck until you discard a
  minion or side scheme. Reveal that card → draw 2 cards and ready each [[KAMA]]
  upgrade you control. »
- Contexte : si le deck Rencontre s'épuise sans minion ni manigance annexe :
  1. **(retenue, provisoire)** la révélation est le coût de la suite : rien révélé,
     rien pioché, Kama non redressées (les cartes défaussées restent défaussées).
  2. On pioche et on redresse quand même.
  3. Autre.
  (Le deck n'est pas remélangé : « until you discard » n'est pas une pioche de
  rencontre.)

## Signalement (pas une question) : paire 14/15 à illustration continue

ta009 Alopex's Kama / ta010 Alopex's Other Kama : l'illustration de la lame traverse
les deux cartes (la 15 est la 14 « retournée »). Rien n'est déclaré dans
`panorama-jumelles.ts` ; `tools/importer_images_alopex.py` le rappelle.

## Notes de lecture (tranchées sans question)

- « charcter » (scan de l'obligation ta012) corrigé en « character » dans cards.json ;
  « Alopex' » (Prey) conservé tel qu'imprimé.
- « printed [mental] resource » (Prowl) = icône mentale imprimée uniquement ; une
  carte à ressource wild ne compte pas.
- « Daze » = carte d'état Dazed (insert « Dazed Rules », zip Baxter Stockman v3).
- Pounce : « 1 damage » + « 2 additional damage for each » = UN seul coup de 1 + 2n
  (comme Repulsor Barrage `im002`).

## REPONSES DE L'UTILISATEUR (16/10/2026)

- **Q1** : regle officielle de « find » collee par l'utilisateur (« search each area where the card could be found (play area, set-aside area, player deck, discard pile, encounter deck, etc) ») : Prey DEJA en jeu est TROUVEE et DEPLACEE sur la nouvelle cible (PAS la lecture retenue). ta001a corrige, `PreyEnJeu` (qui passait une identite au lieu d'un effet) corrige, cas « Prey DEJA en jeu... deplacee » vu rouge puis vert.
- **Q2** : Nobody camouflee, etat lu au moment du contre (confirmee).
- **Q3** : deck Rencontre epuise sans sbire ni manigance annexe : rien (confirmee).
