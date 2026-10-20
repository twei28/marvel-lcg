
---

## 5. Le deck de départ, le set némésis, les variantes, l'extension

### 5.1 Le fichier `deck/starter/<héros>.json`, clé par clé

Le nom du fichier (`lockjaw.json`) est **l'identifiant du héros** : minuscules, chiffres, `_`. Il est unique dans
le jeu (voir `reference/decks-existants.json`, 152 identifiants). C'est aussi la clé de la réplique de recrutement.

| Clé | Type | Contenu | Mesuré sur les 152 decks |
|---|---|---|---|
| `version` | texte | `"0.5.8"` ou `"0.5.9"` (sans effet) | 0.5.8 ×132, 0.5.9 ×20 |
| `name` | texte | le nom **affiché** du héros | toujours |
| `metadata` | objet | `url` (source, ou `""`), `author`/`auteur`, `note`/`deck_note`, variantes, règles de deck-building (§5.3, §5.7) | toujours |
| `hero` | liste d'**une** chaîne | `"<face a>,<face b>[,<forme de plus>…]"` : héros d'abord, alter ego ensuite | toujours |
| `hero_deck` | liste de card_id | les cartes signature, **un id par exemplaire** (id répété = plusieurs exemplaires) | 15 cartes pour 145 decks |
| `set_aside` | liste | `[]` : **le moteur ne le lit pas en partie** (§2.2) | présent dans 150 |
| `obligations` | liste de card_id | l'obligation (UNE) | 1 pour 148 decks |
| `nemesis_set` | liste de card_id | le set némésis, exemplaires comptés | 5 pour 145 decks |
| `player_deck` | liste de card_id | la moitié d'aspect **fournie par l'auteur** ; **`[]` sinon** (règle 10) | `[]` pour 53 decks, 25 cartes pour 90, 24 à 27 pour 8, 15 pour 1 |
| `linked_identity` | objet | seulement Cloak & Dagger (§5.6) | 1 |

Un deck **complet** d'un héros maison **avec la decklist de l'auteur** (Lockjaw) :

{{FICHIER:Fusion/marvel-lcg-src/deck/starter/lockjaw.json|json}}

Un héros **officiel dont l'éditeur n'a pas tout publié** (Iron Fist, 20/10/2026) : `obligations` et `nemesis_set`
vides, `player_deck` vide, et une `deck_note` qui dit ce qui manque et pourquoi.

{{FICHIER:Fusion/marvel-lcg-src/deck/starter/iron_fist.json|json}}

### 5.2 Règles de contenu (toutes contrôlées par `verifier-livraison-heros.py`)

1. **`hero`** : la première face est de type `Hero`, la deuxième de type `AlterEgo` ; une forme de plus (`c`…)
   se liste **après** (Ant-Man : `"12001a,12001b,12001c"`). Les trois (ou cinq) faces existent dans `cards.json`.
2. **`hero_deck`** : ne contient que des cartes **de classe `Hero` de CE héros** (même `set_name`). **Jamais la
   carte signature d'un autre héros** (règle 11). Compte attendu : 15 (145 decks sur 152) ; un autre total se
   **justifie** dans `QUESTIONS.md` (le deck imprimé est-il vraiment différent ?).
3. **Exemplaires** : le plus grand nombre d'exemplaires d'un même titre vaut 3 dans 86 decks, 2 dans 44, 1 dans 12, 4 dans 8, 5 dans 2. Si la carte
   imprime `MaxPerDeck`, c'est la limite. Plus de 3 sans `MaxPerDeck` → vérifie l'image.
4. **`obligations`** : une carte de type `Obligation`, avec `desc.GiveTo` = nom de l'alter ego.
5. **`nemesis_set`** : des cartes de rencontre (jamais des cartes joueur), de `set_name` `"<Héros> Nemesis"` ;
   un sbire marqué `desc.Nemesis`. Un set **emprunté** à un autre héros (Viv Vision emprunte le modulaire Zzzax)
   est possible : c'est une décision, à écrire dans `metadata.nemesis_note`.
6. **`player_deck`** : **vide** pour un héros maison, **sauf** si l'auteur fournit sa decklist ; alors
   `metadata.note` le dit (« Decklist officielle du scan StarterDeck-… »), chaque id existe, aucune signature
   d'un autre héros, 24 à 27 cartes. Héros **officiel** : le deck imprimé dans la boîte.
7. **`metadata.author`** (ou `auteur`) = la clé `custom` des cartes du héros maison.

### 5.3 Variantes d'un héros

