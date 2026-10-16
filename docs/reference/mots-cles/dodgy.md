# Dodgy (Esquive)

**Texte imprimé / définition** : « Dodgy. *(When a character thwarts this side
scheme, they may use their DEF instead of their THW.)* » Mot-clé du scénario TMNT
Bebop & Rocksteady (Inkwire). L'encart précise : « The dodgy keyword works very
similar to the assault keyword. When a character thwarts a side scheme with
dodgy, they may choose to use their DEF value rather than their THW value.
**Important Note**: Unlike assault, the dodgy keyword does not require
characters to use their DEF. » Il ne vit que sur des **manigances annexes**
(Bumbling Buffoons `tk013`-`tk015`, Toro! Toro! `tk020`).

**Mécanisme moteur** : AUCUNE clé `desc` (le mot-clé n'est pas dans
`CardFace.KEY`, donc le texte seul le porte). Il est rendu par la fabrique
`Dodgy()` du `__init__.py` du pack (`src/cards/pack/bebop_rocksteady/`) :
`WhenUnitThwartScheme(AbilityType.Rule, None, op, which_card_be_thwart="This",
is_basic_thwart=True)`, sur le modèle d'`Assault` (`has_assault.py`) qui fait la
même chose mais **d'office** et avec l'ATQ. L'opération calcule
`DEF - THW` et, si c'est positif, **propose** le choix au joueur qui contre
(`MayChooseOneAbility`) : accepter applique `message.GainThwartForThisThwart`.

**Carte exemple** : `tk020` (Toro! Toro!) : `Dodgy()` plus un « When Defeated ».

**Pièges connus** :
- Facultatif, contrairement à Assault : le cas `tk020 ... Dodgy REFUSE` (`choisir_option="Cancel"`) mesure 4 → 3, le cas ACCEPTE 4 → 1 (Spider-Man THW 1, DEF 3).
- Ne vaut que pour le pouvoir de **base** (THW) : un effet de carte qui contre
  (« thwart » d'événement) ne passe pas par ce mot-clé.
- La question n'est posée que si la DEF dépasse la CTR (sinon rien à gagner).
- Les copies sans le script n'ont pas le mot-clé : les TROIS illustrations de
  Bumbling Buffoons ont chacune leur module (`tk013`, `tk014`, `tk015`).
- Le texte imprimé ne s'affiche pas en tooltip (`mots-cles.ts` ne lit que les
  clés de `desc`).

**Variantes maison** : le mot-clé est lui-même maison.
