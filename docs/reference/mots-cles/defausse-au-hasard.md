# Discard at random (« défaussez 1 carte prise au hasard dans votre main »)

**Texte imprimé / définition** : « Discard 1 card from your hand **at random** → <effet> ... where X is equal to the numeral
in the printed resource cost of that card ». Pas un mot-clé : une MÉCANIQUE du pack `new_ultimate_winter_soldier` (`uw`,
Dipsome) que neuf cartes disent ou lisent. Six la **paient** (`uw004` Deranged Burst, `uw005` Wild Slash, `uw006` Berserker
Fury, `uw007` Last Resort : en coût ; `uw008` Desperate Regenerate, `uw012`, `uw013`, `uw016` : en effet) ; trois la **lisent**
(`uw002` Griffes : « for each card you discarded at random this round », `uw003` Phoenix : « when Phoenix is discarded at
random », `uw009` Winter Mask : « after you discard a card at random »).

**Mécanisme moteur** (CORRECTIF du 25/10/2026) :
- `joueur.DiscardRandomHandCards(n, effect, exclude=[...])` (`player_action.py`) est LE point d'entrée de toute défausse au
  hasard, déjà employé par ~40 cartes officielles (Taskmaster, Absorbing Man...). Il tire (`Rand.RandomChoice2`, déterministe sous
  le harnais), défausse, et — nouveau — **pose la marque** `world.defausses_au_hasard` (la liste des faces tirées, le temps de
  la défausse) et **compte** ces défausses dans `world.stat` (`RecordRandomDiscard`, lu par `CountRandomDiscards(joueur)`, remis à
  zéro par `stat.OnRoundEnd()` en fin de round). `exclude` écarte la carte qu'on est en train de jouer.
- Lire « at random » dans une capacité : `message.trigger in world.defausses_au_hasard` (helper `DefausseAuHasard(message)` du
  pack) sur `WhenCardWouldDiscard` / `AfterCardDiscard`. Une défausse CHOISIE ne pose pas la marque.
- En COÛT : `CostFunc.Custom(None, DefausserAuHasard)` (helper `CoutDefausseAuHasard()`), doublé de `conditions=[UneCarteADefausser]`
  (RECETTES-MOTEUR §5 : un coût Custom qui peut échouer exige la même condition). La carte tirée est gardée sur l'effet
  (`effect.uw_defaussee`) : X = `FacesCounter.GetPrintedCost([carte])`, 0 pour une carte sans coût imprimé (ressource de base).

**Carte exemple** : `uw006` Berserker Fury (coût + X), `uw003` Phoenix (lecture de la marque), `uw002` (lecture du compteur).

**Pièges connus** :
- Une carte REMPLACÉE par une interruption (Phoenix, qui entre en jeu à la place) n'est pas défaussée : elle ne compte ni pour les
  Griffes ni pour Winter Mask, mais son coût imprimé fait quand même le X de la carte qui l'a tirée.
- Le compteur du round ne se remet pas à zéro tout seul dans le harnais : `Puzzle.ResetRoundStats()` après `Puzzle.SendRoundEnd()`.
- `Puzzle.DiscardAtRandom(n)` défausse n cartes AU HASARD par la même voie que les cartes ; `Puzzle.EmptyHand()` est une défausse
  ORDINAIRE (le témoin « choisie, pas au hasard »). ⚠ `Puzzle.Gain('X', 'X')` ne donne qu'UNE carte pour deux fois le même id.
- Payer l'événement avec la SEULE autre carte de la main : la défausse au hasard n'a plus de carte, le coût échoue, la carte jouée
  reste en main (cas `uw004`, rien n'est perdu).

**« Repeat this ability » (uw006, 26/10/2026)** : répéter une capacité à coût de défausse au hasard REJOUE le coût (FAQ du RR v1.8, Across the Spider-Verse : « repeating the ability includes the repeat effect itself ») : `DefausserAuHasard([], effect)` retire une NOUVELLE carte (nouveau X dans `effect.uw_defaussee`), la répétition n'est pas proposée si `UneCarteADefausser(effect)` est faux, et elle peut se répéter à son tour. Différence avec `35008` Berserker Barrage, dont la répétition n'a pas de coût avant la flèche.

**Variantes maison** : aucune.
