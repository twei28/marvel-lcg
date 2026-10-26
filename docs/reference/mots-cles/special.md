# Special et l'étoile ★ d'une capacité permanente

**Texte imprimé / définition** : deux notions que le mot « Special » confond.
1. Le **`[star]` en tête d'une ligne de texte** d'une carte de rencontre : une
   capacité PERMANENTE, toujours active tant que la carte est en jeu (par
   exemple « ★ Black Berserker gets +X hit points »).
2. La **capacité « Special » nommée**, rare, qu'une AUTRE carte vient résoudre
   explicitement.

**Mécanisme moteur** :
- **Cas 1, le ★ permanent** : type `AbilityType.NonKeywordStar`
  (`src/game/ability/ability_type.py`, valeur interne `"ConstantStar"`,
  priorité `TimingPriority.Constant`). Rien dans `desc` : seule la ligne
  `[star] <effet>` dans le champ racine `text` de `data/cards.json`, plus la
  capacité dans le module. Le pendant sans étoile est `AbilityType.NonKeyword`.
- **Cas 2, la capacité nommée** : `AbilityFactory.WhenResolveSpecialAbility`
  (`src/game/ability/factory/resolve.py`, type `AbilityType.Special`). Le
  moteur la cherche par `self.effect.Find(type=AbilityType.Special)`
  (`src/game/card/face/card_face.py`) quand une carte demande de résoudre une
  capacité spéciale.

**Carte exemple** : cas 1 : `01132` (* Melter, pack `core`),
`WhenUnitAttackYou(AbilityType.NonKeywordStar, "This", ...)` ; copie commentée
dans `an013` (pack `angela`). Cas 2 : `ab007` (pack `albert`).

**Pièges connus** :
- **Convention du projet** : une capacité `[star]` SANS la mention « In expert
  mode » est codée TOUJOURS active (cf. `RECETTES-MOTEUR.md`). Réserver
  `expert_mode_only=True` aux textes qui le disent.
- Le ★ d'un effet **Boost** (sous le trait horizontal, « [star] Boost: … ») est
  autre chose : c'est un `AbilityType.Boost`, voir [[boost]].
- `NonKeywordStar` sur un effet continu ne se rafraîchit pas tout seul quand la
  quantité qu'il lit change : un « +X PV où X = nombre d'attachements » doit
  passer par une fabrique qui recalcule, ou déclarer son événement de
  rafraîchissement.

**Résoudre un Special HORS de la table** (pack `zeus`, 11/09/2026) : Hera
résout le Special d'une carte EN MAIN, *Skyfather's Tempest* celui d'un
événement PENDANT son paiement. `ResolveSpecialAbility` ne trouve alors aucun
effet enregistré. Recette dans `RECETTES-MOTEUR.md` §4 : déclarer le Special
avec `.NoOutOfPlayLimit()`, et l'enregistrer en temporaire juste avant de le
résoudre (`ResoudreLeSpecialDe`, `cards/pack/zeus/zeus/__init__.py`). Lire
« a printed Special » avec `face.ability.Find(type=AbilityType.Special)` (les
capacités DÉCLARÉES), jamais `face.effect.Find` (les effets enregistrés, qui
dépendent de la zone).

**Variantes maison** : `gb009` (Black Berserker, pack `gorr`) : `[star]` qui
donne des PV proportionnels au nombre d'attachements NECROVERSE en jeu, plafonné
à 4 — la valeur bouge en cours de partie, l'étoile doit donc être recalculée et
non figée à l'entrée en jeu.

