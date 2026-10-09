from . import *

# hs223 Sting of the Scorpion (environnement du mode Hunter, scenario 2)
# Forced Response : apres la fin de la phase du vilain, le premier joueur choisit :
# 1 blessure sur J. Jonah Jameson, ou defausser le deck rencontre jusqu'a un
# attachement et le reveler.

def GetAbilities() -> Sequence['Ability']:

    def piquer(effect: 'Effect', message: 'Message.AfterPhaseEnd') -> None:
        from cards.pack.hunting_season.scorpion import PlacerUneBlessureSurJameson
        premier = Worlds.GetFirstPlayer(effect)
        jameson = Worlds.FindCardsOnField(effect, name="J. Jonah Jameson")

        def blessure(cibles: Sequence['CardFace']) -> None:
            PlacerUneBlessureSurJameson(effect)

        def attachement(cibles: Sequence['CardFace']) -> None:
            carte = Worlds.DiscardEncounterCardsUntil(effect, card_type=Attachment)
            if carte is not None:
                carte.Reveal(premier, effect)

        premier.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Place 1 wound counter on J. Jonah Jameson", blessure, condition=bool(jameson)),
            AbilityFactory.ForChoiceAbility("Discard until an attachment is discarded and reveal it", attachement),
        )

    return [
        AbilityFactory.AfterPhaseEnd(AbilityType.ForcedResponse, "Villain", piquer),
    ]
