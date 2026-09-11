from . import *
# Helluva Punch — EVENEMENT, cout 2, [mental]. ATTACK. x3.
# Hero Action (attack): Deal 4 damage to an enemy. If you paid for this using
#   only [mental] resources, deal an additional 2 damage to that enemy, and this
#   attack gains overkill.
#
# Modele exact : dd004 This World Is Mine (`OnlyHasColor("B")` +
# `AttackProperty(overkill=...)`). « an additional 2 » : 6 en tout, un seul
# appel, pour que le deferlement porte sur la totalite.

def GetAbilities() -> Sequence['Ability']:

    def helluva_punch(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        joueur = effect.GetInitiator()
        heroine = joueur.GetHero() if joueur else None
        if heroine is None:
            return
        mental = PayeSeulementEnMental(effect)
        heroine.DealDamage(
            effect.targets, 6 if mental else 4, effect,
            property=AttackProperty(overkill=mental),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            helluva_punch,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
