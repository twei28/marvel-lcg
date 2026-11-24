from . import *

# * Rachel Summers — ALTER EGO. REC 4, HS 5, PV 10. MUTANT. PSIONIC.
# Telepathic Trickery — Action: Exhaust Rachel Summers -> Search your deck for a copy of Temporal Reversal and add it to
# your hand.
#
# CARTES DE REFERENCE : `48001b` Kurt Wagner (`Search.PlayerCard(.., include_player_deck=True, name=..)` +
# `Faces.AddToHand`) ; l'inclinaison en cout : `CostFunc.Exhaust("This")` (`14007`).
#
# MOTS-PIEGES : « a COPY of » = le nom exact, `rm007`. « Search your deck » : le deck seulement (pas la defausse).
def GetAbilities() -> Sequence['Ability']:
    def telepathic_trickery(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)
        initiator = effect.GetInitiator()
        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            name="Temporal Reversal",
        )
        if face:
            Faces.AddToHand([face], initiator, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            telepathic_trickery,
        ).SetName("Telepathic Trickery")
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
