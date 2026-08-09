from . import *

# Spellbound

def GetAbilities() -> Sequence['Ability']:

    def spellbound_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)

        def action(player: 'Player'):
            if player.GetIdentity().HasTrait("DEFIANT"):
                PlaceCharmCounter(player, 1, effect)
            if player.GetIdentity().HasTrait("ENTHRALLED"):
                player.DiscardControlCards(effect)

        Players.ForEachPlayer(effect, action)


    return [
        # CORRECTIF : le texte est un « When Revealed ». C'etait implemente en
        # WhenSchemeBeDefeated/WhenDefeated, donc l'effet partait quand les
        # joueurs DEJOUAIENT la manigance au lieu de sa REVELATION, ce qui
        # inversait completement l'economie de la carte.
        AbilityFactory.WhenThisRevealed(
            None,
            spellbound_revealed,
        ),
    ]

