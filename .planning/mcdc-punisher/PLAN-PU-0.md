# PU-0 : préparation Punisher MC×DC 2026 (20/10/2026)

Lot PU-0 du découpage `docs/rapports/cadrage-14-15-19-2026-10-20.md` §1.7. Préparation uniquement :
aucun script de capacité, aucune insertion dans `data/cards.json`, aucune modification de
`Fusion/marvel-lcg-src/src/`.

## Choix fait au point 3 (données préparées, pas seulement un plan)

Un fichier de données brutes a été écrit (`.planning/mcdc-punisher/defs/punisher_cards.py`), et pas
seulement ce plan, parce que :
- Le cadrage lui-même range explicitement « `cards.json` (données sans scripts) » dans le périmètre de
  PU-0 (§1.7, ligne PU-0 : « Préfixe, scans, `cards.json` (données sans scripts), sets, levée des `[?]`,
  fiches mots-clés »).
- Le fichier ne contient que des dictionnaires (`card_id`, `type`, `name`, `desc`, `traits`, `text`,
  `set_name`) — strictement ce que demande la consigne « juste les dictionnaires de données brutes »,
  sur le modèle structurel de `.planning/galactic-storm/defs/majestrix_cards.py` (un pack préparé la
  même semaine, par un agent différent, pour le même cadrage).
- Rien n'est exécutable comme capacité de jeu : pas d'`AbilityFactory`, pas d'import du moteur, pas de
  `src/cards/pack/...`. Le fichier ne touche à rien hors de `.planning/`.
- Il reste à relire par un agent fort avant le portage (la convention `card_id` proposée dans l'en-tête
  du fichier n'a pas été validée par l'utilisateur ni par un second agent).

## Contenu préparé

| Set | Cartes physiques | `card_id` distincts | Page de départ (scan) |
|---|---|---|---|
| Jigsaw | 15 | 13 | p111 |
| Hobgoblin | 15 | 14 | p141 |
| Punisher's Armory | 5 | 5 | p227 |
| The Syndicate | 7 | 7 | p261→p249 |
| Capo of the Past | 1 | 1 | p277 |
| **Total** | **43** | **40** | |

Non préparé (hors périmètre « simple » de la section 1.3 du cadrage, laissé pour plus tard) :
- **SWAT Team** (6 cartes) : exclu du texte du mandat PU-0 lui-même (qui liste « Jigsaw, Hobgoblin,
  Syndicate, Armory, Capo of the Past », sans SWAT), probablement parce que SWAT introduit une mécanique
  neuve (jeton recherché, fiche `docs/reference/mots-cles/jeton-recherche.md` créée ce jour) plutôt
  qu'un contenu purement « M6-M9 ».
- **Punishment** (set du méchant final, 20 cartes), **The Big Apple**, **Uptown**, **Locations**, **Leads**,
  **CAPOS**, **Punisher's Hit List**, les cartes de campagne, les 4 défis, Hawkeye MC×DC : dépendent des
  briques M1/M2/M3/M5 (lieux, territoires, pistes) ou de décisions utilisateur encore ouvertes (voir
  `.planning/todos/2026-10-20-punisher-questions.md`), donc hors lot PU-0.

## Ordre pour la suite (rappel du cadrage §1.7, PU-1 à PU-4)

1. **PU-1 aurait dû porter les briques M6/M7** : **déjà fait**, trouvé en relisant
   `docs/reference/mots-cles/README.md` et `docs/reference/RECETTES-MOTEUR.md` §16 avant d'écrire les
   nouvelles fiches de ce lot — `src/game/operate/immunity.py`, `src/game/operate/villains.py` et
   `AbilityFactory.CannotBeAffectedByPlayerCards` existent déjà dans le moteur (écrits le 20/10/2026 pour
   Galactic Storm, pensés dès le départ comme réutilisables pour Punisher). PU-1 est donc à sauter ou à
   réduire à une vérification carte par carte pendant PU-2/PU-4.
2. **PU-2** (Jigsaw + Hobgoblin + 20 scénarios `fne`) peut partir directement de
   `.planning/mcdc-punisher/defs/punisher_cards.py` pour Jigsaw et Hobgoblin.
3. **PU-3** (Syndicate, Hit List, Armory, SWAT, Capo of the Past) peut partir du même fichier pour
   Syndicate, Armory et Capo of the Past ; Hit List et SWAT restent à préparer (SWAT a sa fiche mot-clé,
   pas encore ses données).
4. **PU-4** (Punishment, 20 cartes) : pas préparé ici, dépend de la carte Target Lock (M8, déjà « petit »
   au cadrage) et du méchant Punisher actif/CIBLÉ (M7, déjà couvert par les fiches communes).

## Incertitudes à lever avant de coder (pas des décisions utilisateur, des vérifications techniques)

- La convention `card_id` proposée (voir en-tête de `punisher_cards.py`) n'est qu'une proposition : à
  confirmer qu'elle ne collisionne avec aucune autre carte `pu` future (Punishment ira sans doute de
  `pu086` à `pu113` d'après la suite des ID MC×DC 6086-6113, à vérifier avant de les préparer).
- `p155 Torn to Pieces` est cataloguée « Obligation » dans `cartes.md` mais range ici en `Treachery` par
  erreur de copie du gabarit : à corriger en `Obligation`/type correct au moment du portage (noté aussi en
  commentaire dans le fichier de données).
- `p277 Capo of the Past` est une carte « Attachement » dans `cartes.md` qui porte un `When Revealed` (texte
  normalement réservé aux cartes de rencontre révélées, pas aux attachements posés par une autre carte) :
  son type exact (`Treachery` qui s'attache, ou `Attachment` avec un décalque de `When Revealed`) est à
  trancher sur un modèle existant du dépôt au moment du portage.
