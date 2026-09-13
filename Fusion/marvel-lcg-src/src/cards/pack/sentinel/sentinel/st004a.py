from . import *

# * Torso (Intact) — COMPONENT. INTACT. TECH.
# Permanent. Setup.
# Hero Action: Exhaust Torso (Intact) → heal 1 damage from Sentinel.
#
# Cartes de reference :
#  - `03007` Steve's Apartment : `this.HealthUnits(effect.targets, 1, effect)`
#    avec la cible declaree par `SetTarget("YourIdentity", canbe_heal=True)`.
#  - `av009` pour l'action de heros a inclinaison.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « heal 1 damage from **Sentinel** » : le NOM PROPRE de l'identite. Comme
#    c'est une action de HEROS, seule la face heros peut etre visee, et
#    « YourIdentity » suffit sans risquer le piege an002 (donner un effet aux
#    deux faces).
#  - `canbe_heal=True` : sans ce filtre, l'action resterait proposee alors que
#    Sentinel est indemne, et se resoudrait sans rien faire.


def GetAbilities() -> Sequence['Ability']:

    def reparer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        this.HealthUnits(effect.targets, 1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            reparer,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget("YourIdentity", canbe_heal=True),
    ]
