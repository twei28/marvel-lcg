# Multiverse

**Texte imprimé / définition** : le mot `Multiverse.` apparaît seul, en tête du
bloc de texte d'un **allié signature**, sans aucune parenthèse explicative.
Aucun des trois packs qui l'emploient ne le définit.

**Définition retenue** (arbitrée le 05/09/2026, sur la foi des trois cartes qui
le portent) : *marqueur de DECKBUILDING, sans aucun effet moteur*. Il signale
qu'une carte est **une autre version d'un personnage qui existe déjà ailleurs
dans le jeu**, et rappelle que la règle d'unicité continue de s'appliquer : une
seule version d'un même personnage peut être en jeu à la fois.

Le raisonnement, carte par carte :

| Carte | Personnage | L'autre version déjà au dépôt |
|---|---|---|
| `ra002` `* Odinson` (pack `rainy`) | Thor | `06001a` `* Thor`, héros officiel |
| `bw003` `* Ironheart` (pack `brawn`) | Riri Williams | `bw003` est l'alliée d'un pack où Ironheart existe comme héros |
| `bc003` `* Spider-Man` (pack `blackcat`) | Peter Parker | **quinze** autres `* Spider-Man` au dépôt, dont `01001a` |

Dans les trois cas, la carte marquée `Multiverse` est **la version
ALTERNATIVE** d'un allié livré en plusieurs exemplaires par le même auteur, et
les deux versions portent le **même numéro de set** (`bc002` et `bc003` sont
toutes deux « BLACK CAT (1/15) »). Le joueur en choisit une.

**Mécanisme moteur** : **AUCUN. Zéro ligne de code.** Ni `desc`, ni script.
C'est la règle d'unicité native (l'étoile `*` devant le nom) qui fait le
travail : deux cartes uniques de même nom ne peuvent pas coexister en jeu, et
le moteur l'applique seul.

**Carte exemple** : `ra002` `* Odinson`, dont le module dit déjà, en
commentaire et depuis le portage du pack `rainy` :

```python
# Multiverse. (mot-clé custom de l'auteur, sans effet moteur : une seule
# version « Multiverse » d'un même personnage par deck — géré par l'unicité.)
```

**Pièges connus** :

- ⚠ **`MULTIVERSE` est aussi un TRAIT**, et les deux notions n'ont rien à voir.
  `wd029` Multiverse Recruit (pack `web_of_deceit`) porte
  `"traits": ["MULTIVERSE"]` ; Blink (Earth-295) emploie le même mot comme
  trait. Un trait va dans `traits`, ce mot-clé-ci **ne va nulle part**.
- ⚠ **Ne pas croire que les deux versions sont deux illustrations d'une même
  carte.** `bc002` et `bc003` ont des statistiques, des traits et des
  capacités DIFFÉRENTS (PV 4 contre 3, SYMBIOTE + WEB-WARRIOR contre AVENGER) :
  ce sont deux `card_id` distincts, et le nom de fichier du zip
  (« 1 Spider-Man (black) » / « 1 Spider-Man (red) ») est le seul indice qu'il
  s'agit du même numéro de set.
- ⚠ **Le deck de départ du dépôt inclut les DEUX versions.** Précédent
  `thor_jane_foster`, dont le `hero_deck` compte 16 entrées et contient à la
  fois `ra002` (Multiverse) et `ra003`. Le mot-clé n'interdit pas de les mettre
  toutes les deux dans le deck, seulement d'en avoir deux en jeu.

**Variantes maison** : aucune. Trois packs, trois auteurs différents
(`rainy`, `brawn`, `blackcat`), même écriture nue et même absence de
définition.
