from . import *

# "I've Got Everyone" — custom « ekAugust »
# When Revealed: Deal X indirect damage among players (divided as you choose),
#   where X is equal to the number of side schemes in play. Confuse each
#   character damaged this way. If there are no side schemes in play, this card
#   gains surge.

def GetAbilities() -> Sequence['Ability']:

    def ive_got_everyone(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        value = len(Worlds.GetSideSchemes(effect))
        if not value:
            this.GainSurge(1, effect)
            return

        player = message.GetToPlayer()
        cibles = Worlds.GetOnFieldFriendlyCharacters(effect)
        blesses = player.AssignDamage(cibles, this, value, effect)
        if blesses:
            Faces.GiveStatus(blesses, "Confused", effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            ive_got_everyone,
        ),
    ]
