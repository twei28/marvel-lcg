from . import *

# * Atilla (bandeau « ✦ Spider-Man ») — ALLIE 3 [physical], aspect Basic (TMNT Reskins, Inkwire). FROG. PUNK.
# Forced Response: After you play Atilla from your hand, choose THW or ATK. Atilla gets +2 to the chosen
#   power until the end of the phase.
#
# MODIFIEE de 13019 Spider-Man (Miles Morales) : le scan imprime « Forced Response » au lieu de
# « Response » (le bonus devient obligatoire). Script copie de 13019, type de capacite change.
# Carte de reference : 13019 (meme declencheur `AfterPlayerPlayedCard("You", "This")`, meme choix
# `AskChooseOneText`, meme `GainUntilPhaseEnd`).


def GetAbilities() -> Sequence['Ability']:

    def atilla(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Ally)

        initiator = effect.GetInitiator()
        text = initiator.AskChooseOneText(["THW", "ATK"])

        thwart = None
        attack = None
        if text == "THW":
            thwart = 2
        if text == "ATK":
            attack = 2

        this.GainUntilPhaseEnd(
            effect,
            attack=attack,
            thwart=thwart
        )

    return [
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.ForcedResponse,
            "You",
            "This",
            atilla
        ),
    ]
