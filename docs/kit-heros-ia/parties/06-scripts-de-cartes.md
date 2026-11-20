
---

## 6. Les scripts des cartes du héros (`src/cards/pack/<pack>/…`)

Un script est un fichier Python qui définit **`GetAbilities()`** et renvoie la liste des capacités de **une face de
carte**. Les règles générales (surface utilisable, types de capacité, fabriques, coûts, cibles, 67 exemples réels
classés par mécanique) sont dans l'**annexe A** (`annexes/A-kit-cartes.md`), les **recettes mécanique par
mécanique** dans l'**annexe B**, les **mots-clés** dans l'**annexe C**, et **l'index de tout ce que le moteur
sait faire** dans l'**annexe I**. Ce chapitre dit ce qui est **propre à un héros**.

### 6.1 Où ranger un script, et les `__init__.py`

Le moteur cherche le script d'une carte dans **`src/cards/pack/<pack>/<set_nettoyé>/<card_id>.py`**, puis, à
défaut, dans **`src/cards/pack/<pack>/<card_id>.py`** (racine du pack). `<set_nettoyé>` est le `set_name` de la
carte passé dans `CleanName` (minuscules, espaces → `_`, apostrophes et ponctuation retirées) :

{{BLOC:outils/verifier-livraison-campagne.py|def clean_name|def lire_json|python}}

| `set_name` de la carte | Dossier du script |
|---|---|
| `Lockjaw` | `src/cards/pack/lockjaw/lockjaw/` |
| `Lockjaw Nemesis` | `src/cards/pack/lockjaw/lockjaw_nemesis/` |
| `Iron Fist` | `src/cards/pack/iron_fist/iron_fist/` |
| `""` (carte d'aspect d'une boîte officielle) | la racine du pack : `src/cards/pack/ant/12011.py` |

⚠ **Un dossier de set sans `__init__.py` rend TOUTES ses cartes muettes, sans la moindre erreur.** Un script
rangé dans le mauvais dossier est muet aussi. `verifier-livraison-heros.py` les attrape tous les deux.

Les trois `__init__.py` d'un pack de héros réel (Lockjaw). Le premier est celui du pack, le deuxième celui du set
`lockjaw/`, le troisième celui du set `lockjaw_nemesis/` :

{{FICHIER:Fusion/marvel-lcg-src/src/cards/pack/lockjaw/__init__.py|python}}

{{FICHIER:Fusion/marvel-lcg-src/src/cards/pack/lockjaw/lockjaw_nemesis/__init__.py|python}}

{{FICHIER:Fusion/marvel-lcg-src/src/cards/pack/lockjaw/lockjaw/__init__.py|python}}

⚠ Le commentaire d'en-tête de ce dernier fichier est **historique** : il parle d'une « ressource os » rendue par
`[wild]`. C'est faux depuis le 9/8/2026 : l'icône imprimée est une ressource **mentale** (`B`), et c'est ce que
teste `PayeAvecMental`. Le code, lui, est exact. (Leçon de la règle 8 : une icône lue à vue.)

Chaque script commence par **`from . import *`**.

### 6.2 Une face d'identité = un script, avec **seulement les capacités imprimées**

* Les **statistiques** de base (ATK, THW, DEF, REC, taille de main) viennent de `desc` et sont **automatiques** :
  jamais dans un script.
* Chaque **face** (`a`, `b`, et les formes de plus) qui imprime une capacité a **son propre fichier**
  (`lj001a.py`, `lj001b.py`). Une face sans capacité imprimée n'a **pas** de script (Harry Osborn n'a pas de
  `ho001b.py`).
* Le **commentaire d'en-tête** de chaque script recopie le texte imprimé de la carte, cite les **cartes de
  référence** (celles dont tu as copié la fabrique) et liste les **mots-pièges** du texte (§6.8). Ce n'est pas
  décoratif : c'est ce que Claude relit pour décider si ton script est fidèle.

La face **héros** et la face **alter ego** d'un héros à capacité de fouille et de mise en jeu (Lockjaw) :

