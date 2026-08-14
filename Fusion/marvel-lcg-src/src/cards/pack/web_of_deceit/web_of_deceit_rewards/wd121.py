from . import *

# * Master Weaver

def GetAbilities() -> Sequence['Ability']:

    def entree_dun_allie(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        # « Response: After a WEB-WARRIOR ally enters play, tuck the top card of
        # the encounter deck under that ally. »
        allie = message.trigger
        carte = Worlds.GetEncounterDeck(effect).GetTop()
        if carte:
            allie.TuckCardUnderHere(carte, effect)

    def icones_glissees(effect: 'Effect', face: 'CardFace') -> int:
        # « Each WEB-WARRIOR ally gets +1 hit point for each boost icon tucked
        # under them. » Le compte est PAR ALLIE : chacun ne gagne que ce qu'il
        # porte, d'ou la lecture de sa propre zone.
        total = 0
        for carte in face.GetPlacedCardArea().Get():
            if HasBoostIcon.IsType(carte):
                total += carte.printed_boost
        return total

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(trait="WEB-WARRIOR", card_type=Ally),
            control_by="You",
            get_new_value=icones_glissees,
            health=1,
            change_on_event=OnEvent.PlacedCard(None),
        ),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            CardFinder(trait="WEB-WARRIOR", card_type=Ally),
            entree_dun_allie
        ),
    ]
