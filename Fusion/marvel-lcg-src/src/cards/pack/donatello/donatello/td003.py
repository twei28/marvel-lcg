from . import *

# Bō Tobu — EVENEMENT, cout 1, [mental]. DEFENSE. THWART. x2 (td003).
# Hero Interrupt (defense/thwart): When you would take damage from an attack,
#   prevent 3 of that damage and remove 3 threat from a scheme.
#
# CARTES DE REFERENCE
#  - `si012` Spectacular Save (superior_iron_man) : « Hero Interrupt
#    (defense/thwart) » = `WhenUnitWouldTakeDamage(HeroInterrupt, ...) +
#    SetPlay().SetLabel('defense', 'thwart') + SetTarget(Scheme2,
#    has_threat=True)`, `message.PreventDamage(3, effect)` puis
#    `this.RemoveThreatFromSchemes(effect.targets, n, effect)`.
#  - `br004` Hammer Twirl : `is_from_attack=True` pour « from an attack ».
#
# TEXTE CONTRE CODE
#  « When YOU would take damage » -> "You" (identite, pas un allie).
#  « from AN ATTACK » -> `is_from_attack=True` (pas les degats de carte).
#  « prevent 3 OF THAT damage » -> `PreventDamage(3)` : prevenir au plus 3, pas
#    tout. « and remove 3 threat from A scheme » -> UNE manigance au choix.
#  Les deux copies du scan portent un titre different (« Bō Tobu » avec
#  macron / « Bo Tobu ») pour un texte et des icones identiques : UN seul
#  card_id, deux exemplaires. Voir la question Q-TD-03 du rapport.


def GetAbilities() -> Sequence['Ability']:

    def bo_tobu(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        message.PreventDamage(3, effect)
        this.RemoveThreatFromSchemes(effect.targets, 3, effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            bo_tobu,
            is_from_attack=True,
        ).SetPlay().SetLabel('defense', 'thwart')
        .SetTarget(Scheme2, has_threat=True),
    ]
