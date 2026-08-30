# Index des fiches mots-clés

Gabarit à copier pour chaque nouvelle fiche :

```markdown
# <Mot-clé>

**Texte imprimé / définition** : ...

**Mécanisme moteur** : ...

**Carte exemple** : `<card_id>` : <nom>, extrait du `.py` correspondant
(ou « lu directement depuis `desc`, aucun script requis »).

**Pièges connus** : ...

**Variantes maison** : ...
```

## Officiels

- [x] toughness.md
- [x] guard.md
- [x] quickstrike.md
- [x] retaliate.md
- [x] restricted.md
- [x] permanent.md
- [x] surge.md
- [x] villainous.md
- [x] hazard.md
- [x] crisis.md
- [x] acceleration.md
- [x] amplify.md
- [x] steady.md
- [x] stalwart.md
- [x] peril.md
- [x] incite.md
- [x] patrol.md
- [x] hinder.md
- [x] vulnerable.md
- [x] teamup.md
- [x] alliance.md

## Maison

- [x] drain-x.md (pack `agent_anti_venom`)
- [x] traitor.md (pack `agent_anti_venom`)
- [x] companion.md (pack `lockjaw`)
- [x] squirrel.md (pack `squirrel_girl`)
- [x] investigate-x.md (pack `jessica_jones`)
- [x] setlist.md (pack `dazzler`)
- [x] showtime.md (pack `dazzler`)
- [x] plotting.md (pack `scarlet_spider`)

## Packs passés en revue, aucun mot-clé imprimé propre trouvé

Vérification faite avec l'heuristique `<b>([A-Z][a-zA-Z ]{2,20})</b>` sur
`desc.text`/`text` de chaque carte du pack dans
`Fusion/marvel-lcg-src/data/cards.json` (voir Task 15). Dans les 13 packs
listés ci-dessous, chaque occurrence de `<b>...</b>` trouvée est un label
de type d'aptitude standard officiel (Action, Response, Interrupt, Hero
Action, Hero Interrupt, Hero Response, Hero Resource, Alter-Ego Action,
Alter-Ego Response, Resource, Setup, Special, Boost, Forced Response,
Forced Interrupt, When Revealed, When Defeated) : aucun terme en gras
propre au pack, donc aucun mot-clé maison à cataloguer.

- **`rainy`** (Thor/Jane Foster) : aucun terme en gras hors labels
  d'aptitude standards.
- **`albert`** (Wolverine robot) : idem.
- **`gwenpool`** : la mécanique des BULLES (texte à trous résolu par
  `ResolveBlank()` dans `cards/pack/gwenpool/gwenpool/__init__.py`) n'est
  matérialisée par aucun mot en gras sur le texte imprimé des cartes ; ce
  n'est pas un mot-clé, c'est un mécanisme de remplissage de texte propre à
  ce set.
- **`human_torch`** : les compteurs `flame` (Flame On!) ne sont jamais
  nommés en gras dans le texte imprimé ; simples compteurs de carte.
- **`mister_fantastic`** : mécanique « main vidée puis rechargée », aucun
  mot en gras propre.
- **`the_thing`** : les jetons Tenace (gagnés puis dépensés via Give 'Er /
  Take That!) ne sont jamais imprimés en gras dans `desc.text` ; simples
  jetons de carte, pas un mot-clé.
- **`totally_awesome_hulk`** : identité à trois faces et compteurs `rage`
  pilotant les changements de forme, aucun terme en gras propre au pack.
- **`invisible_woman`** : identité triple face, aucun terme en gras propre.
- **`cloak_dagger`** : mécanisme `linked_identity` (deux identités pour un
  joueur), aucun terme en gras propre ; les seules balises non standards
  rencontrées (`<hr>` sur `iw016`/`iw017`, pack `invisible_woman`) sont de
  la mise en forme, pas un mot-clé.
- **`spider_man_rainy`** : compteurs `web` (toile), aucun terme en gras
  propre.
- **`venom_rainy`** : aucun terme en gras propre.
- **`moon_knight`** : identité à cinq faces + set modulaire « Age of
  Khonshu », aucun terme en gras propre.
- **`brawn`** : la zone **Réserve** (nouvelle zone de joueur ajoutée au
  moteur, documentée en détail au §9 de `GUIDE-CREATION-CONTENU.md`,
  ligne « La zone RÉSERVE ») est un mécanisme maison majeur, mais son nom
  n'apparaît **jamais en gras** sur le texte imprimé des 26 cartes du pack
  (vérifié par balayage complet des balises `<b>` de `brawn` : seuls les
  labels d'aptitude standards y figurent) ; les cartes y font seulement
  référence en texte normal (« put this card into your reserve »). Selon
  le critère de cette tâche (mot-clé = terme en gras sur carte imprimée),
  ce n'est pas un mot-clé à ficher ici, malgré son importance mécanique :
  le mécanisme reste documenté au §9 du guide, pas dans ce catalogue.
- **`speed`** (Tommy Shepherd, set 130, 30/08/2026) : les **compteurs
  explosifs** de l'insert du pack sont un mécanisme maison central, mais le
  terme n'est **jamais imprimé en gras** — balayage complet des balises `<b>`
  des 23 cartes : `Action`, `Alter-Ego Action`, `Forced Interrupt`, `Forced
  Response`, `Hero Action`, `Hero Interrupt`, `Hero Response`, `Interrupt`,
  `Resource`, `When Revealed`, la ligne « Give to the Thomas Shepherd
  player. », et **`Permanent`** (sd018), qui a déjà sa fiche. Même critère que
  la Réserve de `brawn` et que les compteurs `flame` de `human_torch` : ce sont
  des compteurs de carte, pas un mot-clé. Le mécanisme est documenté en tête de
  `src/cards/pack/speed/speed/__init__.py` et dans `docs/speed_cartes.md`.
  `Quickstrike` (sd019) est imprimé sans gras mais possède déjà sa fiche.

Quatre packs supplémentaires, absents du §9 du guide et inaccessibles
depuis ce worktree (existent uniquement dans un checkout non lié), ont été
vérifiés directement par l'agent contrôleur avec la même heuristique
`<b>` : conclusion transmise et reprise ici telle quelle.

- **`wolverine_x23`** : un seul helper de script par carte (ex.
  `EstTonHeros`), aucun mot-clé en gras correspondant sur le texte
  imprimé.
- **`red_guardian`** : un seul helper de script par carte (ex.
  `BouclierEnJeu`), aucun mot-clé en gras correspondant sur le texte
  imprimé.
- **`jj`** : `__init__.py` du pack entièrement vide, aucun mécanisme
  maison d'aucune sorte.
- **`luke_cage`** : `__init__.py` du pack entièrement vide, aucun
  mécanisme maison d'aucune sorte.
