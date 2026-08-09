from . import *

# * J. Jonah Jameson — custom « Rainy »
# Alter-Ego Action: Exhaust J. Jonah Jameson -> draw 1 card. If that card had
#   a picture of Spider-Man on it, draw another card.
#
# « une carte avec une photo de Spider-Man » : lue comme « une carte du set
# signature Spider-Man (Rainy) autre que J. Jonah Jameson lui-meme » (toutes
# les autres cartes du set montrent Spider-Man sur leur illustration).

def GetAbilities() -> Sequence['Ability']:

    def jameson(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        initiator = effect.GetInitiator()
        piochees = initiator.DrawUp(1, effect)
        if piochees and any(
            getattr(x.paper, 'set_name', '') == "Spider-Man (Rainy)"
            and x.paper.card_id != "71009"
            for x in piochees
        ):
            initiator.DrawUp(1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            jameson
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
