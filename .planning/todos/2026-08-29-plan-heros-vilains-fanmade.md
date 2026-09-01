# PLAN — Ordre de création des héros/vilains fan-made du dossier « A créer »

**Statut :** 📋 Plan prêt. Rien n'est encore créé — seuls les 21 préfixes/numéros de
set ont été réservés dans `tools/prefixes_fanmade.json` (`cartes: 0`, note
"RESERVE"), pour que plusieurs sessions puissent démarrer des héros différents
en parallèle sans se marcher dessus.
**Origine :** demande utilisateur — 22 zips de héros/vilains fan-made
accumulés dans `A créer/`, à trier par difficulté et à ordonner pour
maximiser la réutilisation de mécaniques du moteur d'un pack à l'autre.
**Méthode :** 23 agents ont chacun dézippé un pack, lu son rulebook/ses
cartes (texte réel, pas juste les noms de fichiers), et vérifié dans
`src/` quelles mécaniques repérées existent déjà dans le moteur.

---

## 1. Ce qui a été écarté avant même d'entrer dans le plan

| Zip | Raison |
|---|---|
| **THE SPOT (3.0)** | Déjà livré (préfixe `sp`, 21 cartes), exclu à la demande de l'utilisateur. |
| **The Lizard** | Doublon exact : déjà entièrement porté dans `src/cards/pack/web_of_deceit/the_lizard/` (préfixe `wd`, 18 fichiers). Rien à faire, ne pas re-créer. |
| **Doctor Doom Alt Arts** | Même kit de cartes que « Doctor Doom Hero Revised » (mêmes 15 noms, même total), signé du même illustrateur ("Alt Art Custom by Grawlix Ipsum") — un jeu d'illustrations alternatives, pas un pack indépendant. À comparer texte par texte au moment du portage de `dd` (Doctor Doom) et à ne garder que pour ses images si le texte est identique. |
| **OneDrive_2026-08-29.zip** | Pas un fourre-tout de synchro comme le nom le laissait penser : c'est en fait le pack complet **Iron Patriot** (Norman Osborn). Réintégré dans le plan sous ce nom (préfixe `ip`). |

21 items restent : 19 héros/vilains + 2 campagnes complètes (mises en fin de
liste, cf. §4).

## 2. Logique de l'ordre

Les items sont groupés par ce qu'ils demandent au **moteur**, pas par ordre
alphabétique ni par popularité du personnage :

- **Groupe A — assemblage pur, zéro primitive nouvelle (difficulté 2/5).**
  Certains sont des quasi-clonages directs d'un pack déjà codé (Hawkeye Kate
  Bishop ← pack `trors/hawkeye`, Okoye ← pack `bp`, Superior Iron Man ← pack
  `core/iron_man`) : les faire tôt donne des gabarits de code réutilisables
  pour le reste du groupe.
- **Groupe B — une brique vraiment neuve mais isolée (difficulté 3/5).**
  Tout le reste du pack est standard ; une ou deux cartes demandent une
  petite mécanique sur-mesure sans précédent exact.
- **Groupe C — un sous-système moteur à concevoir (difficulté 4/5).**
  Le pack entier tourne autour d'un concept qui n'existe nulle part dans le
  moteur (nouveau type de ressource, héros qui devient un attachment, deck
  imbriqué). Plus lourd, à faire une fois les réflexes pris sur les groupes
  A/B.
- **Groupe D — campagnes complètes (difficulté 5/5), en fin de liste**,
  décision utilisateur : ampleur d'une extension officielle, à traiter à
  part quand le reste sera rodé.

## 3. Le plan, dans l'ordre

Numéro de set = déjà réservé dans `tools/prefixes_fanmade.json` (le
prochain set libre après Dazzler `123` était `124`).

### Groupe A — clonage direct / assemblage standard (2/5)

