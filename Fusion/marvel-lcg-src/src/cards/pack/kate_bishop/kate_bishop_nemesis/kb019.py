from . import *

# Golden Shot (1/2) — trahison nemesis de Hawkeye (Kate Bishop)
# When Revealed: Take 1 damage. Then, take 1 indirect damage for each
#   friendly character you control.
# [star] Boost: Reveal this card.
#
# Exemplaire physique 1 de 2 (kb019, kb020) : meme carte imprimee deux fois
# dans le set nemesis (4/5 et 5/5), donc deux card_id distincts au contenu
# identique -- pas une erreur de copier-coller. « friendly character you
# control » = identite + allies : `player.GetControlCharacters()`
# (player_get.py:91).


def GetAbilities() -> Sequence['Ability']:

    def golden_shot(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        player = message.GetToPlayer()
        identity = player.GetIdentity()

        identity.TakeDamage(this, 1, effect)
        nb = len(player.GetControlCharacters())
        if nb:
            identity.TakeIndirectDamage(this, nb, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            golden_shot,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            RevealThisCard,
        ),
    ]
