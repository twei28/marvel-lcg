
---

## 2. Un héros dans le jeu : ce que c'est, et son voyage du fichier à la table

### 2.1 Un héros, ce sont six choses

| # | Quoi | Où | Qui s'en sert |
|---|---|---|---|
| 1 | **Les cartes** : deux faces d'identité, ~15 cartes signature, 1 obligation, 5 cartes némésis (et, pour un héros officiel, les cartes d'aspect de la boîte) | `data/cards.json`, clé = le **pack** | le moteur, le plateau, le deck-builder |
| 2 | **Le deck de départ** : l'identité, les cartes signature, l'obligation, le set némésis, l'éventuelle moitié d'aspect | `deck/starter/<héros>.json` | le moteur (partie), le lanceur (la **liste des héros**) |
| 3 | **L'extension** : à quelle boîte le héros appartient | `data/sets_info.json`, liste `heroes` | le lanceur, le deck-builder |
| 4 | **Les scripts** : ce que font les cartes | `src/cards/pack/<pack>/…` | le moteur |
| 5 | **Les textes et l'habillage** : français, biographie, réplique de recrutement, images, crédits | `ui-app/src/board/textes-fr-fanmade.ts`, `public/js/prepare/heros-info.js`, `repliques-heros.js`, `assets/pics/` | le plateau, le lanceur |
| 6 | **Les preuves** : cas de test, gabarits | `tools/cas/…`, `docs/packs/<héros>_cartes.md` | Claude |

⚠ **Le deck de départ n'est pas un « deck de joueur » : c'est la fiche d'inscription du héros.** Sans lui, le
héros n'apparaît **nulle part**, pas même dans le deck-builder, parce que `catalog.heroes()`
(`public/js/prepare/catalog.js`) construit la liste des héros **en lisant `deck/starter/*.json`**. On l'écrit donc
toujours, avec **ce qui est imprimé et rien d'autre**.

### 2.2 Le voyage, étape par étape

1. **Le lanceur** (`public/prepare.html`, `public/js/prepare/`) lit `deck/starter/*.json` : un fichier = une tuile
   de héros. Il range chaque héros dans son **extension** grâce à la liste `heroes` de `data/sets_info.json`. Une
   extension dont la clé contient « Custom » (`117. Custom (Lockjaw)`) est rangée parmi les héros **fan-made**
   (`isHomebrew`, `catalog.js`) et affiche le nom du créateur (champ `custom` de la face héros, `auteur.js`).
2. **Au survol d'une tuile**, le lanceur affiche la **biographie** (`public/js/prepare/heros-info.js`, indexée par le
   `card_id` de la **face héros**). Au recrutement, une **réplique** s'affiche sur la carte
   (`public/js/prepare/repliques-heros.js`, indexée par l'**identifiant de deck**).
3. **Le joueur choisit** un deck de héros (la modale du héros propose les **variantes** : autre deck de héros,
   autre identité, autre art), construit ou choisit sa moitié d'aspect dans le **deck-builder** — le
   `player_deck` du fichier n'en est que le *deck par défaut* —, puis lance la partie.
4. **Le moteur** charge le fichier (`SceneLoader` → `FileManager.FindJsonPath('Hero', …)` cherche dans `./deck/`
   puis `./deck/starter`) et en fait un `HeroDescriptor` par joueur.
5. **La mise en place du joueur** — `PlayerSetup.SelectIdentity` (extrait ci-dessous) :
   * les faces de `hero` sont fabriquées, **la face `b` (alter ego) d'abord** : le héros **commence en alter
     ego** ;
   * `obligations` et `nemesis_set` sont fabriqués et **mis de côté** (`set_aside_obligations`,
     `set_aside_nemesis_sets`) ; chaque carte némésis est **marquée** `nemesis_of_player` ;
   * `hero_deck` (cartes signature) et `player_deck` sont fabriqués et **mélangés** en un seul deck.
6. **En partie**, le héros alterne ses formes (`ChangeToForm`) ; les capacités imprimées sur les faces `a` et `b`
   sont des scripts comme les autres ; ATK / THW / DEF / REC de base et la taille de main viennent de `desc` et
   sont **automatiques**.

{{BLOC:Fusion/marvel-lcg-src/src/game/player/element/player_setup.py|    def SelectIdentity|        # CORRECTIF (02/09/2026) : marquer|python}}

⚠ `HeroDescriptor` (`src/game/scene/replay/hero.py`) ne connaît **que** : `version`, `name`, `hero`, `hero_deck`,
`obligations`, `nemesis_set`, `player_deck`, `linked_identity`, `team`. **Le champ `set_aside` du fichier de deck
n'est pas lu en vraie partie.** Une carte qu'un héros « met de côté à la mise en place » doit être créée par le
héros lui-même (`AbilityFactory.BeginGameWithSetAside([...])` sur la face alter ego, §6.4).

{{FICHIER:Fusion/marvel-lcg-src/src/game/scene/replay/hero.py|python}}

### 2.3 Ce que le jeu contient déjà (mesuré le 20/10/2026)

{{STATS:}}

### 2.4 Ce qui existe en plus, et que tu ne produis pas

Ces fichiers touchent aussi un héros, mais **Claude** les génère ou les met à jour (tu n'as pas à les écrire, et
tu ne dois pas les inventer) : positions des bulles de statistiques (`ui-app/src/components/stat-bubbles/positions.ts`,
générées par `ui-app/outils/calibrer-stat-bubbles.py` à partir de l'image), palette du héros
(`data/palettes-heros.json`, `outils/palettes-heros.py`), annuaire d'identités (`data/identites.json`,
`outils/annuaire-identites.py`), arts alternatifs cosmétiques (`ARTS_HEROS`), checksums de `cards.json` /
`sets_info.json` (`tools/recalculer_checksums.py`), numéro d'extension (`N.` dans la clé de `sets_info`), entrée de
nouveautés. Si ton héros a besoin d'une de ces choses de façon particulière (une identité alternative, un art),
**dis-le dans `BESOINS-MOTEUR.md`**.
