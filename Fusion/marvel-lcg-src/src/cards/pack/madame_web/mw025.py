from . import *

# * Spider-Woman: Mattie Franklin — custom « Kajislav », carte d'aspect BASIC
# Forced Interrupt: When Spider-Woman enters your hand, pay her printed cost ->
#   put Spider-Woman into play under your control. If you cannot, discard
#   Spider-Woman.
#
# Le moteur n'expose qu'un `AfterCardEnterHand` (pas d'interruption sur l'entree
# en main) : la capacite se declenche donc juste apres l'arrivee en main.

def GetAbilities() -> Sequence['Ability']:

    def mattie_franklin(effect: 'Effect', message: 'Message.AfterCardEnterHand') -> None:
        this = effect.this.CastTo(Ally)

        player = effect.GetInitiator()

        if player.PayCardPrintCost(this, effect) != None:
            this.PutIntoPlay(player, effect, under_control=True)
        else:
            Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.AfterCardEnterHand(
            AbilityType.ForcedResponse,
            "This",
            mattie_franklin
        ),
    ]
