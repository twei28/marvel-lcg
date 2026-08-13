from . import *

# * Human Torch

def GetAbilities() -> Sequence['Ability']:

    def human_torch(effect: 'Effect', message: 'Message.AfterPlayerTurnBegin') -> None:
        this = effect.this.CastTo(Ally)

        player = this.GetControlByPlayer()
        if player is None:
            return

        cibles: List['CardFace'] = []
        villain = Worlds.FindVillain(effect)
        if villain:
            cibles.append(villain)
        cibles += [x for x in Worlds.FindCardsOnField(effect, card_type=Minion,
                                                      engaged_with=player)
                   if not x.IsDefeated()]
        cibles.append(player.GetHero())
        cibles += [a for a in player.GetAllies() if a != this]
        if cibles:
            this.DealDamage(cibles, 1, effect)

    return [
        AbilityFactory.AfterPlayerTurnBegin(
            AbilityType.ForcedResponse,
            "You",
            human_torch
        ),
    ]
