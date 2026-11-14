from . import *
# * Marvel Girl: Rachel Summers (Aggression, allie 3 [mental], THW 2** ATK 2*, PV 3). PSIONIC. STARJAMMER. X-MEN.
# Interrupt: When Marvel Girl attacks, choose one: • That attack gains piercing. • That attack gains ranged. • That attack gains overkill.
#
# Cartes de reference : 16019 Rocket Raccoon (`WhenUnitWouldAttack...(Interrupt, "This", op)` + `message.GainOverKill(effect)`) ; 16046
# Hand Cannon (`message.GainOverKill`) ; `message.GainPiercing` / `GainRanged` (do_attack.py, memes methodes) ; RECETTES §2 (choix
# `ChooseAbilities(ForChoiceAbility(...).SetHasNoTargetEffect())`).
# « When Marvel Girl attacks » : toute attaque (de base ou par une carte), contre n'importe quel ennemi. UN SEUL mot-cle a la fois.
def GetAbilities() -> Sequence['Ability']:
    def marvel_girl(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        joueur = JoueurDe(effect)
        if joueur is None:
            return
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("That attack gains piercing", lambda targets: message.GainPiercing(effect))
            .SetHasNoTargetEffect(),
            AbilityFactory.ForChoiceAbility("That attack gains ranged", lambda targets: message.GainRanged(effect))
            .SetHasNoTargetEffect(),
            AbilityFactory.ForChoiceAbility("That attack gains overkill", lambda targets: message.GainOverKill(effect))
            .SetHasNoTargetEffect(),
        )
    return [
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.Interrupt,
            "This",
            marvel_girl,
        ),
    ]
