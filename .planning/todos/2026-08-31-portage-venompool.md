# Portage du pack VENOMPOOL — journal de validation

Set 129, préfixe `vp`, 17 `card_id`. Auteur **CptScorp**, *Marvel Champions
Custom Project*, Cycle 2. Zip source : `A créer/Venompool (Council
Released)-20260813T091211Z-1-001.zip`.

Ce document tient le gabarit `PROCESSUS-CARTE.md` pour chaque carte du pack,
comme l'exige la « Gate finale » de `PROCESSUS-HEROS.md`.

---

## 0. Ce que le pack apporte au projet, au-delà du héros

### `drain X` a enfin une définition imprimée

L'insert du pack (« Venompool Insert.png ») définit le mot-clé maison resté
sans définition depuis `agent_anti_venom` :

> « When an ability instructs you to drain X from an enemy, deal X damage to
> that enemy, then heal X damage from your identity. »

C'est **mot pour mot** la lecture arbitrée à l'aveugle avec l'utilisateur le
4/8/2026. `docs/reference/mots-cles/drain-x.md` est mis à jour : la
convention n'est plus une supposition, et la question systématique qu'exigeait
la fiche avant tout nouvel appel à `Drain()` n'a plus lieu d'être.

### L'icône du side scheme, identifiée par comparaison d'image

`vp012` Shocking Entrance porte une icône « + sur une forme ». Plutôt que de
la nommer à vue (leçon Lockjaw, `PROCESSUS-CARTE.md` étape 3), elle a été
découpée du scan puis superposée aux icônes officielles :

| Carte | Icône | Forme |
|---|---|---|
| 01107 Breakin' & Takin' | **hazard** | « + » sur une **carte inclinée** |
| 01109 Bomb Scare | acceleration | « + » sur une **maison soulignée** |
| **vp012 Shocking Entrance** | **hazard** ✔ | « + » sur une carte inclinée |

`desc.Hazard = "1"`, pas `Acceleration`.

### Quatre homonymes préexistants

| Nom | Carte déjà présente | Conséquence |
|---|---|---|
| **Wade Wilson** | `44001b`, alter-ego officiel de Deadpool | `desc.GiveTo` de `vp011` se résout **par nom** (`Worlds.FindPlayerByName`). L'insert du pack interdit lui-même de jouer Deadpool et Venompool ensemble. |
| **Venompool** | `dt105`, allié de l'aspect fan-made Determination | Un allié à son propre nom est **exclu** du deck. Les modules ne résolvent jamais « Venompool » par son nom, toujours par le joueur (`GetVenompool`). |
| **Black Cat** | `01002` (allié signature de Spider-Man), `wd045` (sbire Electro) | Classe `Hero` : jamais mélangeable. |
| **Thwip!** / **Foresight** | `sr003` (Spider-Man Rainy), `mw009` (Madame Web) | Événements signature d'autres héros, classe `Hero`. |

Tout est consigné dans `metadata.collision_note` de `deck/starter/venompool.json`.

---

## 1. Étapes de `PROCESSUS-HEROS.md`

| Étape | État | Preuve |
|---|---|---|
| 1. Cartes dans `data/cards.json` | ✅ | 17 `card_id`, diff de **305 lignes ajoutées / 0 supprimée** |
| 2. Scripts | ✅ | 17 modules, `test_cards` 4895 → **4912 ok / 0 err** |
| 3. Deck de départ | ✅ | `deck/starter/venompool.json`, 15 signature + 25 aspect/basiques |
| 4. `data/nemesis/…` | ⬜ | facultatif (UI), non fourni |
| 5. `data/sets_info.json` | ✅ | set « 129. Custom (Venompool) » |
| 6. Images | ✅ | 17 `.jpg` en 975 px extraits des scans du zip |
| 7. Biographie | ✅ | `vp001a` dans `heros-info.js`, `node --check` propre |
| 8. Textes français | ✅ | 17 entrées, `tsc --noEmit` propre |
| 9. Validation carte par carte | 🟡 | 7 cas verts + 3 substitutions, §3 et §4 |
| 10. Points transverses | ✅ | 0 carte signature étrangère dans un `player_deck` |

**Aspect** : contrairement à `ms_america` et `patriot`, l'auteur fournit sa
decklist complète (planche « Venompool Starter Deck ») — aspect **Protection**,
aucun choix à faire.

---

## 2. Arbitrages posés à l'utilisateur

| Carte | Question | Réponse (31/08/2026) |
|---|---|---|
| `vp016` Psyche Warp | « the ally with the highest printed ATK » : quels alliés ? | **Tes alliés seulement.** En multi, la carte ne peut pas défausser l'allié d'un coéquipier. |

Points **non** soumis à question, et pourquoi :

- **`vp007` « attacks » vs `vp010` « makes a basic attack »** : le contraste est
  imprimé dans le même pack, il est donc voulu. `is_basic_attack=None` sur
  l'un, `True` sur l'autre.
- **`vp001a` « Limit 1 [per_hero] per phase »** : sur une carte d'identité,
  l'icône joueur ne peut désigner que le porteur — personne d'autre ne
  déclenche la Response d'une identité qui n'est pas la sienne.
