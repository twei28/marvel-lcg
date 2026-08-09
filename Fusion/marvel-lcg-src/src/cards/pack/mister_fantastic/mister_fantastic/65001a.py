from . import *

# * Mister Fantastic — custom « DesignHacker »
# Flexibility — Response: After you spend a SUPERPOWER card as a resource or
# discard it from your hand without being played, return it to your hand.
# (Limit once per phase.)
#
# LENIENT : dépenser une carte comme ressource et la défausser de la main
# aboutissent au même message moteur (mise à la défausse). Le déclencheur
# couvre donc les deux cas d'un coup, mais il ne distingue pas la défausse
# d'une carte SUPERPOWER qui était en jeu.

def GetAbilities() -> Sequence['Ability']:

    def flexibility(effect: 'Effect', message: 'Message.AfterCardDiscard') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this)

        initiator = effect.GetInitiator()
        face = message.trigger
        if face is None:
            return
        initiator.GainCard(face, effect)

    return [
        AbilityFactory.AfterCardDiscard(
            AbilityType.Response,
            CardFinder(trait="SUPERPOWER"),
            flexibility,
            control_by_player="You",
        ).SetName("Flexibility")
        .LimitOncePerPhase(),
    ]
