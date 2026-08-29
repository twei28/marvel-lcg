from . import *

# Hack
# Interrupt (thwart): When threat would be placed on a scheme, discard Hack
#   → remove that amount from that scheme instead. Additionally, you may
#   discard 5 cards from your deck to remove the same amount from a
#   different scheme.
#
# Prevention + redirection : `message.SetBeInstead(effect)` puis retrait de
# `message.value` sur `message.trigger` (le plan vise), meme montage que
# Great Responsibility (core/01061.py), qui redirige en degats au lieu d'un
# retrait de menace. Retrait de menace : `this.RemoveThreatFromSchemes(...)`
# (modele : next_evol/cable/40013.py, Temporal Leap).

def GetAbilities() -> Sequence['Ability']:

    def hack(effect: 'Effect', message: 'Message.WhenSchemeWouldPlaceThreat') -> None:
        this = effect.this.CastTo(Upgrade)
        initiator = effect.GetInitiator()

        scheme = message.trigger.CastTo(Scheme2)
        value = message.value
        message.SetBeInstead(effect)
        if value > 0:
            this.RemoveThreatFromSchemes([scheme], value, effect)

        autres = [s for s in Worlds.FindCardsOnField(effect, card_type=Scheme2) if s is not scheme]
        if value > 0 and autres:
            choix = initiator.AskChooseOneText(
                ["No", "Yes"],
                text_list=[
                    "Do not remove more threat",
                    "Discard 5 cards from your deck to remove the same amount from a different scheme",
                ],
            )
            if choix == "Yes":
                initiator.DiscardDeckTopCards(5, effect)
                autre_scheme = initiator.AskChooseFace(autres, effect)
                if autre_scheme:
                    this.RemoveThreatFromSchemes([autre_scheme], value, effect)

    return [
        AbilityFactory.WhenThreatWouldBePlacedOn(
            AbilityType.Interrupt,
            None,
            hack,
        ).SetLabel('thwart')
        .SetCostFunc(CostFunc.Discard("This")),
    ]
