# PLAN — Ordre de création des héros/vilains fan-made du dossier « A créer »

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

## 6. Deuxième arrivage : 27 zips déposés à la racine le 02/09/2026

**Méthode :** contenu de chaque zip listé, puis carte d'identité (et les cartes
signalant une mécanique inhabituelle) lues à l'image. Aucune difficulté n'est
donnée sur la foi d'un nom de fichier.

### 6.1 Quatre zips à écarter tout de suite

| Zip | Raison |
|---|---|
| **Intergalactic Hazards [2.5]** | Déjà porté le 02/09 (`ih`, 6 cartes). |
| **Necroverse [1.5]** | Déjà porté le 02/09 (`nv`, 8 cartes). |
| **Galactic Storm** | Copie octet pour octet de `A créer/Galactic Storm` (21 fichiers, même arborescence). |
| **Skrull Menace (Released)** | Copie de `A créer/Skrull Menace (Released)` (39 fichiers, même arborescence). |

23 nouveaux items restent.

### 6.2 Groupe A — clonage direct, aucune primitive neuve (2/5)

| Item | Auteur | Cartes | Réutiliser | Capacité lue |
|---|---|---|---|---|
| **Throg** | Rainy | 23 | `alligator_loki` en entier | Réponse : rendre Frogjolnir à la main → prêter Throg. Frogjolnir (`al022`), Throg sbire-joueur (`al002`) et le nemesis Alligator Loki sont déjà codés. |
| **Viv Vision** | Rainy | 21 | `vision` officiel | Action : dépenser une ressource ⚡ → +2 à un pouvoir de base. Clone de Vision. |
| **Hulk** | Rainy | 19 | `core/hulk` officiel | Réponse : après que Hulk subit des dégâts, 1 dégât à un ennemi. Une ligne. |
| **Lady Sif** | Rainy | 23 | `red_guardian`, `angela` | Réponse : après un pouvoir de base, retirer 1 menace. |
| **Beta Ray Bill** | Rainy | 19 | `thor` officiel | Action : chercher Stormbreaker et l'ajouter à la main. Motif Mjolnir à l'identique. |
| **Iron Man (Model 42)** | Rainy | 18 | `core/iron_man`, `superior_iron_man` | Action : dépenser X ressources ⚡ imprimées → X compteurs `reactor`. ⚡ est la ressource ÉNERGIE officielle, pas un 5e type. |
| **Blade** | Rainy | 26 | compteurs (`speed`, `venompool`) | Réponse : après un pouvoir de base, retirer 1 compteur `blood` → prêter Blade. |
| **Sunfire** | Rainy | 29 | `beast` (pool hors-deck), `superior_iron_man` | Interruption : attacher une copie mise de côté de Burning (6 exemplaires) à l'ennemi attaqué ou défendu. |
| **Texas Twister** | Kajislav | 32 | `dazzler`, upgrades exclusives | Upgrades ROTATION mutuellement exclusives, défaussées à l'attaque de base. |
| **Armored Spidey** | Kajislav | 33 | `gorr` (Godbomb recto-verso), `wiccan` | Spider Armor : permanent recto-verso à compteurs `metal`, se retourne quand le dernier part. |
| **Ares** | Rainy | 23 | `doctor_doom` (exception de deck), `angela` (`an005`) | Alter-ego : jusqu'à 5 upgrades TACTIC hors aspect. Héros : chercher un sbire dans le deck rencontre et le mettre en jeu engagé. |
| **Spider-Man 2099** | Rainy | 23 | fouille de deck existante | Réponse : chercher un event dans le deck, le jouer, remettre les cartes défaussées au fond **dans l'ordre de défausse**. |

### 6.3 Groupe B — une brique neuve, isolée (3/5)