- **`vp006` « Each enemy may only be targeted once »** : rendu par l'absence de
  `repeat_rules`, là où `vp003` (« divided as you choose ») en a besoin. Choix
  technique, pas arbitrage de règles.
- **`vp011` « You MUST flip »** : `48026` et `16053`, les deux obligations
  modèles, disent « you MAY flip ». Le changement de forme est ici **forcé**,
  le helper `YouMayFlipToYourAlterEgoForm` n'est donc pas utilisé.

---

## 3. Les trois bugs trouvés par les cas de comportement

Aucun n'était visible pour `test_cards`, qui rendait **4912 ok / 0 err** avec
les trois en place. C'est exactement ce que `PROCESSUS-CARTE.md` annonce :
construire une capacité ne prouve pas qu'elle s'exécute.

### a. `vp003` — l'assertion qui empêchait la partie de monter

`AssertionError: face.paper.card_id='vp003'`, levée au **setup**. Le moteur
exige qu'un événement n'ait qu'**une** capacité `Play` ; celui-ci en a deux,
parce que sa portée change (« 4 damage divided among enemies, 6 instead if
True Form is in play ») et que `range` est figé à la construction.

Correctif : déclaration dans la liste blanche de `game/card/factory.py`, aux
côtés de `ht009`, `mk008`, `kb005` — et surtout de **`13006` Wasp Sting**,
déjà là pour exactement la même raison (formes GIANT / TINY).

### b. `KILLER_THRILL_NAME` — le piège du `*` d'unicité, tombé dedans après l'avoir lu

La constante cherchait `"* Killer Thrill"`. `cards/paper.py:46` retire le
préfixe (`lstrip("* ")`) : la recherche ne trouvait **rien, en silence**, et
ni Coldwar ni Guzz ne gagnaient jamais leur bonus. Piège déjà documenté sur
`pt012` « * Patriot's Shield ». Un commentaire d'avertissement est désormais
en tête de `venompool_nemesis/__init__.py`.

### c. `vp010` — `Upgrade` n'a pas de méthode `Discard()`

`this.Discard(effect)` levait un `AttributeError` **dans le handler**. Le
déclencheur `AfterCardLeavePlay`, lui, était correct — c'est la trace qui
l'a prouvé. Remplacé par `Faces.DiscardAll([this], effect)`.

---

## 4. Cas de comportement : 7/7, avec preuves par substitution

| Carte | Capacité couverte | Cas | Substitution |
|---|---|---|---|
| `vp002` | contre de base ignore crisis | ✅ | — |
| `vp009` | +3 points de vie | ✅ | — |
| `vp009` | `drain 1`, **les deux moitiés** | ✅ | ✅ sans le module : 0 dégât au lieu de 1 **et** identité à 4 au lieu de 3 |
| `vp010` | défausse quand Klyntar Suit part | ✅ | ✅ sans le module : la carte reste en jeu |
| `vp013` | +1 ATK par compteur d'adrénaline | ✅ | — |
| `vp014` | +1 ATK tant que Killer Thrill est là | ✅ | ✅ étoile réintroduite : le bonus disparaît |
| `vp015` | +1 SCH tant que Killer Thrill est là | ✅ | — |

### Trois pièges de mise en place, consignés dans le `pourquoi` du cas `drain`

1. Sans `ChangeToFace` préalable, `Puzzle.Damage('vp001a')` **instancie une
   seconde identité** dans l'aside deck, et le rendu lève `AssertionError`
   (modèles `ma005`, `hd001a`, qui font tous le `ChangeToFace` d'abord).
2. La face se désigne par **`card_id`** (`vp001b`), jamais par « Wade
   Wilson » : c'est l'homonyme de `44001b`, l'alter-ego de Deadpool.
3. L'attaquant doit être un **sbire** (ATK fixe, pas de carte de boost) et le
   héros **épuisé**. Avec Rhino, le pilote défendait, les dégâts tombaient à
   0 et la Response ne partait pas : **le module avait raison, c'était le cas
   qui était faux.**

---

## 5. Ce qui reste à prouver

- cas `test_capacites` pour les capacités **non encore couvertes** : `vp001a`
  Fear Factor et sa limite, `vp001b` (REC conditionnel, Unexpected Bond),
  `vp003` à `vp008`, `vp011`, `vp012`, `vp016` ;
- `tools/autoplay.py`, 8 parties minimum contre un héros témoin ;
- une partie complète jouée à la main dans le navigateur — **seul juge de
  « est-ce que la carte est agréable et fait ce qu'elle promet »**.

### Leçon d'outillage (coûteuse, à ne pas reperdre)

`tools/test_capacites.py` **n'a pas de filtre par nom** : son docstring
annonce `[filtre]` en 4ᵉ argument, mais `main()` ne lit que `argv[1..3]`. Le
seul moyen de cibler des cas est `CAS_INDEX=<n>`, un cas à la fois.

Avoir cru au filtre a lancé les **776** cas au lieu de 7, en parallèle de la
vérification des decks : la machine saturée a produit **31 faux échecs**
`AssertionError: port=...` (73/105 au lieu de 104/105) et un faux « main vide
après le setup » sur venompool. Le guide prévient déjà que ces échecs-là ne
sont pas des régressions. **Ne jamais lancer deux harnais en parallèle.**