Un héros n'a qu'**une tuile** dans le lanceur. Ce qu'il a de particulier se choisit dans une **modale** au clic
(version du deck de héros, identité alternative, art, ressources). Trois mécanismes, à ne pas confondre :

| Le héros a… | Où le déclarer | Exemple |
|---|---|---|
| un autre **deck de héros** (allié signature, alter ego avec sa propre obligation) | un **second** `deck/starter/<id>.json` **complet**, avec `metadata.variante_de: "<id de base>"` et `metadata.variante_nom` ; **la base porte aussi son `variante_nom`** | `hellcat.json` + `hellcat_she_hulk.json` |
| une autre **identité** dans le même deck (mêmes cartes, autres faces) | `metadata.hero_alts` du deck de base : `[{"name": "…", "hero": ["xx001c,xx001d"], "url": "…"}]` | The Thing Guardian (`th001c,th001d`) |
| un **art** alternatif | `ARTS_HEROS` (côté Claude, `BESOINS-MOTEUR.md`) | M3T4LB0X |

Le fichier de variante reste un deck **montable** (même contrôle que le deck de base). C'est le catalogue qui le
replie sous sa base, pas le moteur. **Ne crée jamais un deuxième deck de départ pour une identité alternative**
(`hero_alts`) : un deuxième héros apparaîtrait dans la grille.

Les deux exemples réels, côté métadonnées seulement :

{{BLOC:Fusion/marvel-lcg-src/deck/starter/hellcat_she_hulk.json|"metadata"|"hero": [|json}}

{{BLOC:Fusion/marvel-lcg-src/deck/starter/the_thing.json|"metadata"|"hero": [|json}}

### 5.4 `data/nemesis/<héros>_nemesis.json` (facultatif)

⚠ **Ce n'est pas « pour l'interface »** (vérifié au grep) : ni le lanceur ni le plateau ne lisent ce dossier. Le
`nemesis_set` affiché vient du **deck de départ**, et le moteur le lit au même endroit. Le fichier sert à
charger le set némésis **comme un set de rencontre nommé** (`data/nemesis/` figure dans les dossiers de sets de
rencontre du moteur) : utile le jour où une carte ou un scénario le réclame par son nom. Cinq packs récents
n'en ont pas et fonctionnent. Si tu le livres, `encounters` = **exactement** `nemesis_set` :

{{FICHIER:Fusion/marvel-lcg-src/data/nemesis/lockjaw_nemesis.json|json}}

### 5.5 L'entrée de l'extension : `data/sets_info.<pack>.fragment.json`

La liste `heroes` de l'entrée est ce qui range le héros dans son extension. Pour un pack de héros : `scenarios`
et `encounters` sont **vides** ; `name` = la clé du pack ; `max_id` = le plus grand `card_id`. La clé est
`"N. Custom (<Nom>)"` pour un héros maison (`N` est attribué par Claude : laisse la lettre `N`) ; pour un héros
officiel, `"<n° du pack>. <Nom>"`.

{{SETSINFO:117. Custom (Lockjaw)}}

{{SETSINFO:64. Iron Fist}}

### 5.6 L'identité liée (Cloak & Dagger) — pour information

Un pack qui fait piloter **deux identités par un seul joueur** déclare, dans le deck, une clé `linked_identity` :
une identité complète (`hero`, `hero_deck`, `set_aside`, `obligations`, `nemesis_set`, `player_deck`) que le
moteur développe en un **second joueur** au chargement. C'est le **seul** pack construit ainsi : n'invente pas ce
mécanisme pour un héros ordinaire ; si le héros que tu livres l'exige, **question** et `BESOINS-MOTEUR.md`.

### 5.7 Règles de deck-building propres au héros : `metadata.deckbuilding`

Certaines identités changent les règles de construction (autant d'aspects que l'on veut, N cartes d'autres aspects
pourvu qu'elles aient tel trait…). Le deck-builder les applique ; **le moteur ne valide jamais un deck** — ces
règles n'existent que dans le deck-builder, et un deck de départ écrit à la main les contourne. On les déclare dans
`metadata.deckbuilding`, **accompagnées d'une `deckbuilding_note`** qui cite le texte imprimé. Dix decks du jeu
en ont :

{{DECKBUILDING:}}

Les clés reconnues (`public/js/deckbuilder/regles.js`) : `aspects {min, max, label}`, `hors_aspect {max, traits,
types, compte, label}` (`"compte": "titres"` compte des titres et non des exemplaires), `types_interdits`,
`types_interdits_aspect`, `ressources_egales {couleurs, label}`, `path {…}` (voies TMNT Shinobi). Toute autre
clé est une **erreur**. Une règle que ces clés ne savent pas dire → `BESOINS-MOTEUR.md`.