| # | Set | Préfixe | Héros/Vilain | Réutiliser | Point notable |
|---|---|---|---|---|---|
| 1 | 124 | `kb` | **Kate Bishop** (Hawkeye) | `trors/hawkeye` (compteurs de flèches identiques) | ✅ PORTÉ. ~~Allié "Hawkeye" référencé mais absent du zip — piocher dans `trors/hawkeye`.~~ **RÉSOLU** : la carte a été créée à l'identique (`kb002`, allié 2/2 PV, ATQ 2\*, CTR 1\*, ressource wild, AVENGER), pas substituée par une carte officielle. Scan de l'auteur (CptScorp, « HAWKEYE 1/15, Cycle 2 ») fourni par l'utilisateur le 01/09/2026 et **comparé point par point** à `kb002` : coût, PV, stats, traits, texte et image concordent. Rien à réclamer. |
| 2 | 125 | `ok` | **Okoye** | pack officiel `bp` (Aneka/Ayo/Okoye déjà codées) | Attention aux collisions de noms de cartes avec les versions officielles. |
| 3 | 126 | `si` | **Superior Iron Man** | `core/iron_man` | Re-skin complet façon Wolverine X-23. Le zip contient du texte structuré (`xb-cards.json`) mais sans le texte de règles — a fallu lire quelques images quand même. |
| 4 | 127 | `il` | **Iron Lad** | `ironheart` (trait TECH, compteurs) | Rien de neuf, assemblage standard. |
| 5 | 128 | `ss` | **Kaine Parker** (Scarlet Spider) | `spdr`/`wsp`/`jj` (excess damage) | Pack nommé `kaine_parker` exprès, pour ne pas collisionner avec un futur Ben Reilly. |
| 6 | 129 | `vp` | **Venompool** | `deadpool` + `vnm` | Mot-clé "Plotting" à écrire (hook `AfterMinionEngagePlayer` déjà présent, juste jamais branché sur un scheme auto). |
| 7 | 130 | `wc` | **Wiccan** | `agent_13` (comptage d'icônes boost) | Pattern quasiment copiable tel quel. |
| 8 | 131 | `ho` | **Harry Osborn** (New Ultimate Green Goblin) | `core/iron_man` (TECH) + `she_hulk`/`dazzler` (Persona) | C'est un pack **HÉROS**, à ne pas confondre avec le pack VILAIN officiel `gob` (Green Goblin classique) déjà dans le moteur — même nom de carte Obligation ("Risky Business") dans les deux, coïncidence à signaler. |
| 9 | 132 | `aa` | **Agatha Harkness** | `she_hulk`/`dazzler` (Persona) + `mister_fantastic_nemesis` | Carte "Agatha All Along" référencée mais absente du zip, à réclamer. |
| 10 | 133 | `an` | **Angela** | `red_guardian` / `wolverine` | Thème Weapon/frenzy déjà bien couvert par le moteur. |
| 11 | 134 | `bt` | **Beast** (Hank McCoy) | `red_guardian` (squelette) | Mini-pool "Discovery" (5 cartes hors-deck) à construire sur le pattern `set_aside_deck` déjà utilisé par Iceman/Storm/Valkyrie/Wonder Man. |
| 12 | 135 | `hd` | **Howard the Duck** | `next_evol/cable` / `mts/loki` (victory display) | Une carte à vérifier de près : "Nexus of All Realities" (choix de la zone où un personnage entre en jeu), aucun précédent trouvé dans le moteur. |
| 13 | 136 | `gb` | **Gorr the God Butcher** | `mts/thanos` (deck-out trigger) | C'est un pack **VILAIN** (scénario), pas un héros — 34 cartes, le plus gros du groupe A. Dépend d'un set modulaire externe "Intergalactic Hazards" absent du zip, à créer ou substituer. |

### Groupe B — une brique neuve isolée (3/5)

| # | Set | Préfixe | Héros/Vilain | Ce qui est vraiment neuf |
|---|---|---|---|---|
| 14 | 137 | `ma` | **Ms. America** | Le minion nemesis (Catalina Chavez) copie les modificateurs de stat du joueur en substituant l'icône THW→SCH — aucune primitive de ce type trouvée. |
| 15 | 138 | `pt` | **Patriot** | Deux cartes nemesis (Commandeer, Commander's Orders) : déplacement d'un attachment entre personnages avec texte neutralisé, et échange de valeurs ATK/THW. Le trait "Young Avenger" est aussi à créer (mais c'est juste un trait, pas une mécanique). |
| 16 | 139 | `dd` | **Doctor Doom** | Bascule de statut "villainous" pilotée par des compteurs de power (primitives existantes, cf. Moon Knight AoK/Cyclops/Phoenix) + une exception de deckbuilding multi-aspect ("6 cartes Tech/Spell d'un autre aspect") sans équivalent trouvé, à valider. Fusionne "Hero Revised" (règles) et "Alt Arts" (mêmes cartes, art alternatif). |

### Groupe C — sous-système moteur à concevoir (4/5)

| # | Set | Préfixe | Héros/Vilain | Le sous-système à construire |
|---|---|---|---|---|
| 17 | 140 | `al` | **Alligator Loki** | Le héros lui-même devient un attachment mobile posé sur un ennemi (Interrupt d'attaque/défense + détachement Forced Response) — concept sans aucun précédent dans le moteur. |
| 18 | 141 | `sd` | **Speed** | Un 5ᵉ type de ressource ("⚡", utilisée sur 5 des 15 cartes) — la classe `Resources` du moteur est figée sur R/B/Y/G, aucune carte n'utilise un 5ᵉ type. Vraie extension moteur, pas juste une carte. |
| 19 | 142 | `ip` | **Iron Patriot** | Un deck secondaire de 20 cartes "REGISTERED" attaché au héros (pioche/révélation/engagement séparés du deck de rencontre, conversion minion→allié, conversion carte→ressources) — un mini gestionnaire de deck à part entière, le plus lourd des héros hors campagnes. |

### Groupe D — campagnes complètes, fin de liste (5/5)

| # | Set | Préfixe | Campagne | Ampleur |
|---|---|---|---|---|
| 20 | 143 | `sk` | **Skrull Menace** | 4 scénarios, 5 vilains/nemesis jouables, système "Cooperation Area"/victory display, ~27 cartes joueur. Rulebook 24 pages. Placée avant Galactic Storm : pas de nouveaux héros à stater entièrement. |
| 21 | 144 | `gs` | **Galactic Storm** | 5 scénarios + 2 interludes + épilogue, 305 cartes, 4 sets modulaires additionnels, **2 nouveaux héros jouables à créer de toutes pièces** (Binary, Quasar). La plus lourde de tout le lot. |

## 4. Comment lancer plusieurs sessions en parallèle sans collision

Chaque héros/vilain retenu a déjà son préfixe de 2 lettres et son numéro de
set réservés dans `tools/prefixes_fanmade.json` (entrées `"cartes": 0`,
note `RESERVE`). Une session qui démarre un portage :

1. Prend un item de ce plan (dans l'ordre, ou pas — les préfixes ne
   collisionnent pas entre eux quel que soit l'ordre réel de traitement).
2. Écrit les cartes sous le préfixe déjà réservé, sans toucher au préfixe
   d'un autre item.
3. Met à jour `cartes` et retire la mention `RESERVE` dans
   `tools/prefixes_fanmade.json` une fois le pack livré, et ajoute
   l'entrée correspondante dans `data/sets_info.json`.
4. Lance `python3 tools/verifier_prefixes.py` avant de committer : aucun
   défaut n'est attendu.

`git status`/`git diff` restent le seul vrai risque de collision : deux
sessions qui travaillent dans le **même clone** en même temps sur des
fichiers centraux partagés (`data/cards.json`, `data/sets_info.json`)
s'écraseront quand même l'une l'autre. Deux checkouts séparés (`git
worktree`) restent recommandés pour un vrai travail en parallèle.

## 5. Points à trancher avant de lancer le premier portage

- **Gorr the God Butcher** dépend d'un set modulaire "Intergalactic
  Hazards" absent du zip fourni — à créer ou remplacer avant de livrer le
  pack.
- **Doctor Doom** : comparer carte par carte "Hero Revised" et "Alt Arts"
  avant portage, pour confirmer qu'il s'agit bien du même texte de règles.
- **Agatha Harkness** : ~~carte "Agatha All Along" absente du zip, à
  réclamer~~ ✅ **FOURNIE** par l'utilisateur et portée (`aa008`,
  manigance-joueur). **Reste ouvert, en revanche** : elle existe en deux
  versions, **13 menaces** (planche du zip) et **10** (Discord de l'auteur),
  textes identiques par ailleurs. 13 retenues sur arbitrage utilisateur du
  31/08/2026 ; c'est un vrai choix d'équilibrage, la carte se vidant en
  encaissant des attaques. Seul point de ce §5 qui vaudrait encore une
  question à l'auteur.
- ~~**Kate Bishop**~~ ✅ **RÉSOLU le 01/09/2026** : l'allié Hawkeye (Clint
  Barton) a bien été créé à l'identique dans le pack (`kb002`), et non
  substitué par la version officielle. Le scan de l'auteur, fourni par
  l'utilisateur, concorde en tout point. **Ne plus le compter comme un point
  ouvert** : cette ligne du plan datait d'AVANT le portage.
- ~~**Patriot**~~ ✅ **RÉSOLU** : l'allié spécifique existe (`pt002`
  « * Hawkingbird », Kate Bishop, trait YOUNG AVENGER), avec son script, son
  image et sa place dans le deck de départ. Ligne également antérieure au
  portage.

> ⚠ **Leçon du 01/09/2026** : ce paragraphe a été écrit AVANT les portages et
> a été relu ensuite comme s'il décrivait l'état courant, ce qui a fait
> annoncer à tort deux points ouverts (Kate Bishop, Patriot). **Toujours
> vérifier dans `data/cards.json` et `deck/starter/` avant de citer une
> lacune de ce plan.**

Anciennement à créer
  (Patriot).
