from . import *

# Pay the Price (2/2) — contenu identique a il021, voir ce fichier pour le
# detail du modele repris (5/5).

def GetAbilities() -> Sequence['Ability']:

    def pay_the_price(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        player = message.GetToPlayer()
        discarded = player.DiscardDeckTopCards(8, effect)
        if len(discarded) < 8:
            ThisCardGainSurge(effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            pay_the_price,
        ),
    ]
