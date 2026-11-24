from . import *

# Blessings of the Sun — EVENEMENT, cout 0, RES [mental], x2. DEFENSE.
# Hero Interrupt (defense): When you defend against an attack, place 1 solar counter on Sunspot -> for each solar counter
#   on Sunspot, you get +1 DEF for that attack.
#
# CARTES DE REFERENCE
#  - `14014` Never Back Down : `WhenUnitDefendAgainstAttack(HeroInterrupt, "You", op, is_basic_defense=True).SetPlay().SetLabel('defense')`
#    + `message.GainDEFForThisAttack(n, effect)`.
#
# TEXTE CONTRE CODE
#  ⚠ « place 1 solar counter -> for each solar counter on Sunspot » : le compteur est POSE d'abord, puis on compte TOUT le stock
#    (celui qu'on vient de poser compris) : stock 0 -> +1 DEF, stock 3 -> +4 DEF.


def GetAbilities() -> Sequence['Ability']:

    def blessings_of_the_sun(effect: 'Effect', message: 'Message.WhenUnitWouldDefend') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        joueur = effect.GetInitiator()
        PoserSolaires(joueur, 1, effect)
        message.GainDEFForThisAttack(SolairesDe(joueur), effect)

    return [
        AbilityFactory.WhenUnitDefendAgainstAttack(
            AbilityType.HeroInterrupt,
            "You",
            blessings_of_the_sun,
            is_basic_defense=True,
        ).SetPlay().SetLabel('defense'),
    ]
