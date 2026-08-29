# Companion

**Texte imprimé / définition** : mot-clé maison du pack `lockjaw` (héros
custom **Lockjaw**, « Nugget », Marvel Champions Custom Project Cycle I),
porté par plusieurs alliés du deck signature. Texte exact lu dans
`cards.json` sur * Hairball (`lj021`) : « Companion. *(This ally does not
count towards the ally limit, and it cannot be used to defend against
attacks.)* ». Le texte entre parenthèses est celui qui définit le mot-clé,
imprimé identiquement sur chaque carte qui le porte.

**Mécanisme moteur** : composé dans `Companion()`
(`Fusion/marvel-lcg-src/src/cards/pack/lockjaw/lockjaw/__init__.py`) à
partir de deux fabriques génériques déjà présentes dans le moteur, sans
mot-clé dédié :

```python
def Companion() -> List['Ability']:
    """« Companion » : hors limite d'alliés, et ne peut pas défendre.

    Mot-clé maison du pack, sans équivalent dans le moteur : il se compose de
    deux règles déjà existantes.
    """
    return [
        *AbilityFactory.ThisNotCountAllyLimit(),
        *AbilityFactory.UnitCannotDefend(
            "This",
            None,
            cannot_trigger_defense_ability=True,
        ),
    ]
```

`ThisNotCountAllyLimit()` (`AbilityFactoryFriend`,
`game/ability/factory/friend.py`) écoute `Message.CheckIfAllyCountLimit` et
appelle `message.SetNotCountAlly(effect)` dès que l'allié vérifié est bien
« This » : c'est la règle générique derrière tout allié qui ne compte pas
dans la limite (le moteur ne connaît que cette fabrique, pas un concept
« Companion »).

`UnitCannotDefend("This", None, cannot_trigger_defense_ability=True)`
(`AbilityFactoryDoAttack`, `game/ability/factory/do_attack.py`) écoute
`Message.CheckIfUnitCanDefendAgainstAttack` et appelle
`message.SetCannotDefend(effect)`. Le deuxième paramètre positionnel
(`who_attacker`) est `None` : lu dans `Condition.CheckWhichCard`
(`game/ability/condition/card_type.py`, fonction interne
`invoke_check_card`), un `check_rule` à `None` renvoie toujours `True`,
donc la restriction ne porte que sur l'unité (« This »), pas sur
l'attaquant : Hairball ne peut défendre contre aucun ennemi, pas seulement
certains. `cannot_trigger_defense_ability=True` ajoute en plus
l'incapacité à déclencher une capacité de défense propre à la carte (pas
seulement l'action de défense de base) ; ce paramètre est aussi ce qui
distingue `UnitCannotDefend` de sa variante `UnitCannotMakeBasicDefense`
(même fichier), qui appelle `UnitCannotDefend` avec
`cannot_trigger_defense_ability=False` pour ne bloquer que la défense de
base.

**Carte exemple** : `lj021` (* Hairball), extrait de
`Fusion/marvel-lcg-src/src/cards/pack/lockjaw/lockjaw/lj021.py` :

```python
def GetAbilities() -> Sequence['Ability']:

    def amortir(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        message.PreventDamage(1, effect)

    return [
        *Companion(),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.Interrupt,
            Friend,
            amortir,
            is_from_attack=True,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
```

D'autres alliés du pack portent le même `*Companion()` en tête de leurs
capacités : Zabu (`lj018`), Throg (`lj019`), Redwing (`lj020`) et Lockheed
(`lj022`), tous confirmés par grep sur le dossier
`Fusion/marvel-lcg-src/src/cards/pack/lockjaw/lockjaw/`.

**Pièges connus** : aucun signalé au 29/08/2026.

**Variantes maison** : **Squirrel** (pack `squirrel_girl`, fonction
`Ecureuil()` dans
`Fusion/marvel-lcg-src/src/cards/pack/squirrel_girl/squirrel_girl/__init__.py`)
reprend le même montage `ThisNotCountAllyLimit()` +
`UnitCannotDefend("This", None, cannot_trigger_defense_ability=True)`, mais
n'est pas une simple copie augmentée d'une capacité de dépense : elle
ajoute aussi `AbilityFactory.UnitCannotHaveUpgradeAttached("This")` (l'allié
ne peut pas recevoir d'amélioration), la capacité de dépense étant portée
séparément par le reste du pack et non par `Ecureuil()` elle-même. Voir
`squirrel.md` pour le détail.
