from . import *

# Dazzler's Rollerskates
# ITEM.
# Hero Action: Exhaust Dazzler's Rollerskates -> ready Dazzler.
#
# On cible « YourIdentity » plutot que `name="Dazzler"` : c'est une Hero
# Action, donc l'identite est forcement le heros, et le ciblage par nom n'est
# pas borne au joueur dans ce moteur.


def GetAbilities() -> Sequence['Ability']:

    def patins(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        Faces.ReadyAll(effect.targets, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            patins,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget("YourIdentity", canbe_ready=True),
    ]