{{FICHIER:Fusion/marvel-lcg-src/src/cards/pack/lockjaw/lockjaw/lj001a.py|python}}

{{FICHIER:Fusion/marvel-lcg-src/src/cards/pack/lockjaw/lockjaw/lj001b.py|python}}

Les deux faces d'un héros officiel à **compteurs** (Iron Fist : le jeton Chi vit **sur l'identité**) :

{{FICHIER:Fusion/marvel-lcg-src/src/cards/pack/iron_fist/iron_fist/64001a.py|python}}

{{FICHIER:Fusion/marvel-lcg-src/src/cards/pack/iron_fist/iron_fist/64001b.py|python}}

### 6.3 Les accroches propres aux identités (recettes vérifiées)

| Texte imprimé sur l'identité | Fabrique | Carte modèle | À savoir |
|---|---|---|---|
| **Setup:** … | `AbilityFactory.WhenCardSetup("This", op)` — **deux arguments** | `lj001b`, `an001b`, `ok001b` | à un seul argument la capacité ne fait rien |
| After you change to this form | `AfterUnitChangeForm(type, "You", op, to_this_form=True)` | `01019a`, `12001a`, `bt001b` | |
| After you attack an enemy | `AfterUnitAttackEnd(type, "You", op, against_who=Enemy)` | `iw001a`, `ho001a` | le champ du message est `attacked_targets`, pas `attacked` |
| After you play a card | `AfterPlayerPlayedCard(Response, "You", None, op)` | `64001a`, `fne/60027` | « jouer » ≠ « mettre en jeu » |
| After the player phase ends | `AfterPhaseEnd(ForcedResponse, "Player", op)` | `64001a`, `aos/50029` | |
| Your <Trait> cards lose Temporary / gain X (continu) | `*GiveKeywordToInPlayWhenApplyThis(CardFinder(card_type=…, trait=…), control_by="You", …)` | `64001b`, `cyclops/33004` | un `CardFinder` à trait doit porter aussi `card_type` |
| Un compteur sur l'identité | `…CostFunc.Counter("YourIdentity", n, 'chi')` | `64006`, `64010`–`64012` | sans la condition « au moins n », la capacité est offerte impayable |
| Mettre une carte **de côté** à la mise en place | `AbilityFactory.BeginGameWithSetAside([ids], op)` sur la **face alter ego** | `bt001b`, `09001b`, `al001b`, `36001b` | voir §6.4 |

### 6.4 Les cartes « mises de côté » : `set_aside` n'est pas lu

Le champ `set_aside` du deck de départ **n'est pas lu par le moteur en vraie partie** (§2.2). Une carte qui doit
exister « à côté » (un pool de cartes Discovery, une forme de plus, un compagnon) se crée par
`AbilityFactory.BeginGameWithSetAside([...])` **dans le script de la face alter ego**, puis se relit par
`set_aside_deck.Get()`. Modèle commenté : `bt001b` (Beast). Le harnais de test, lui, fait exister cette carte avec
`Puzzle.CreatePlayerAdditionalDeck` : **un cas vert ne prouve pas** que la carte existe en vraie partie
(piège payé sur Alligator Loki).

### 6.5 Les cartes signature, l'obligation, les cartes némésis

* **Cartes signature** : l'étiquette `Hero Action` / `Hero Response` / `Hero Interrupt` n'autorise la carte que
  **sous la forme héros** ; une carte sans cette étiquette se joue sous les deux formes. Cherche la mécanique
  dans le catalogue de l'annexe A (§8), jamais dans ta mémoire de l'ancien jeu.
* **Obligation** : c'est une carte de rencontre « donnée » au joueur ; son script porte le texte imprimé
  (« You may flip to alter-ego form. Choose: … »).
* **Cartes némésis** : des cartes de rencontre ordinaires (sbire, complot annexe, attachement) rangées dans
  `<set> Nemesis` ; leurs mots-clés lus dans `desc` (`Surge`, `Boost`…) ne demandent **aucun** script.

