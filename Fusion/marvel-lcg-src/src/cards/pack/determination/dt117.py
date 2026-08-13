from . import *

# * The Behemoth

def GetAbilities() -> Sequence['Ability']:

    def the_behemoth(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        # « votre collection ou votre deck » : la collection d'abord, puisque
        # `Search.Collection` la couvre entierement (elle lit la base du jeu).
        initiator = effect.GetInitiator()
        face = Search.Collection(effect, initiator,
                                 trait="S.H.I.E.L.D.", card_type=Ally,
                                 card_classes="Any")
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
