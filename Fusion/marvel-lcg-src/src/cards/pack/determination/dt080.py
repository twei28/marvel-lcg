from . import *

# * Masacre

def GetAbilities() -> Sequence['Ability']:

    def chercher_merc_squad(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        initiator = effect.GetInitiator()
        face = Search.PlayerCard(effect, initiator,
                                 include_player_deck=True,
                                 include_discard_pile=True,
                                 may=True,
                                 name="Merc Squad")
        if face:
            face.CastTo(Support).PutIntoPlay(initiator, effect)

    def poser_les_tactiques(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)

        player = this.GetControlByPlayer()
        if player is None:
            return
        squads = [f for f in player.GetControlCards() if f.paper.name == "Merc Squad"]
        if squads:
            Faces.PlaceCountersOn(squads, 1, 'tactic', effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.HeroResponse,
            "This",
            chercher_merc_squad
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            poser_les_tactiques
        ).LimitOncePerRound()
        .SetCostFunc(CostFunc.DealDamage(1, "This")),
    ]
