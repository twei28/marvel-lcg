# TODO / SPEC — L'aspect « Determination » (DesignHacker)

**Statut :** ✅ **LIVRÉ le 2026-08-13.** Les **142 cartes** sont dans le jeu avec
leurs données, leurs images, leurs modules et leur **texte français**. Le défaut
qui les rendait injouables (le moteur lit le `desc`, pas le texte) est corrigé et
verrouillé par deux outils. **Reste une seule chose : jouer une vraie partie avec
un deck Determination** — voir §13.
**Origine :** demande utilisateur (« créer un nouvel aspect qui vient d'ici
https://designhacker.ca/ »)
**Prérequis :** `2026-08-12-nommage-contenu-fanmade.md` (le préfixe `dh`)
**Source :** https://designhacker.ca/ — « This site compiles custom fan content
for the Marvel Champions: The Living Card Game ». Téléchargements par le Workshop
Steam (Tabletop Simulator) et par Google Drive.

---

## 1. Ce que c'est

Un **cinquième aspect** de construction de deck, à côté de Aggression, Justice,
Leadership et Protection. Relevé sur le site le 12/8/2026 :

| Type | Cartes (ordre de grandeur) |
|---|---|
| Alliés | ~45 |
| Événements | ~40 |
| Améliorations | ~40 |
| Supports | ~10 |
| Ressources | 4 |
| Complots personnels | 2 |
| **Total** | **~140** |

À recompter précisément au plan : le site annonce « plus de 100 cartes » et la
répartition ci-dessus est une lecture de ses sections, pas un inventaire.

## 2. Pourquoi ce n'est PAS un ajout de contenu ordinaire

**Les sept héros ajoutés jusqu'ici (Wonder Man, Hercules, Echo…) n'ont jamais
touché au moteur.** Un aspect, si. C'est ce qui distingue ce chantier de la
méthode rodée en 7 étapes de `~/marvel-work/TODO.md`.

**Les aspects sont une liste FERMÉE dans le moteur**, mesuré le 12/8 :

`src/game/card/face/base/card_player.py:18-37` déclare deux `Literal` :

```python
ASPECT_CLASS_TYPE = Literal['Aggression', 'Justice', 'Leadership', 'Protection', "'Pool"]
CARD_CLASS        = Literal["Aggression", "Justice", "Leadership", "Protection",
                            "'Pool", "Basic", "IdentitySpecific", "Encounter",
                            "Campaign", "Aspect"]
```

Trois choses à en tirer :

1. **Un cinquième aspect a DÉJÀ été ajouté** : `'Pool` (Deadpool). Le moteur sait
   donc en accueillir un de plus ; le chemin existe.
2. **`card_player.py` est un fichier refidélisé.** Le modifier est une divergence
   volontaire, à marquer comme les autres (`CORRECTIF` commenté, ligne dans
   `QUALITE-V2.csv`).
3. Une classe `"Aspect"` générique existe déjà (« Non-Hero Non-basic card »).
   **À mesurer avant de coder** : peut-elle porter Determination sans toucher aux
   `Literal` ? Si oui, le chantier moteur disparaît presque entièrement. C'est la
   première question du plan.

### Les autres endroits qui énumèrent les aspects

Chacun est un endroit où un cinquième aspect change un comportement de jeu, pas
seulement une déclaration :

| Fichier | Ce qu'il fait |
|---|---|
| `engine/lib/image_creator.py:136` | la couleur d'aspect. Determination en a besoin d'une |
| `cards/pack/fne/echo/__init__.py:2` | `ASPECT_OR_BASIC_CLASSES`, utilisé par Echo |
| `cards/pack/moon_knight/76006.py:12` | `ASPECTS`, une carte qui parcourt les quatre |
| `game/achievements.py:154` | les hauts faits par aspect |

**Une carte qui dit « choisissez un aspect » doit-elle proposer Determination ?**
C'est une question de RÈGLE, pas de code : le livret de DesignHacker doit
trancher, et à défaut c'est une décision à prendre et à écrire.

## 3. Le nommage

Préfixe **`dh`**, selon `2026-08-12-nommage-contenu-fanmade.md` : `dh001`…
Surtout pas un préfixe numérique — les 61 à 79 sont déjà pris et FFG arrive à 61.

## 4. Les chantiers

1. **Mesurer** si la classe `"Aspect"` existante suffit, ou s'il faut étendre les
   `Literal`. Décide de tout le reste.
2. **Le préfixe `dh`** et son registre (fiche nommage).
3. **Les données** : les ~140 entrées de `cards.json`, section `dh`, plus
   `sets_info.json`.
4. **Les images** : 140 scans à récupérer. ⚠️ Voir la dette mesurée le 12/8 —
   les scans récents pèsent 577 Ko en moyenne et l'archive livrable a triplé.
   **Redimensionner à l'import**, ne pas répéter l'erreur.
5. **Les modules** : ~140 fichiers `src/cards/pack/dh/**`. C'est le gros du travail.
   La méthode en 7 étapes de `~/marvel-work/TODO.md` s'applique.
6. **La construction de deck** : le wizard et le deck-builder doivent proposer
   Determination. `public/js/prepare/` et `public/deck-builder.html`.
7. **Les tests** : `test_cards`, `test_generate_cards` (obligatoire après tout
   ajout, il attrape ce que `test_cards` ne voit pas), et l'autoplay.

## 5. À trancher

- **Tout ou une part ?** 140 cartes, c'est plus que Hercules (40) et Wonder Man
  (25) réunis. Un premier jet « les 20 cartes qui font l'aspect » serait jouable
  bien plus tôt, et dirait si le moteur suit.
- **Que faire des cartes dont l'effet n'a pas de crochet moteur ?** L'audit du
  28/7 a montré qu'une part du contenu custom reste approximée. Les approximations
  doivent être **écrites**, jamais silencieuses.
- **Determination casse-t-il l'équilibre des hauts faits ?** `achievements.py`
  compte par aspect.

## 6. Comment on saura que c'est fait

Une partie menée avec un deck Determination, du wizard à la victoire, sans
`/debug`, et `test_generate_cards` vert sur les ~140 cartes.


---

## Ce que la mesure a établi (12/08/2026)

### 1. Le moteur : la question qui décidait de tout a une réponse simple

`CARD_CLASS_LIST` et `ASPECT_CLASS_LIST` sont **dérivées** des `Literal` de
`card_player.py`, par `Types.LiteralToList` (`game/element/utility.py:5-6`).
Les déclarer là suffit donc à la validation d'exécution (`assert IsCardClass`),
au typage et à la construction de deck. **Un seul point de modification**, pas
une liste éparpillée comme le craignait le §2.

Fait (`e161ffe`) : les deux `Literal` étendus, la couleur violette dans
`image_creator.py`, et `tools/test_aspect_determination.py` qui verrouille les
deux sens en 18 vérifications (Determination accepté, une classe inventée
toujours refusée). Sans régression : `test_cards` 4189/0, `test_generate_cards`
4764/0.

**La classe générique `"Aspect"` ne suffisait PAS** : elle est ajoutée
automatiquement aux classes d'aspect (`card_player.py:65-66`), mais l'assert
tombe avant sur le nom de l'aspect lui-même.

### 2. La source des cartes : le Drive, pas le site

- Le site n'a **ni API ni JSON** : un WordPress avec une page par carte.
- Le Drive partagé contient `DETERMINATION (3.0)/BLEED/`, soit les **images des
  cartes** en haute définition, nommées `D-1.jpg` à `D-141.jpg` (~1,5 Mo pièce).
- **Une image se lit et rend la carte entière.** Éprouvé sur `D-1.jpg` :

  > Cable (Nathaniel Summers) — coût 3, ALLY, ressource Mental, THW 2 / ATK 2 /
  > HP 4, traits X-FORCE. X-MEN. — *Reckless. Interrupt: When Cable attacks,
  > discard any number of cards from your hand...* — aspect DETERMINATION, D1

C'est donc la voie : lire les 141 images, pas gratter le site.

### 3. Le format d'une entrée de carte

Relevé sur `01002` (Black Cat) : `card_id`, `type`, `name`, `subtitle`,
`desc{Cost, HP, ATK, THW, RES, Class}`, `traits`, `set_name`, `text`.

**Le code des ressources** (`game/element/resources.py:12`) :
`R` = physical, `B` = mental, `Y` = energy, `G` = wild. Cable porte donc
`"RES": "B"`, et `"Class": "Determination"`.

### 4. Ce qui reste, et son ordre

1. **Extraire les 141 cartes** du Drive vers un JSON de travail. Mécanique,
   une lecture d'image par carte.
2. **Le préfixe `dt`** au registre `tools/prefixes_fanmade.json`, et
   `sets_info.json`.
3. **Les données** dans `cards.json`, section `dt`.
4. **Les images** : 141 fichiers, **à redimensionner à l'import** (1,5 Mo pièce
   ferait grossir l'archive livrable de 200 Mo à elle seule).
5. **Les modules Python** : c'est le gros du travail, et il faudra trancher les
   mots-clés custom. `Reckless` (« After this character enters play, place 1
   threat on each scheme ») n'existe pas dans le moteur : chaque mot-clé de
   l'aspect demande soit un helper partagé, soit une approximation **écrite**.
6. **Le deck-building** : le wizard et le deck-builder doivent proposer
   Determination. Non vérifié à ce jour.

### 5. Estimation honnête

Hercules (40 cartes) et Wonder Man (25) ont pris une session chacun, sans
mot-clé neuf. Determination, c'est ~140 cartes **et** des mots-clés à inventer :
plusieurs sessions, à découper par lots. Un premier lot « les 20 cartes qui font
l'aspect » dirait bien plus tôt si le moteur suit.


---

## Ce que le 13/08/2026 a établi

### 1. Le préfixe est `dt`, et il est au registre

La fiche se contredisait : `dh` au §3, `dt` au §4. **Tranché : `dt`**, parce que
la convention du registre est un préfixe par CONTENU et non par auteur (`cd` =
Cloak & Dagger, `mk` = Moon Knight, `bw` = Brawn). `dh` aurait désigné
DesignHacker, qui publiera peut-être autre chose. Déclaré dans
`tools/prefixes_fanmade.json` avec `cartes: 0`, avant la première carte, comme le
veut la règle du registre ; `verifier_prefixes.py` reste vert et le signale
seulement comme « déclaré mais inutilisé ». Le numéro de set 118 est réservé dans
le libellé, mais **`sets_info.json` n'est pas touché** : il porte un checksum, et
déclarer un set vide ne servirait à rien.

### 2. Le dossier contient 142 cartes, pas 141

`D-1.jpg` à `D-142.jpg`, **sans aucun trou**, plus un `~Multifaceted--Setup.jpg`
qui n'est pas une carte. La recherche Drive du MCP ne renvoie que 34 des 143
fichiers (elle n'indexe que ce qui a été ouvert) : l'énumération fiable passe par
`https://drive.google.com/embeddedfolderview?id=<dossier>#list`, qui rend la liste
complète en HTML, et le téléchargement par
`https://drive.google.com/uc?export=download&id=<fichier>` (le dossier est public).

### 3. Les 142 cartes sont relevées

`.planning/donnees/determination-cartes.json`. **Deux niveaux de lecture, et le
champ `_niveau` dit lequel** : les 20 premières sont lues en pleine page
(`releve`), les 122 autres sur des planches de six à 470 px (`inventaire`) — texte
net, mais non relu mot à mot, donc **à relire en pleine page avant d'écrire son
module**.

Répartition **mesurée** (la fiche l'estimait à ~140) :

| Type | Cartes |
|---|---|
| Alliés | 46 |
| Événements | 41 |
| Améliorations | 39 |
| Supports | 10 |
| Ressources | 4 |
| Manigances annexes de joueur | 2 |
| **Total** | **142** |

### 4. Trois conventions de lecture, calées sur des cartes officielles

* une étoile SOUS une valeur THW/ATK = dégât conséquent, écrite en suffixe `*`
  (Black Cat `01002` → `"THW": "1*"`) ; deux étoiles → `**` (Lockjaw `05018`) ;
* une étoile EN EXPOSANT à côté de la valeur relie la statistique au texte. Elle
  ne s'écrit PAS dans `desc` : c'est la capacité qui la produit ;
* l'icône de ressource se lit à la couleur : rouge/poing = `R`, bleu/molécule =
  `B`, doré/éclair = `Y`, vert/étoile = `G`. Vérifié sur quatre cartes officielles
  au `RES` connu.

**CORRECTION : Cable est une ressource ÉNERGIE (`Y`), pas mentale (`B`)** comme
l'écrivait le §3 des mesures du 12/08. L'erreur venait d'une lecture sans point de
comparaison.

### 5. Ce que le moteur ne sait pas encore faire, mesuré et non deviné

**Neuf compteurs manquent à `CardFace.COUNTER`** (`src/game/card/face/card_face.py:117`) :
`tactic`, `adrenaline`, `diversion`, `stimulant`, `spider`, `replay`, `ball`,
`LMD`, `configuration`. Cinq compteurs de packs fan-made y sont déjà, commentés
`CORRECTIF` : le chemin est balisé. Sans eux, `test_generate_cards` tombe à la
construction — c'est le piège connu de la méthode.

**Mots-clés sans crochet moteur connu** : `Reckless` (4 cartes), `Alias` (4),
`Alliance` (2), `Fragile` (une quinzaine), `all-purpose counter` (3). Aucun n'a
encore été cherché dans le moteur : c'est la première mesure du prochain lot.

**Cartes hors norme à traiter à part** : 2 manigances annexes de joueur
(`dt096`, `dt102`), un coût variable `X` (`dt083`), deux coûts à étoile (`dt136`,
`dt139`), quatre cartes **sans aucune icône de ressource imprimée** (`dt075`,
`dt140`, `dt141`, `dt142` — constat vérifié au zoom, pas un défaut de lecture), et
trois homonymes de cartes déjà présentes (Moon Knight, Deadpool, The Thing).

### 6. Ce qui reste, dans l'ordre

1. **Relire en pleine page** le lot que l'on s'apprête à coder (`_niveau:
   inventaire` → `releve`).
2. **Les 9 compteurs** dans `card_face.py`, commentés `CORRECTIF`.
3. **Mesurer les mots-clés** : `Reckless`, `Alias`, `Alliance`, `Fragile`.
4. **Les entrées `cards.json`** et le set dans `sets_info.json` (avec recalcul des
   deux checksums).
5. **Les images** : 142 fichiers de ~1,5 Mo. **Redimensionner à l'import** — les
   scans officiels du jeu font 300×434 pour 29 Ko.
6. **Les modules**, lot par lot, puis `test_cards`, `test_generate_cards`, autoplay.


## 7. Le premier lot est entré dans le jeu (13/08/2026)

**16 cartes sur 20**, et la raison des 4 manquantes vaut d'être retenue.

### Ce qui est fait

* `data/cards.json` : un pack `determination` de 16 entrées (`dt001` à `dt020`,
  moins les événements) ;
* `data/sets_info.json` : `118. Custom (Determination)`, sans héros ni scénario —
  un aspect n'en apporte pas — et les **deux checksums recalculés** avec la
  fonction du moteur (`Types.DictChecksum`), après avoir vérifié qu'elle
  reproduisait les checksums existants ;
* **les images** : `tools/make_determination_pics.py`. Il télécharge le bleed du
  Drive, **rogne les 3 mm de fond perdu** (1638×2229 = 69,5×94 mm quand une carte
  finie fait 63,5×88), ramène à 600×840 et dépose dans les deux installations.
  129 Ko de moyenne au lieu de 1,5 Mo : la dette mesurée le 12/08 ne se répète
  pas. Éprouvé en régénérant `dt007` à l'octet près.

### Vérifié, pas supposé

* `test_generate_cards` sur le préfixe `dt` : **16 générées, 0 échec** ;
* sur tout le jeu : 4779 générées, 1 échec — `example_event`, la carte d'exemple
  de `data/cards_custom.json`, qui échoue pour la même raison qu'au §7.1 et
  n'a jamais eu de module. Préexistant, sans rapport ;
* `verifier_prefixes.py` vert, et `dt` n'est plus « déclaré mais inutilisé » ;
* dans un vrai navigateur : le set est proposable dans la galerie, ses 16 cartes
  s'affichent, les 16 images se chargent en 600×840, aucune erreur JS.

### 7.1 La règle apprise : un Event ne va jamais sans son module

`dt005`, `dt006`, `dt012`, `dt017` — les quatre événements du lot — ont d'abord
été mis dans les données, et **les quatre ont échoué à la génération** :

    factory.py:120  assert False, f"{face.paper.card_id=}"

Une carte `Ally`, `Support`, `Upgrade` ou `Resource` vit sans module : elle se
construit, s'affiche, se choisit. Un `Event`, non : `factory.py` exige qu'il porte
**exactement une capacité `Play`**, et celle-ci ne peut venir que de son module.
Le commentaire d'un correctif voisin le dit sans ambiguïté : sans cela, « la
création de partie du héros PLANTE ».

Ils sont donc **sortis des données** plutôt que laissés en bombe à retardement.
Ils rentreront avec leur module. **Pour tous les lots suivants : les données et
le module d'un événement se livrent ensemble.**

### 7.2 Ce que le prochain lot doit faire

1. Écrire les modules des 4 événements sortis, et les remettre dans les données.
2. Les 9 compteurs dans `CardFace.COUNTER`, avant toute carte qui en porte
   (`dt008` Merc Squad en a besoin dès ce lot : son `Uses (3 tactic counters)`
   n'a aucun effet tant que `tactic` n'existe pas).
3. Les modules des 16 cartes deja en place : elles sont dans le jeu, mais leurs
   capacités ne font encore rien.


## 8. Les modules commencent (13/08/2026)

**Deux écrits, 18 à écrire, plus les 4 événements** (`b2e0172`). `dt003` (Venom)
et `dt016` (Deadpool), choisis pour leur banalité : ce qui compte est la méthode.

**La méthode, en trois gestes** :

1. **Trouver la carte officielle qui porte le même texte** et copier sa structure.
   `dt016` est le jumeau de `10012` (Sentry) au mot près. Rien ne s'invente tant
   qu'un précédent existe.
2. **Écrire le module** dans `src/cards/pack/determination/<card_id>.py`. Le pack
   a son `__init__.py` (`from cards.pack import *`), et le moteur retombe sur
   `cards.pack.<pack>.<card_id>` faute de sous-dossier de set.
3. **Prouver qu'il est branché** avec `tools/sonde_capacites.py`, **toujours avec
   un témoin** : une carte officielle à module, et une carte du même type sans
   module. Allié sans module 7 capacités, avec module 8.

**Le piège que le témoin a attrapé** : la première sonde lisait `card.faces`, qui
n'existe pas (c'est `card.printed_faces`), et rendait 0 pour TOUTES les cartes.
Sans témoin officiel dans la même mesure, la conclusion aurait été « mes modules
ne sont pas branchés », et j'aurais cherché des heures du mauvais côté.

**Ce qui reste hors de portée de la sonde** : qu'une capacité fasse la bonne
chose. Hors de la file du moteur aucune réaction en chaîne ne part. Il faudra une
vraie partie, comme pour la campagne.


## 9. Le premier lot FONCTIONNE (13/08/2026, soir)

**Les 20 premières cartes ont leur module.** Les 16 qui dormaient dans le jeu, et
les 4 événements qui en étaient sortis faute de module — ils sont rentrés avec le
leur, comme le §7.1 l'exigeait.

`test_generate_cards` préfixe `dt` : **20 générées, 0 échec**. `test_cards` :
**4209 ok, 0 erreur**. `verifier_prefixes.py` vert.

### 9.1 Les compteurs sont posés, et ils étaient DIX

Neuf étaient relevés le 13/08 ; la relecture des 142 textes en a sorti un dixième,
`deploy` (dt117, The Behemoth). Les dix sont dans `CardFace.COUNTER`, commentés
`CORRECTIF` comme les cinq compteurs fan-made qui y étaient déjà : `tactic`,
`adrenaline`, `diversion`, `stimulant`, `spider`, `replay`, `ball`, `LMD`,
`configuration`, `deploy`.

**`all-purpose counter` n'en fait pas partie** : `counter` existe déjà dans le
Literal et c'est très probablement lui que les trois cartes concernées (dt118,
dt119, dt120) utiliseront. À trancher quand leur lot arrivera.

### 9.2 La sonde sait maintenant répondre là où le comptage est muet

Trois murs, et ce qui les a fait tomber :

1. **Aucun support du jeu n'est sans module.** Le témoin négatif n'existait pas :
   il a fallu le **fabriquer par substitution** (module déplacé, reconstruit,
   resondé). Support sans module 3, avec module 4.
2. **Une ressource ne change pas de compte** : `DoubleResourcesThisGenerates`
   REMPLACE la capacité du moteur au lieu d'en ajouter une. dt007 : 2 avant, 2
   après.
3. **`tools/sonde_capacites.py --detail`** nomme désormais l'origine de chaque
   capacité, en descendant dans la fermeture quand une fabrique du moteur enveloppe
   l'opération voulue. Pour 19 des 20 cartes elle dit directement
   `dt005 : GetAbilities > blast_radius` : plus besoin de témoin. Pour dt007 elle
   sépare `DoubleResourcesThisGenerates > the_power_of_leadership` de
   `CheckThisCanPayCost > action`.

⚠️ **La sonde lit `.game`.** Sans `launcher_fast.py --build-only` avant, elle décrit
l'état précédent — piège payé une fois sur dt007.

### 9.3 Les écarts, écrits dans les modules

| Carte | Ce que dit la carte | Ce que fait le module | Pourquoi |
|---|---|---|---|
| dt013 Recon | « 3 facedown encounter cards » | les 3 du dessus de la pile | seul ensemble de cartes face cachée que le moteur sait montrer |
| dt018, dt019 | « maximum hit points » | `max_health` | le crochet officiel ne lit que l'imprimé |
| dt014 | « attaque avec overkill » | l'identité parmi les cibles touchées | le moteur ne publie pas le drapeau, il publie son effet |
| dt001 | `Reckless` | 4 lignes explicites | mot-clé sans crochet ; à reprendre pour les 3 autres cartes Reckless |

**Une approximation redoutée s'est révélée inutile** : `choose_x_different_options`
dit exactement « 2 des 3 lignes » pour le joker de Moon Knight.

### 9.4 Le prochain lot

1. **Relire en pleine page** les cartes du lot visé (`_niveau: inventaire` →
   `releve`) : c'est la première étape, et elle n'est pas facultative.
2. Écrire les modules par petits paquets, chacun copié sur la carte officielle qui
   porte le même texte, chacun prouvé à la sonde APRÈS un build.
3. Les événements ne rentrent dans `cards.json` qu'avec leur module.
4. `make_determination_pics.py <ids>` pour les images, `test_generate_cards` après.

**Ce que rien de tout cela ne prouve encore** : qu'une capacité fasse la bonne
chose en partie. Le §6 (« une partie menée avec un deck Determination, du wizard à
la victoire ») reste entier, et c'est le seul juge qui manque.


## 10. Le deuxième lot : dt021 à dt040 (13/08/2026, soir)

**40 cartes sur 142 fonctionnent.** Le lot compte **onze événements**, entrés
avec leur module comme l'exige le §7.1.

`test_generate_cards` préfixe `dt` : **40 générées, 0 échec**. `test_cards` :
**4229 ok, 0 erreur**. Dans un vrai navigateur : 40 cartes proposées à l'éditeur
de deck, images servies, aucune erreur JS.

### 10.1 La relecture en pleine page a confirmé le relevé

Les 20 cartes ont été relues une par une avant d'écrire une ligne. **Le relevé
fait sur planches de six était fidèle sur les vingt** : seuls trois textes
étaient abrégés (le rappel entre parenthèses de `Fragile`). C'est une bonne
nouvelle pour les 102 cartes restantes, mais la relecture reste obligatoire :
c'est elle qui a donné la définition exacte de `Fragile`, sans laquelle le
mot-clé serait resté « sans crochet connu ».

### 10.2 Les mots-clés vivent dans `__init__.py`

Une définition, partagée par toutes les cartes qui la portent :

| Helper | Ce qu'il fait | D'où il vient |
|---|---|---|
| `Fragile()` | les attaques contre cette carte gagnent overkill | **crochet officiel** : 33032 Marked |
| `Reckless()` | 1 menace sur chaque manigance à l'entrée en jeu | pas de crochet, joué tel qu'écrit |
| `PeutRevenirEnMain()` | « première carte jouée ce round » → retour en main | 18012 Clobber |
| `RepartirLeRetraitDeMenace()` | « remove X threat divided as you choose » | 03011 Falcon |

**`Fragile` avait un crochet officiel**, contre l'attente de la fiche du 13/08.
Il ne restait donc, des cinq mots-clés sans crochet, que `Alias` et `Alliance` à
mesurer — plus deux réponses trouvées en chemin (§10.3).

### 10.3 Deux crochets qui existaient déjà, et que le relevé croyait manquants

* **`all-purpose counter`** : `GetCounters('all-purpose')` rend le total de tous
  les compteurs d'une carte. Le moteur le connaît. dt118, dt119 et dt120
  n'auront pas besoin d'un compteur neuf.
* **`IsFirstCardPlayedThisRound()`** existe (18012, Clobber), et son usage
  officiel apprend que le moteur enregistre la carte jouée **après** sa
  résolution — sinon Clobber ne reviendrait jamais en main.

### 10.4 Un outil de plus, né d'un vrai défaut

`tools/verifier_noms_modules.py` comble le trou entre `test_cards` et la partie
réelle : `test_cards` n'exécute pas le CORPS des fonctions d'un module, donc un
nom absent y dort jusqu'à ce que la carte soit jouée. Il a trouvé son premier
défaut en naissant (`SetTarget(Character)` dans dt031, alors que le moteur attend
la chaîne). Passé sur **les 85 packs du jeu : zéro signalement**.

### 10.5 Ce qui reste

1. **102 cartes** (dt041 à dt142), même méthode, par lots de 20.
2. Mesurer `Alias` et `Alliance` quand leur lot arrivera.
3. Les cartes hors norme du §5 des mesures : les 2 manigances annexes de joueur,
   le coût variable `X` (dt083), les deux coûts à étoile, les quatre cartes sans
   icône de ressource imprimée.
4. **Le juge qui manque toujours** : une partie menée avec un deck Determination.


## 11. Où en est le chantier (13/08/2026, fin de soirée)

**100 cartes sur 142 fonctionnent.** Cinq lots livrés, chacun vérifié et commité :
dt001-dt020, dt021-dt040, dt041-dt060, dt061-dt080, dt081-dt100.

`test_generate_cards` préfixe `dt` : **100 générées, 0 échec**. `test_cards` :
**4289 ok, 0 erreur**. Dans un vrai navigateur, les cartes sont proposées à
l'éditeur de deck et leurs images se chargent.

### 11.1 Les cinq mots-clés de l'aspect sont TOUS traités

| Mot-clé | Verdict | Où |
|---|---|---|
| `Fragile` | **crochet officiel** (33032, Marked) | `__init__.py` |
| `all-purpose counter` | **crochet officiel** (`GetCounters('all-purpose')`) | — |
| `Reckless` | pas de crochet, joué tel qu'écrit | `__init__.py` |
| `Alias` | pas de crochet, approximation écrite | dt100 |
| `Alliance` | ne fait rien par lui-même, rien à écrire | dt061 |

Deux des cinq avaient donc déjà leur crochet dans le moteur, contre l'attente du
relevé du 13/08.

### 11.2 Ce qui reste : dt101 à dt142 (42 cartes)

* **dt101 à dt106 sont relues en pleine page** ; les 36 autres restent au niveau
  `inventaire` et doivent être relues avant qu'on écrive leur module.
* La relecture a déjà corrigé un défaut : **dt102 porte une menace de départ de
  1 PAR JOUEUR**, ce que la planche de six ne montrait pas.
* Répartition du reste : 16 alliés, 11 améliorations, 9 événements, 4 supports,
  1 manigance annexe de joueur, 1 ressource.
* Points connus dans ce tronçon : le compteur `configuration` de Darkhawk
  (dt101), plusieurs cartes `Alias` (dt105, dt106), et les trois dernières
  cartes sans icône de ressource imprimée (dt140, dt141, dt142).

### 11.3 Ce que ce tronçon a appris, et qui vaut pour la suite

**Une manigance annexe de joueur se déclare `PlayerSideScheme`**, et son `desc`
a besoin de `StartingThreat` et `Victory` — sans quoi la génération tombe sur
`KeyError('Cost')`. Le relevé disait `SideScheme` pour dt096 et dt102 : les deux
sont corrigées.

**Un Event ou un Upgrade n'accepte qu'UNE capacité Play.** dt087 en avait deux
et la génération l'a refusée. C'est la troisième fois que `test_generate_cards`
attrape ce que `test_cards` laisse passer.


## 12. L'ASPECT EST COMPLET (13/08/2026, nuit)

**Les 142 cartes sont dans le jeu**, relues en pleine page, avec leur module,
leurs données et leur image.

* `test_generate_cards` préfixe `dt` : **142 générées, 0 échec**
* `test_cards` : **4331 ok, 0 erreur**
* `verifier_noms_modules` : propre ; `verifier_prefixes` : vert
* dans un vrai navigateur : **142 cartes proposées** à l'éditeur de deck, images
  servies, aucune erreur JS

### 12.1 Les mots-clés de l'aspect, tous traités

Quatre helpers partagés dans `src/cards/pack/determination/__init__.py` :
`Fragile()`, `Reckless()`, `AliasReduitLeCout()`, plus `PeutRevenirEnMain()` et
`RepartirLeRetraitDeMenace()` et `Drain()` pour les textes qui reviennent.

⚠️ **CETTE FICHE A AFFIRMÉ ICI QUE LE MOTEUR LISAIT LE TEXTE. C'ÉTAIT FAUX**, et
c'est ce qui a rendu 49 cartes injouables — voir §13.

### 12.2 Les écarts, tous écrits dans leur module

| Carte | Ce que le moteur ne sait pas faire |
|---|---|
| dt013 Recon | pas d'ensemble « cartes rencontre face cachée » consultable |
| dt030 | « 2 dégâts de plus » passe par l'ATK de l'attaque |
| dt072 Red Dagger | une attaque en cours ne se rejoue pas X fois |
| dt074 In the Wings | le défenseur se déclare dans sa propre fenêtre |
| dt075, dt117 | « votre collection » n'existe pas → deck et défausse |
| dt100/105/106/107 | `Alias` : la défausse simultanée ne s'exige pas |
| dt101 Darkhawk | un compteur posé SUR une statistique n'existe pas |
| dt109 Phase Shift | un mot-clé ne se donne qu'à une carte EN JEU |
| dt111 Morph | aucune fenêtre « boîte de texte traitée comme vide » |
| dt125 Night Thrasher | seul un retournement VERS une face nommée est publié |
| dt135 Tarantula | « une icône PAR JETON » : ligne **non implémentée**, dite |
| dt056 Oblivion | le joueur d'origine n'est pas retenu après le mélange |

**Une seule ligne de tout l'aspect n'est pas implémentée** (l'icône par jeton de
Tarantula), et son module le dit. Tout le reste est joué ou approximé par écrit.

### 12.3 Ce qui reste, et c'est le seul juge qui manque

**Une partie menée avec un deck Determination, du wizard à la victoire.** Ni la
sonde, ni `test_generate_cards`, ni `verifier_noms_modules` ne disent qu'une
capacité fait la bonne chose : ils disent qu'elle est là, qu'elle se construit,
et que ses noms existent. Le §6 de cette fiche reste donc ouvert — et c'est
maintenant la seule chose qui l'est.



## 13. Le défaut qui rendait 49 cartes injouables (13/08/2026, corrigé)

**Signalé en jouant : « Merc Squad ne fonctionne pas, je peux pas cliquer
dessus. »** Sa capacité coûtait « retirer 1 pion tactique » et la carte entrait
en jeu **sans un seul pion** : action grisée pour toujours.

**La cause était de classe.** Cette fiche avait conclu (§12.1) que le moteur
lisait les mots-clés dans le TEXTE, parce que Luke Cage porte « Toughness » sans
module. **Il les lit dans le `desc`** (`RegisterAttribute`, has_uses.py) ; le
texte n'est que de l'affichage. **49 cartes sur 142**, 54 champs manquants :
`Uses`, `Toughness`, `Restricted`, `Retaliate`, `MaxPerDeck`, `MaxPerUnit`,
`Setup`, `Victory`, `Alliance`, `Villainous`, `Requirement`.

**Un attribut n'existe que pour certains TYPES** : `Uses` sur
Upgrade/Support/Attachment/Obligation/Environment, `Villainous` sur Minion,
`Restricted` sur Upgrade. Le déclarer ailleurs **empêche la carte de se générer**
(KeyError). Spiders-Man pose donc ses pions depuis son module.

### 13.1 Pourquoi aucun outil ne l'a vu, et les deux qui manquaient

Les quatre outils du chantier demandaient **« la capacité existe-t-elle ? »**.
Aucun ne demandait **« le joueur peut-il s'en servir ? »**. Deux outils neufs,
chacun mis en défaut exprès avant d'être cru :

* **`tools/verifier_desc_mots_cles.py`** — compare le texte au `desc`. Il aurait
  attrapé les 49 d'un coup.
* **`tools/verifier_cartes_en_jeu.py`** — génère chaque carte dans une vraie
  partie et compare le texte à ce que la carte PORTE.

⚠️ Les deux trouvent **26 écarts du même genre ailleurs dans le jeu** (fne,
madame_web, cw, mk, sr… et un dans le contenu OFFICIEL : 01055 dit « Max 2 per
deck » sans le champ, donc la carte retombe sur 3). **Préexistants, non touchés.**

## 14. Le français (13/08/2026)

Les **142 textes et noms** sont traduits, avec la terminologie du jeu
(`translate_fr.json` : Déferlement, Perçant, À Distance ; et manigance, sbire,
méchant, contrer, incliner, redresser du dico du plateau).

**Pas dans `data/cards.json`, volontairement** : `dt133.py` compte les
personnages dont le texte porte « Fragile. » et `scheme_main.py` reconnaît une
manigance perdante à sa phrase anglaise. Le français vit dans
`public/js/prepare/cartes-fr.js`, la source dans
`.planning/donnees/determination-fr.json`.

## 15. CE QUI RESTE, ET C'EST TOUT

1. **Jouer une vraie partie avec un deck Determination**, du wizard à la
   victoire. Aucun outil ne dit qu'une capacité fait la BONNE chose.
2. **Les 12 écarts du §12.2** sont assumés et écrits ; à revoir seulement si le
   jeu en pâtit.
3. **Les 26 écarts `desc` ailleurs dans le jeu** (§13.1), à traiter comme un
   chantier à part si on veut les corriger.



## 16. Les écarts repris : 8 sur 12 levés (13/08/2026)

Ils avaient été assumés faute d'avoir cherché assez loin. **Le moteur savait
faire, dans huit cas sur douze.**

| Carte | Ce qui a été trouvé |
|---|---|
| dt013 Recon | `player.dealt_encounter_cards` tient les cartes face cachée |
| dt074 In the Wings | `DeclareDefender` sur le message d'attaque |
| dt125 Night Thrasher | `WhenCardFlip`, la fenêtre générique de retournement |
| dt072 Red Dagger | `AddTarget` résout l'attaque X fois pour de vrai (25013) |
| dt030 Adrenaline Shot | `IncreaseDamage` : ce sont les dégâts, pas l'ATK |
| dt056 Oblivion | le joueur d'origine est retenu sur la carte |
| dt101 Darkhawk | deux gains, chacun conditionné par le pouvoir courant |
| dt100/105/106/107 `Alias` | l'homonyme est défaussé à l'entrée en jeu |

### 16.1 Les quatre qui restent, et pourquoi

**Aucun n'a de porte dans le moteur — vérifié, pas supposé :**

* **dt075 / dt117 « votre collection »** — aucune notion de collection dans
  `operate/search.py`. La recherche se fait dans le deck et la défausse.
* **dt109 Phase Shift** — un mot-clé ne se donne qu'à une carte EN JEU ; la
  carte parle du deck et de la main.
* **dt111 Morph** — `OnEvent.CardKeyword` ne surveille que ATK/THW/SCH : aucune
  fenêtre « boîte de texte traitée comme vide ».
* **dt135 Tarantula** — `have_res_icon` n'existe que pour une carte qui accorde
  une icône à UNE AUTRE, et rien ne la donne PAR JETON. **Seule ligne non
  implémentée de tout l'aspect**, et son module le dit.

Les quatre demanderaient une modification du MOTEUR, pas d'une carte. C'est un
chantier différent, et il n'est pas ouvert.

### 16.2 Ce qui reste, toujours le même

**Jouer une vraie partie avec un deck Determination.** Les outils disent
maintenant que chaque carte est là, se construit, porte ce qu'elle annonce et
que ses noms existent. Aucun ne dit qu'elle fait la bonne chose.
