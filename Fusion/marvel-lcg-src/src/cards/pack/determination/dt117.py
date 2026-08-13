from . import *

# * The Behemoth

def GetAbilities() -> Sequence['Ability']:

    def the_behemoth(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        # « votre collection OU votre deck » : le moteur ne connait pas de
        # collection, la recherche se fait dans le deck et la defausse.
        initiator = effect.GetInitiator()
        face = Search.PlayerCard(effect, initiator,
                                 include_player_deck=True,
                                 include_discard_pile=True,
                                 may=True,
                                 finder=CardFinder(trait="S.H.I.E.L.D.", card_type=Ally))
        if face:
            face.CastTo(Ally).PutIntoPlay(initiator, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            the_behemoth
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'deploy'))
        .SetCostFunc(CostFunc.Discard(CardFinder(card_type=Ally),
                                      from_where=["YouControlCards"])),
    ]
