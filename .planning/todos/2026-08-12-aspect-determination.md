# TODO / SPEC — L'aspect « Determination » (DesignHacker)

**Statut :** infrastructure moteur faite (`e161ffe`), préfixe `dt` déclaré, les
142 cartes inventoriées, et **les 16 premières sont DANS LE JEU depuis le
2026-08-13** : données, set, images, et génération éprouvée carte par carte. Les
4 événements du lot attendent leur module (voir §7). **Aucun module n'est
écrit** : c'est le gros du chantier, et il reste entier.
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
