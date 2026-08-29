# Squirrel

**Texte imprimé / définition** : mot-clé maison du pack `squirrel_girl`
(héroïne custom **Squirrel Girl**), porté par les six alliés du « deck
écureuil ». Texte exact lu dans `cards.json` sur * Tippy-Toe (`sg002`) :
« Squirrel. *(Does not count against your ally limit. Cannot defend.
Cannot have upgrades attached. Cannot be chosen or strengthened by
non-Squirrel Girl player cards. When it leaves play, put it into the
Squirrel discard pile. Can be spent for Squirrel Aid.)* ». Contrairement à
Companion, ce texte ne se réduit pas à deux règles : il en couvre cinq, et
seules les trois premières sont portées par la fonction du mot-clé
elle-même (voir plus bas).

**Mécanisme moteur** : composé dans `Ecureuil()`
(`Fusion/marvel-lcg-src/src/cards/pack/squirrel_girl/squirrel_girl/__init__.py`,
lignes 283-299), commune aux six cartes du deck écureuil :

```python
def Ecureuil() -> List['Ability']:
    return [
        *AbilityFactory.ThisNotCountAllyLimit(),
        *AbilityFactory.UnitCannotDefend(
            "This",
            None,
            cannot_trigger_defense_ability=True,
        ),
        *AbilityFactory.UnitCannotHaveUpgradeAttached("This"),
    ]
```

Les deux premières fabriques sont identiques à celles de `Companion()` (voir
`companion.md`) : `ThisNotCountAllyLimit()` pour « ne compte pas dans la
limite d'alliés », `UnitCannotDefend("This", None,
cannot_trigger_defense_ability=True)` pour « ne peut pas défendre ».
`UnitCannotHaveUpgradeAttached("This")`
(`game/ability/factory/ability_factory.py`, lignes 287-314) ajoute « ne peut
pas recevoir d'amélioration » : elle écoute `Message.CheckIfFaceCanAttachTo`
pour refuser l'attache dès l'intention (`SetCannotAttachTo`), et
`Message.WhenCardWouldAttachTo` en filet de sécurité, qui défausse
l'amélioration à la place de l'attacher (`SetBeInstead` +
`Faces.DiscardAll`) si elle passait quand même.

Ces trois fabriques ne couvrent que 3 des 5 clauses du texte imprimé. Les
deux autres sont portées ailleurs, pas par `Ecureuil()` :

- « *Cannot be chosen or strengthened by non-Squirrel Girl player cards* »
  passe par deux points d'accroche posés carte par carte dans
  `PreparerEcureuil(face, joueur)` (lignes 134-159), appelée une fois par
  écureuil au setup : `face.refuse_target_fn` et `face.refuse_gain_fn` sont
  réglés sur `_EstSourceEtrangere`, qui renvoie vrai si la source de l'effet
  est une carte joueur hors du set. Ce ne sont pas des capacités
  interceptables : `refuse_target_fn` est lu en direct par
  `GetAllLegalTargets` (le seul entonnoir de sélection de cibles) et
  `refuse_gain_fn` par `Gain`, qui est `@final`.
- « *When it leaves play, put it into the Squirrel discard pile* » passe
  aussi par `PreparerEcureuil`, qui enregistre sur chaque écureuil un
  `WhenCardWouldMoveToArea` (`AbilityType.Temp0`) : dès que le mouvement
  visé est vers `discard_pile` ou `player_deck`, il est redirigé vers
  `additional_discard_pile` / `additional_deck` du joueur
  (`message.ChangeToArea(...)`).
- « *Can be spent for Squirrel Aid* » passe par `CapaciteDepenseIdentite()`
  (lignes 235-280), une capacité `Resource` (« Discard a SQUIRREL ally you
  control → 1 [wild] », `for_card=FinderCarteSquirrelGirl()`) posée sur les
  deux faces d'**identité** (`sg001a` et `sg001b`, appel confirmé aux lignes
  47 et 30 de leurs fichiers respectifs), et non sur les six écureuils. Le
  docstring de la fonction explique pourquoi : le moteur recense les
  sources de paiement une seule fois, avant toute dépense, et chaque
  capacité ne compte que pour une source. Poser la capacité sur les six
  écureuils offrirait six sources qu'il serait ensuite impossible de
  limiter (refuser une source déjà recensée fait échouer l'assertion
  `len(resources_effects) == 1` de `ProcessPayingEffect`). Avec une source
  unique sur l'identité, la limite « 1 seul écureuil par carte jouée » du
  matériel d'origine devient structurelle : le joueur choisit toujours quel
  écureuil part, via le coût (`CostFunc.Custom` ciblant un allié `SQUIRREL`
  qu'il contrôle).

**Carte exemple** : `sg002` (* Tippy-Toe), extrait de
`Fusion/marvel-lcg-src/src/cards/pack/squirrel_girl/squirrel_deck/sg002.py` :

```python
return [
    *Ecureuil(),
    AbilityFactory.AfterCardEnterPlay(
        AbilityType.Response,
        "This",
        reordonner,
        conditions=[PasDeDiscorde],
    ),
]
```

Les six écureuils (`sg002` à `sg007`) portent tous `*Ecureuil()` en tête de
leurs capacités, confirmé par lecture du dossier
`Fusion/marvel-lcg-src/src/cards/pack/squirrel_girl/squirrel_deck/`. Notes
sur l'identifiant : les card_id du pack suivent le format `sgNNN` (`sg001a`,
`sg001b`, `sg002`…`sg022`), pas le format numérique `750NN` mentionné dans
une version antérieure du plan de doc ; une recherche `grep "\"750"` sur
`cards.json` ne renvoie donc rien pour ce pack, il faut chercher par
`"card_id": "sg0` ou par le nom des cartes.

**Pièges connus** :

- Les cartes du deck écureuil sont hors jeu : elles ne se désignent PAS par
  `SetTarget(Select.From(faces=...))` (le sélecteur ne les restreint pas),
  mais par `player.MayChooseFace(faces, effect, not_move=True)`. Vu à
  l'œuvre dans `AppelerEcureuil` (interruption de Network of Trees,
  `sg012`) et dans `sg002.reordonner` (Tippy-Toe reclasse le dessus du deck
  écureuil).
- Poser `CapaciteDepenseIdentite()` sur chaque écureuil au lieu de
  l'identité casserait la limite « 1 écureuil par carte jouée » : voir
  l'explication détaillée ci-dessus (assertion `ProcessPayingEffect`).
- `Puzzle.PutIntoPlay` crée une copie NEUVE de la carte, qui n'a reçu aucune
  règle de setup (ni `PreparerEcureuil`, ni le montage du deck écureuil) :
  tout cas de test portant sur les règles d'un écureuil doit le faire
  APPELER par le jeu (`AppelerEcureuil`), pas le poser directement en jeu.

**Variantes maison** : **Companion** (pack `lockjaw`, voir `companion.md`)
partage la même base `ThisNotCountAllyLimit()` +
`UnitCannotDefend("This", None, cannot_trigger_defense_ability=True)`, sans
la troisième fabrique (`UnitCannotHaveUpgradeAttached`) ni la mécanique de
dépense.