Quatre scripts réels, de l'événement le plus simple à l'obligation à choix :

{{FICHIER:Fusion/marvel-lcg-src/src/cards/pack/lockjaw/lockjaw/lj008.py|python}}

{{FICHIER:Fusion/marvel-lcg-src/src/cards/pack/lockjaw/lockjaw/lj010.py|python}}

{{FICHIER:Fusion/marvel-lcg-src/src/cards/pack/lockjaw/lockjaw/lj013.py|python}}

{{FICHIER:Fusion/marvel-lcg-src/src/cards/pack/lockjaw/lockjaw_nemesis/lj015.py|python}}

### 6.6 Un héros complet commenté : les recettes payées par Iron Fist (MC64)

{{SECTION:docs/reference/RECETTES-MOTEUR.md|## 14. Iron Fist officiel|## 15.|2}}

### 6.7 Les déclencheurs côté joueur (recettes, §1 de l'annexe B)

{{SECTION:docs/reference/RECETTES-MOTEUR.md|## 1. Déclencheurs|## 2. Effets|2}}

### 6.8 Mots-pièges du texte imprimé, à chercher sur **chaque** carte

Avant d'écrire une ligne, relis le texte de la carte et cherche ces mots (étape 5 de `PROCESSUS-CARTE.md`) : ils
changent le sens. Le détail est au chapitre 12 (« Mots-pièges »). Les plus coûteux sur des cartes de héros :

* **« a »** (un) contre **« that »** (ce) : « remove 1 status from THAT enemy » (coût) contre « deal 2 damage to AN
  enemy » (effet) — deux cibles différentes ;
* **« play »** contre **« put into play »** ; **« after »** contre **« when »** ; **Response** contre **Interrupt** ;
* **« once per round »** (limite par round) contre **« once per phase »** ; **« Limit »** s'écrit `LimitOncePerRound()`
  sur la capacité (voir `lj001a`) ;
* **« each »** / **« all »** / **« any number »** ; **« up to »** ; **« may »** (facultatif) ;
* les **mots répétés** (« deal 1 damage ... deal 1 damage ») : une attaque PAR coup ;
* **« this card »** / **« here »** (= la carte qui porte le texte, souvent l'identité) ;
* **« your identity »** contre **« your hero »** (sous la forme alter ego, un « hero » n'existe pas).

### 6.9 Le gabarit de contrôle d'une carte (à remplir pour chaque carte à capacité)

Le fichier `GABARITS.md` de ta livraison contient **un gabarit par carte à capacité** : c'est la trace que tu as
fait les contrôles de `PROCESSUS-CARTE.md` à ta portée (étapes 1, 2, 3, 5, 6). Les étapes qui demandent **de
jouer** (7 : cas de test, 8 : autoplay) sont celles de Claude : tu y mets `à exécuter par Claude`, jamais « OK ».

{{SECTION:docs/reference/PROCESSUS-CARTE.md|## Gabarit à copier|## ZZZ_FIN|2}}

### 6.10 Auto-relecture d'un script

* [ ] `from . import *` en tête ; `GetAbilities()` défini ;
* [ ] le commentaire d'en-tête recopie le texte imprimé, cite 1 à 3 cartes de référence **qui existent** (le
  fichier existe dans le zip ou dans l'annexe A) et liste les mots-pièges rencontrés ;
* [ ] **chaque fonction appelée figure dans l'annexe I** (index de l'API) ou dans un modèle du zip ;
* [ ] `CardFinder(name="…")` **sans** l'étoile des cartes uniques ;
* [ ] aucune entrée-sortie (`open`, `os`, `subprocess`, `socket`, `exec`, `eval`), aucun `print` ;
* [ ] ce qui manque est un `# A_FAIRE_CLAUDE:` listé dans `A_FAIRE_CLAUDE.md` ;
* [ ] la face alter ego et la face héros ont chacune leur fichier si leur texte imprime une capacité.