| Item | Auteur | Cartes | Ce qui est vraiment neuf |
|---|---|---|---|
| **Spider-Man Noir** | Rainy | 23 | Zone de cartes « glissées sous l'identité » (max 3), +X ATQ/CTR selon leur nombre, alimentée par les traîtrises résolues. |
| **Black Cat** | Rainy | 13 | Même zone, plus dur : Interruption qui, au moment où les icônes d'une carte rencontre sont comptées, **compte celles d'une carte glissée à la place**. |
| **Spider-Woman** | Kajislav | 36 | Annuler les icônes boost **une par une** en dépensant des compteurs `psionic web`, à la révélation de la carte boost. |
| **Yondu** | BlueHG + DesignHacker | 23 | La Yaka Arrow migre entre ennemis et l'identité, avec un effet à chaque attache et détache. Motifs `alligator_loki` (AttachHeroTo/DetachHero) et `patriot` (Commandeer). |
| **Superior Spider-Man** | Rainy | 26 | **Deux alter-ego au choix** (Peter Parker, Elliot Tolliver) pour un seul héros, et Contingency Plan : carte attachée face cachée, jouable comme si elle était en main. |
| **Night Thrasher** | DesignHacker | 26 | Mot-clé maison **agile X** (réduire de X les dégâts d'une attaque à carte boost). Fiche à créer avant la première ligne de code. |
| **Blink** | Kajislav | 30 | Portal : upgrade attachée à un ennemi ou une manigance qui **réduit de 2 le coût** d'un event ATTAQUE ou MENÉE visant cette cible. Réduction conditionnée à la cible choisie. |
| **Doctor Druid** | Kajislav | 23 | Action : jouer le premier event de la défausse **dont la capacité est de type Action ou Hero Action**. Le moteur doit introspecter le type de capacité de cartes en défausse. |
| **Muse** | Rainy | 7 | Set MODULAIRE (pas un héros). Interruption forcée : « quand un joueur joue une carte **à l'effigie de son identité** ». Aucune donnée du moteur ne dit quelles cartes représentent le héros : convention à trancher. |

### 6.4 Groupe C — chantier de moteur (4/5)

| Item | Auteur | Cartes | Le sous-système |
|---|---|---|---|
| **[1] Venomized** | ekAugust | 37 | **Un nouvel ASPECT** (noir), utilisable par tous les héros. Mot-clé maison **weakness** (cartes mélangées au deck, hors compte de taille, à effet négatif à la pioche) et règle de deckbuilding au **coût cumulé** : 1 à 20 → 1 carte weakness, 21 à 40 → 2. Recette connue via `determination`, mais le mot-clé et la règle sont neufs. |
| **Cameo compliment** | BlueRiver | 3 | 3 cartes seulement, mais chacune dit « cherche dans ta **collection** » au Setup : sélection sur tout le catalogue selon un critère (upgrade WEAPON spécifique à une identité absente de la partie), plus l'écran qui va avec. |

### 6.5 Ordre conseillé

Les 23 nouveaux items s'insèrent après ce qui reste du plan d'origine. L'ordre
suit la réutilisation, pas la difficulté brute : deux items qui partagent une
brique se suivent.

1. **Throg** (2/5). Le plus rentable du lot : le pack `alligator_loki` livré le
   01/09 contient déjà Frogjolnir, le sbire Throg et le nemesis Alligator Loki.
2. **Viv Vision, Hulk, Lady Sif, Beta Ray Bill** (2/5). Quatre clones de héros
   officiels, capacité d'identité en une ligne.
3. **Iron Man (Model 42), Blade, Sunfire** (2/5). Compteurs et cartes mises de
   côté : trois motifs déjà écrits trois fois.
4. **Texas Twister, Armored Spidey** (2/5). Upgrades exclusives et permanent
   recto-verso à compteurs.
5. **Ares, Spider-Man 2099** (2/5). Exception de deckbuilding façon `dd` et
   fouille de deck.
6. **Spider-Man Noir puis Black Cat** (3/5 puis 4/5). Noir construit la zone
   « glissée sous l'identité » dans sa version simple, Black Cat la reprend et
   n'a plus que la substitution d'icônes à écrire.
7. **Spider-Woman** (3/5). Même famille : intervenir pendant la résolution des
   icônes boost, juste après Black Cat.
8. **Yondu, Superior Spider-Man** (3/5). Attachement mobile et zone jouable
   hors main : deux motifs posés par `alligator_loki`, `patriot` et `beast`.
9. **Night Thrasher, Blink, Doctor Druid** (3/5). Trois briques indépendantes,
   une par pack, aucune dépendance entre elles.
10. **Muse** (3/5). 7 cartes, mais une question de données à trancher avec
    l'utilisateur avant d'écrire.
11. **[1] Venomized** (4/5). Le plus gros retour sur investissement du lot :
    un aspect entier disponible pour tous les héros du jeu.
12. **Iron Patriot** (4/5, reste du plan d'origine). Deck secondaire REGISTERED.
13. **Cameo compliment** (4/5). 3 cartes, mais un sélecteur sur tout le
    catalogue et un écran à faire.
14. **Doctor Doom Alt Arts** (2/5, valeur faible). 12 arts alternatifs de
    cartes officielles et 4 vraies cartes (Castle Doom, Kristoff, Prot-Doombot,
    Ingenuity). À faire quand on veut, ça ne débloque rien.
15. **Skrull Menace, Galactic Storm** (5/5). Bloqués, voir §7.

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
