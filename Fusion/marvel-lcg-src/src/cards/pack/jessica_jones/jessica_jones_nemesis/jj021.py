from . import *

# The Purple Children — custom « ekAugust »
# Incite 1 (incite 2 instead, if Purple Man is in play).
# When Revealed: Place 2 threat on each side scheme in play. If there are no
#   side schemes in play, you are confused.
#
# `Incite: 1` est imprime dans cards.json ; le +1 conditionnel est ajoute ici.

def GetAbilities() -> Sequence['Ability']:

    def purple_children(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        manigances = Worlds.GetSideSchemes(effect)
        if manigances:
            for manigance in manigances:
                this.PlaceThreatOnSchemes([manigance], 2, effect)
        else:
            identity = message.GetToPlayer().GetIdentity()
            Faces.GiveStatus([identity], "Confused", effect)

    return [
        *AbilityFactory.ThisGainIncite(
            lambda effect:
                Worlds.FindCardOnField(effect, name="Purple Man") != None,
            incite=1,
            change_on_event=OnEvent.CardInPlay(CardFinder(name="Purple Man")),
        ),

        AbilityFactory.WhenThisRevealed(
            None,
            purple_children,
        ),
    ]
