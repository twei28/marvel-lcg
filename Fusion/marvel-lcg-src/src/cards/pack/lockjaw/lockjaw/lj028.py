from . import *

# Companionship — custom « Nugget » (carte d'aspect BASIC)
# Action: Exhaust a PET AVENGER you control → choose a player. That player
#   draws 2 cards.


def GetAbilities() -> Sequence['Ability']:

    def piocher(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        for cible in effect.targets:
            joueur = cible.GetControlByPlayer()
            if joueur is not None:
                joueur.DrawUp(2, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            piocher,
        ).SetPlay()
        .SetCostFunc(CostFunc.Exhaust(
            trait="PET AVENGER",
            card_type=Ally,
            from_where=["YouControlCards"]))
        .SetTarget("Players"),
    ]
