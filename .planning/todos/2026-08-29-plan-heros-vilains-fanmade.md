# PLAN — Ordre de création des héros/vilains fan-made du dossier « A créer »

> **Rangement du 05/09/2026.** Les zips ne sont plus a la racine : ceux dont
> le pack existe sont dans `paquets-cartes/`, ceux qui restent a porter dans
> `A creer/`. Les chemins cites plus bas (« zips deposes a la racine »,
> « A creer/Galactic Storm ») datent d'avant. `OneDrive_2026-08-29.zip` a ete
> renomme `Iron Patriot-20260829T085900Z-1-001.zip`, son vrai contenu.
> Les doublons Galactic Storm et Skrull Menace (exports du 13/08 et du 02/09)
> cohabitent desormais dans `A creer/`, rien n'a ete supprime.

**Statut au 02/09/2026 :** 18 des 21 items sont LIVRÉS, plus deux sets
modulaires non prévus au plan (`ih` Intergalactic Hazards, `nv` Necroverse).
Chiffres vérifiés dans `tools/prefixes_fanmade.json`, pas dans ce document.

| Reste du plan d'origine | Préfixe | État |
|---|---|---|
| Iron Patriot | `ip` | `cartes: 0`, jamais commencé |
| Skrull Menace | `sk` | `cartes: 0`, **matériel incomplet**, voir §7 |
| Galactic Storm | `gs` | `cartes: 0`, **matériel incomplet**, voir §7 |
| Doctor Doom Alt Arts | aucun | 16 cartes distinctes, pas de préfixe réservé |

⚠ La phrase « Rien n'est encore créé » qui occupait cette place datait du
29/08 et était fausse depuis le 31/08. Les tableaux du §3 sont eux aussi
antérieurs aux portages : ils décrivent le travail PRÉVU, pas l'état courant.
Toujours vérifier dans `tools/prefixes_fanmade.json`.
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
  Hazards" absent du zip fourni. ⚠ **INTROUVABLE** : ni officiel, ni dans
  nos packs, ni dans les zips Galactic Storm / Skrull Menace (vérifié le
  02/09/2026). Le texte de Deicide 1A ne fait que le **recommander**, un
  modulaire quelconque convient. **Décision de l'utilisateur (02/09/2026)** :
  le scénario propose **Légions de Hel** par défaut, en attendant.
  ➡ **TROUVÉ le 02/09/2026** : l'utilisateur a fourni deux dossiers Drive de
  **Patrick Burk**, tous deux à porter comme sets modulaires à part entière :
  - **Intergalactic Hazards [2.5]** —
    `https://drive.google.com/drive/folders/1AmHdjyKQcmjUM0SlWazmO0qeNPnYK0NW`
    (le modulaire recommandé par Deicide 1A) ;
  - **Necroverse [1.5]** —
    `https://drive.google.com/drive/folders/1S3Sm_N4uNZrANMNV6LLQrmeglo4xYG75`
    (le modulaire que le Setup met de côté et que le complot 3A mélange).

  ✅ **RÉGLÉ le 02/09/2026** : l'utilisateur a déposé les deux zips à la
  racine du projet, et les deux sets sont portés (`ih`, 6 cartes ; `nv`,
  8 cartes). Le complot 3A et le Setup de Gorr trouvent désormais le
  `set_name` « Necroverse » qu'ils cherchaient. Reste ouvert : remplacer
  Légions de Hel par Intergalactic Hazards dans `data/scenarios/gorr.json`,
  maintenant que le vrai modulaire existe.

  ⚠ **Conséquence déjà appliquée sur le pack Gorr** : les 34 cartes du zip
  forment UN SEUL set d'encartage (toutes portent « GORR THE GOD BUTCHER
  (x/34) » en pied). Le premier montage, qui coupait les 11 cartes au trait
  NECROVERSE pour en faire le modulaire, était faux. Le Setup et le complot
  3A cherchent le `set_name` « Necroverse » : ils ne trouvent rien tant que
  le set externe n'est pas porté, et fonctionneront sans changer une ligne
  le jour où il le sera.

  ⚠ L'utilisateur a présenté Necroverse comme « pour l'expert » : le texte
  de Deicide 1A dit autre chose (« Gorr the God Butcher, **Necroverse**, and
  Standard encounter sets », dans les deux modes). À reconfirmer avec lui au
  moment de porter le set.

  En attendant, `data/scenarios/gorr.json` et `gorr_expert.json` proposent
  **Légions de Hel** ; le joueur peut choisir un autre modulaire à l'écran de
  préparation.
