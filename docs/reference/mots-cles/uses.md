# Uses

**Texte imprimé / définition** : « Uses (N <nom> counters). » La carte entre
en jeu avec N pions du type nommé. Quand le **dernier** pion est retiré, la
carte quitte le jeu : c'est la règle du mot-clé, pas un effet de la carte.
Rien n'est imprimé pour cette sortie, et c'est précisément pour ça qu'on
oublie de la vérifier.

Le nom du pion est libre (`doubt`, `emergency`, `pheromone`, `charge`,
`unworthy`, `foe`…) et n'a aucune sémantique : deux cartes qui portent le même
nom de pion ne se parlent pas pour autant.

**Mécanisme moteur** : clé `desc.Uses` valant `"<N>,<nom_du_pion>"`, lue
nativement par `HasUses`
(`src/game/card/face/attribute/has_uses.py`). **Aucun script requis**, ni pour
poser les N pions, ni pour faire sortir la carte. Deux points d'ancrage :

- `OnWhenCardEnterPlay` (ligne 20) pose les N pions à l'entrée en jeu ;
- `RemoveCountersInternal` (ligne 46) surveille chaque retrait : dès que
  `GetAllCounters() <= 0`, la carte part.

⚠ Le nom du pion doit passer `IsCounter()` (`game/element/utility.py`) :
`has_uses.py:15` pose un `assert` sec. Un nom absent de l'énumération fait
tomber la construction de la carte, pas la partie.

Le retrait d'un pion s'écrit soit en effet
(`Faces.RemoveCountersOn([this], 1, '<nom>', effect)`, modèle `53029`), soit
en **coût** (`CostFunc.Counter("This", 1, '<nom>')`, modèle `61033a`).

**Carte exemple** : `61033a` : Suggestion ([energy]) — lu directement depuis
`desc` pour les pions et la sortie de jeu ; le script ne code que la capacité
imprimée :

```python
AbilityFactory.WhenInYourPlayTurn(AbilityType.ForcedAction, suggestion)
.SetCostFunc(CostFunc.Exhaust("This")).SetCostFunc(CostFunc.Counter("This", 1, 'pheromone')),
```

**Pièges connus** :

- **Ne pas coder la sortie de jeu.** Le réflexe est d'ajouter un
  `WhenTheLastCounterIsRemovedFromHere` qui défausse la carte : il ferait
  double emploi avec `RemoveCountersInternal` et défausserait deux fois. Cette
  fabrique ne sert que pour un effet EN PLUS de la sortie (modèle `wd057`, qui
  retourne Curt Connors).
- ⚠ **`GetAllCounters()`, pas le compteur nommé.** La sortie se déclenche
  quand la carte n'a **plus aucun pion, tous types confondus**. Une carte à
  `Uses` sur laquelle un autre effet pose un pion d'un type différent ne part
  donc pas tant que ce pion-là reste. Aucune carte du dépôt n'est dans ce cas
  aujourd'hui, mais le montage est possible et le comportement surprendrait.
- ⚠ **`Victory 0` ne va PAS dans la pile de victoire.** `has_uses.py:54` teste
  `if self.victory:` : `Victory 0` vaut l'entier `0`, donc faux, et la carte
  est **défaussée**. Les règles imprimées, elles, envoient une carte
  « Victory 0 » dans la pile de victoire (pour 0 point). L'écart est sans
  conséquence tant qu'aucune carte ne COMPTE les cartes de la pile de
  victoire — et le commentaire `# Hack` du moteur cite justement `51031`, une
  carte à `Victory 0`, ce qui laisse penser que l'intention était l'inverse.
  Cinq cartes livrées sont concernées : `51031`, `53029`, `59004`, `br012` et
  `tg011`. À rouvrir le jour où une carte lira la pile de victoire.
- **La carte doit être EN JEU** (`self.IsInPlay()`), sinon le retrait de pion
  ne déclenche rien. Retirer un pion d'une carte en défausse est inerte.

**Variantes maison** : aucune. Les packs maison qui emploient `Uses`
(`br012` Unworthy, `sr013` Bad Publicity, `tg011` Trouble in Central Park)
suivent tous la règle officielle sans l'étendre.

**Obligation a Uses** (`gs065` Protector of the Universe, Galactic Storm, 20/10/2026) : « Uses (3 duty counters) »
sur une obligation qui reste dans la zone des obligations ; les pions sont poses a la revelation et la carte part au
dernier pion retire, sans script (cas `[quasar] gs065 ... DERNIER pion`). Compteur `duty` ajoute a `CardFace.COUNTER`.
