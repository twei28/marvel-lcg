from . import *

# * Black Cat

def GetAbilities() -> Sequence['Ability']:

    def chat_noir(effect: 'Effect', joueur: 'Player') -> None:
        # « [star] Forced Response: After Black Cat engages you or schemes,
        # discard the top 2 cards of the encounter deck. Deal each card with a
        # star icon ([star]) discarded this way to yourself as a facedown
        # encounter card. »
        defaussees = Worlds.DiscardEncounterCards(2, effect)
        etoilees = [x for x in defaussees
                    if HasBoostIcon.IsType(x) and x.boost_star > 0]
        for carte in etoilees:
            joueur.DealEncounterCard(carte, effect)

    def engagement(effect: 'Effect', message: 'Message.AfterMinionEngagePlayer') -> None:
        chat_noir(effect, message.GetToPlayer())

    def complot(effect: 'Effect', message: 'Message.AfterUnitSchemeEnd') -> None:
        chat_noir(effect, message.GetToPlayer())

    return [
        AbilityFactory.AfterMinionEngagePlayer(
            AbilityType.ForcedResponse,
            "This",
            None,
            engagement
        ),
        AbilityFactory.AfterUnitSchemeEnd(
            AbilityType.ForcedResponse,
            "This",
            complot
        ),
    ]