- ~~**Doctor Doom** : comparer carte par carte "Hero Revised" et "Alt Arts"~~
  ✅ **TRANCHÉ le 01/09/2026** : ce ne sont PAS les mêmes cartes (16 cartes
  différentes dans "Alt Arts", aucun nom en commun). Pas de fusion ; le zip
  "Alt Arts" reste à traiter comme un pack à part.
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

---

---

## 6. Deuxième arrivage : 27 zips déposés à la racine le 02/09/2026

> ⚠ **Ce paragraphe a été réécrit le 02/09/2026 après une première version
> fausse.** La première tentative classait les packs à partir des NOMS de
> fichiers et de la seule carte d'identité, et concluait par exemple que Throg
> était « presque de l'assemblage » parce que le pack Alligator Loki contient
> des cartes nommées Throg et Frogjolnir. **Ce sont des cartes différentes, sans
> aucun code commun.** Le classement ci-dessous repose sur la lecture des 425
> cartes distinctes des 23 packs, une par une. C'est le même piège que la leçon
> du 01/09 en §5 : ne jamais citer une réutilisation sans avoir lu les deux
> cartes.

### 6.1 Quatre zips à écarter

| Zip | Raison |
|---|---|
| **Intergalactic Hazards [2.5]** | Déjà porté le 02/09 (`ih`, 6 cartes). |
| **Necroverse [1.5]** | Déjà porté le 02/09 (`nv`, 8 cartes). |
| **Galactic Storm** | Même arborescence que `A créer/Galactic Storm` (21 fichiers). |
| **Skrull Menace (Released)** | Même arborescence que `A créer/Skrull Menace` (39 fichiers). |

23 nouveaux items restent, 425 cartes distinctes.

### 6.2 Les six briques partagées, qui commandent l'ordre

Le facteur de coût n'est pas le pack, c'est la brique. Six briques reviennent
d'un pack à l'autre ; les écrire une fois sert à chaque fois.

| # | Brique | Packs qui en dépendent |
|---|---|---|
| 1 | **Provenance du paiement** : la carte sait avec QUELLE ressource, ou par QUEL chemin, elle a été payée | Throg, Beta Ray Bill, Hulk, Lady Sif, Spider-Man 2099, Spider-Woman, Venomized |
| 2 | **Zone « glissée sous » une carte**, persistante et invisible au `find` | Spider-Man Noir, Black Cat, Throg, Beta Ray Bill |
| 3 | **Sélection d'une carte par son TEXTE** (« portant Hero Action ou Hero Response ») | Black Cat, Sunfire, Doctor Druid |
| 4 | **Recherche dans toute la COLLECTION** (pas le deck) | Black Cat, Cameo compliment |
| 5 | **Pouvoir de base démultiplié** (résolu contre chaque manigance ou chaque sbire) | Throg, Beta Ray Bill, Ares, Blink |
| 6 | **Upgrade JOUEUR attachée à un ennemi ou à une manigance** | Ares, Sunfire, Blink, Yondu |

### 6.3 Difficulté réelle, pack par pack

