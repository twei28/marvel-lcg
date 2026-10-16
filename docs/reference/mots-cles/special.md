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