**Capacité Special NOMMÉE sur un complot principal** (scénario Baxter Stockman, 16/10/2026) : `tx004b` porte
« *Replicate* — Special : ... », résolue par `tx001-tx003`, `tx008`, `tx009`, `tx011` (« each player resolves the Special
on the Baxter's Laboratory scheme »). `WhenResolveSpecialAbility("This", op)` sur la face 1B, appelants via
`ResoudreLeSpecial(effect, joueur)` : fiche `replicate.md`.


## Pack Roz (jakxin, `rz`, 25/10/2026) : tout un héros construit sur « Special »

- **Résoudre le Special d'une carte précise** : `joueur.ResolveSpecialAbility(faces, effect)` envoie `WhenResolveSpecialAbility` à
  chaque face ; seules les cartes qui IMPRIMENT un Special réagissent. Pour proposer au joueur « une carte WAKANDA qui a un
  Special » : `SetTarget("Hero|Ally|Upgrade|Support", trait="WAKANDA", from_where=["YouControlCards"], check_fn=ADesSpecial)` avec
  `ADesSpecial = face.ability.Find(type=AbilityType.Special)` (`roz/roz/__init__.py`, `CarteWakandaSousControle`) ; `exclude="This"` =
  « ANOTHER card ». Modèles : `51001a` (héros), `51025` (événement).
- **Compter les Specials résolus ce tour** (« for each Special ability resolved this turn », « if you resolved a Special this turn ») :
  `PlayerStat.this_turn_resolved_specials` (CORRECTIF du 25/10/2026), alimenté par `EffectInvoker._ResolveSelfInternal` pour toute
  capacité `AbilityType.Special` dont le coût est payé ; vidé à chaque tour. Une carte à DEUX Specials (rz006) en fait compter deux.
- **« After you resolve a Special ability »** : `AbilityFactory.AfterPlayerResolveAbility(Response, "You", None, op,
  which_abilities=["Special"], control_by_you=True, conditions=[...])` ; `message.trigger` = la carte dont le Special a été résolu
  (« on ANOTHER card » : `message.trigger is not effect.this`). Modèle : `storm/36007`.
- **Deux Specials imprimés sur la même carte** (rz006, DÉCISION UTILISATEUR du 26/10/2026) : « resolve the "Special" ability » n'en résout
  qu'UN, au choix du joueur (le texte dit « the Special » au singulier ; chaque Special a sa propre limite). Rendu : UNE seule capacité
  `WhenResolveSpecialAbility("This", op)` pour le moteur (une seule résolution comptée dans `this_turn_resolved_specials`), dont `op` fait
  `joueur.ChooseAbilities(effect, ForChoiceAbility(.., condition=libre1), ForChoiceAbility(.., condition=libre2))`. ⚠ La limite « once per
  round » de chaque effet est un MARQUEUR DE ROUND posé sur la carte au moment de l'effet : `LimitOncePerRound()` se serait consommée même
  quand l'AUTRE effet est choisi. (Avant : deux capacités sans nom, les deux résolues d'un coup.)
- **Banc de test** : `Puzzle.ResolveSpecial('<card_id>')` (CORRECTIF du 25/10/2026, `puzzle.py`) résout le Special d'une carte en jeu,
  cibles et coûts compris.


## Pack Hepzibah (Phenexian et Mysteltainn, `hz`, 26/10/2026) : le Special des événements de la MAIN

- **Quatre événements portent un Special** (`hz007` Feral Rage, `hz008` Keen Senses, `hz009` Feline Grace, `hz010` Armed to the Teeth) ;
  l'identité (`hz001a`), l'allié Corsair (`hz002`) et Energy Blaster (`hz005`, quand son action VAINC) en résolvent un **depuis la
  main**. Helpers du set : `APrintedSpecial`, `ResoudreLeSpecialDe`, `ResoudreUnSpecialEnMain` (`src/cards/pack/hepzibah/hepzibah/__init__.py`),
  calqués sur `zeus` (`ResoudreLeSpecialDe`, RECETTES §4) : enregistrement temporaire du Special puis `ResolveSpecialAbility`.
- **Le Special d'un événement se déclare `WhenResolveSpecialAbility("This", op).NoOutOfPlayLimit()`** ; dans `op`, le joueur est
  `message.GetToPlayer() or effect.GetInitiator()`.
- ⚠ **« (Limit once per phase.) » d'un Special résolu depuis la main** : `LimitOncePerPhase()` ne vaut pas pour une carte hors jeu.
  Marqueur `(effect.world.round_id, effect.world.phase_id)` posé SUR LA CARTE (`hz009`), avec un témoin d'épuisement (le héros est
  ré-incliné entre deux résolutions : il reste incliné à la seconde).
- Le choix de la carte à Special se fait **par le joueur** (`AskChooseFace(.., forced=True)`) ; le pilote du harnais prend la première
  candidate de la main, dans l'ordre de `main_exclusive` : poser la carte voulue EN PREMIER.