| Pack | Auteur | Cartes | Diff. | Ce qui la fixe |
|---|---|---|---|---|
| **Viv Vision** | Rainy | 12 | 2/5 | Clone de Vision. Un seul mot-clé neuf, `breakthrough`, absent du moteur et des fiches. |
| **Hulk** | Rainy | 15 | 2/5 | Tout paie sur le changement de forme. Brique 1 sur 2 cartes. Pas de set nemesis. |
| **Iron Man (Model 42)** | Rainy | 15 | 2/5 | Une seule économie, les compteurs `reactor`. ⚡ = ressource ÉNERGIE officielle, pas un 5ᵉ type. |
| **Lady Sif** | Rainy | 18 | 2/5 | Prêter des ASGARD, chercher une WEAPON. Brique 1 sur 1 carte. |
| **Beta Ray Bill** | Rainy | 13 | 3/5 | Briques 1, 2 et 5 à la fois. Le motif Mjolnir n'est qu'une partie du pack. |
| **Throg** | Rainy | 17 | 3/5 | Briques 1, 2 et 5. Aucune réutilisation possible du pack `alligator_loki`. |
| **Spider-Man Noir** | Rainy | 16 | 3/5 | Brique 2, dans sa version la plus lisible : 8 cartes sur 16 la lisent. |
| **Sunfire** | Rainy | 16 | 3/5 | Briques 3 et 6. Pool BURNING de 6 upgrades qui font l'aller-retour avec la réserve. |
| **Ares** | Rainy | 15 | 3/5 | Brique 6 poussée loin : modificateurs de dégâts posés SUR l'ennemi, éponge à dégâts, sélection d'upgrade selon la légalité d'attache. |
| **Blade** | Rainy | 17 | 3/5 | Le set nemesis entier est mélangé au deck de rencontre AU SETUP, et deux cartes OCTROIENT DU TEXTE aux sbires. Mot-clé `teamwork` sans fiche. |
| **Spider-Man 2099** | Rainy | 19 | 3/5 | Brique 1 appliquée au CHEMIN de mise en jeu (6 cartes). Mot-clé maison `Seek`. Capacité « Acceleration » homonyme du mot-clé OFFICIEL. |
| **Blink** | Kajislav | 24 | 3/5 | Brique 6 : les PORTAL s'attachent aux ennemis ET aux manigances. Deux hooks neufs (carte qui entre en main, upgrade défaussée du jeu). |
| **Yondu** | BlueHG + DesignHacker | 20 | 3/5 | Brique 6 + mot-clé maison `summon` + « la prochaine carte dépensée compte double ». Decklist fournie. |
| **Night Thrasher** | DesignHacker | 19 | 3/5 | Mot-clé maison `agile X`, Battle Board recto-verso, mémoire de la dernière carte jouée. ⚠ contient une carte étrangère (MAGMA NEMESIS 2/5). |
| **Texas Twister** | Kajislav | 28 | 3/5 | Mécanique 2/5, volume 3/5 : 8 cartes d'aspect génériques et un trait RANGER à créer. Défaut d'écriture sur Lone Star Rangers. |
| **Armored Spidey** | Kajislav | 30 | 3/5 | Spider Armor recto-verso à compteurs (motif Godbomb), plus 9 cartes d'aspect génériques qui entrent dans le pool commun. |
| **Spider-Woman** | Kajislav | 32 | 3/5 | Compteurs `psionic web`, annulation des icônes boost une par une, brique 1. Le plus gros pack héros, avec un nemesis livré en deux versions. |
| **Venomized** | ekAugust | 38 | 3/5 | Un ASPECT complet. Mot-clé `weakness` et règle de deckbuilding au coût cumulé. Recette connue via `determination`. |
| **Black Cat** | Rainy | 13 | 4/5 | Briques 2, 3 et 4 réunies, plus substitution d'icônes boost, annulation d'activation et mot-clé `Multiverse` non défini dans le zip. |
| **Cameo compliment** | BlueRiver | 3 | 4/5 | 3 cartes, mais brique 4 seule : chercher dans tout le catalogue une carte d'une identité absente, avec l'écran qui va avec. |
| **Superior Spider-Man** | Rainy | 22 | 4/5 | Mot-clé `Track` : de la MENACE SUR UN SBIRE, état de jeu inexistant. Plus DEUX alter-ego au choix avec chacun son obligation. |
| **Doctor Druid** | Kajislav | 17 | 4/5 | 8 cartes produisent un effet CONTINU DEPUIS LA MAIN. Recalcul à chaque changement de main, et le bot doit comprendre qu'une carte gardée vaut quelque chose. |
| **Muse** | Rainy | 6 | 4/5 | 6 cartes, mais 5 demandent « une carte qui porte l'illustration de ton identité ». Donnée absente du moteur pour tout le catalogue. Décision de conception à prendre avec l'utilisateur. |

### 6.4 Ordre conseillé

**Vague 0, quatre vrais 2/5 pour se remettre en route** : Viv Vision, Hulk,
Lady Sif, Iron Man (Model 42). Hulk et Lady Sif font écrire la brique 1 sur deux
cartes faciles, là où elle est vérifiable à l'œil.

**Vague 1, la brique 1 rentabilisée** : Beta Ray Bill, Throg. Ils ajoutent la
brique 2 dans sa forme la plus simple (une seule carte glissée) et la brique 5.

**Vague 2, la zone glissée** : Spider-Man Noir (la zone comme ressource, 8 cartes
la lisent), puis Black Cat (la même zone plus la substitution d'icônes et la
recherche en collection), puis Cameo compliment (3 cartes, qui ne fait que
réutiliser la recherche en collection).

**Vague 3, les upgrades posées sur les ennemis** : Sunfire, Ares, Blink, Yondu.
Quatre variantes de la brique 6, de la plus simple à la plus mobile.

**Vague 4, les gros packs autonomes** : Blade, Spider-Man 2099, Night Thrasher,
Texas Twister, Armored Spidey, Spider-Woman. Aucun ne dépend des autres, chacun
apporte un mot-clé maison ou du volume.

**Vague 5, les chantiers** : Venomized (un aspect entier, le plus rentable des
quatre), Iron Patriot (reste du plan d'origine), Superior Spider-Man, Doctor
Druid, Muse (à trancher avec l'utilisateur avant tout code).

**Hors vague** : Doctor Doom Alt Arts, 2/5 et sans dépendance, à faire quand on
veut. Skrull Menace et Galactic Storm restent bloqués, voir §7.

## 7. ⚠ Les deux campagnes sont incomplètes dans le matériel fourni

Vérifié le 02/09/2026 en listant les deux zips, dans leurs deux copies
identiques (`A créer/` et racine).

**Skrull Menace** (39 fichiers) ne contient que la couche campagne : 7 alliés,
7 manigances-joueur, 6 soutiens, 6 upgrades, le livret 24 pages et les visuels
de boîte. **Aucun vilain, aucun complot principal, aucun set de rencontre.** Or
le carnet de campagne (page 22) compte 4 scénarios avec « Shaper of Worlds » et
« Cosmic Cube Creation », et la feuille de coopération (page 24) réclame Skrull
Spy, Skrull Warrior, Skrull Soldier, Skrull Commander, Hijacked, Cloning
Program, Emperor's Throne, Plotting Revenge, Seeking a Suitable World : rien de
tout cela n'est dans le zip. Le livret annonce aussi des **formes
supplémentaires** de héros (« origin form » de Hulkling), donc des héros
absents eux aussi.

**Galactic Storm** (21 fichiers) : 3 alliés de campagne, 10 alliés liés à une
identité, le livret 24 pages, les visuels de boîte. Ni les 5 scénarios, ni les
4 modulaires, ni Binary, ni Quasar.

➡ **À demander à l'utilisateur avant de planifier ces deux campagnes** : les
zips des scénarios eux-mêmes. En l'état, les porter voudrait dire inventer les
cartes à partir du livret, ce qui n'est pas du portage.

## 8. Mots-clés maison rencontrés, à ficher avant d'écrire une ligne

Vérifié dans `src/` et dans `docs/reference/mots-cles/` le 02/09/2026.

| Mot-clé | Pack | État |
|---|---|---|
| `breakthrough` | Viv Vision | absent du moteur ET des fiches |
| `agile X` | Night Thrasher | absent du moteur ET des fiches |
| `Seek` | Spider-Man 2099 | absent ; défini par l'insert du pack |
| `summon` | Yondu | absent ; à déduire des cartes, pas d'insert |
| `Track` | Superior Spider-Man | absent ; défini par l'insert du pack |
| `weakness` | Venomized | absent ; défini par l'insert du pack |
| `Multiverse` | Black Cat | le mot existe dans `card_face.py`, mais comme TRAIT chez Blink (Earth-295) et comme MOT-CLÉ chez Black Cat. Deux notions, à ne pas confondre. Le zip Black Cat ne le définit pas : question à l'auteur. |
| `teamwork (VAMPIRE)` | Blade | présent dans les fabriques `environment` du moteur, sans fiche |
| `Acceleration` | Spider-Man 2099 | ⚠ homonyme total du mot-clé OFFICIEL déjà fiché. Annoter `acceleration.md`. |

---
## 6. ARRIVAGE DU 02/09/2026 : 25 zips déposés à la racine

L'utilisateur a déposé ce jour-là une fournée de zips à la racine du
dépôt (`*.zip`), non suivis par git. Deux ont été portés dans la foulée
(Intergalactic Hazards et Necroverse, les deux modulaires de Gorr) ; les
autres attendent. Cette liste n'a PAS été triée par difficulté ni
croisée avec `data/cards.json` : le faire avant d'en annoncer un comme
manquant, comme le rappelle l'encart en fin de §3.

- `Ares`
- `Armored Spidey (Released)`
- `Beta Ray Bill`
- `Black Cat`
- `Blade`
- `Blink (Released)`
- `Cameo compliment`
- `Doctor Druid (Released)`
- `Galactic Storm`
- `Hulk`
- ✅ `Intergalactic Hazards [2.5]`
- `Iron Man (Model 42)`
- `Lady Sif`
- `Muse`
- `NIGHT THRASHER (MC4 SEALED)`
- ✅ `Necroverse [1.5]`
- `Skrull Menace (Released)`
- `Spider-Man 2099`
- `Spider-Man Noir`
- `Spider-Woman (Released)`
- `Sunfire`
- `Superior Spider-Man`
- `Texas Twister (Released)`
- `Throg`
- `Viv Vision`
- `YONDU (MC4 SEALED)`
- `[1] Venomized`

⚠ `Galactic Storm` et `Skrull Menace (Released)` sont des DOUBLONS des
zips déjà présents dans `A créer/` : vérifier avant de porter.
