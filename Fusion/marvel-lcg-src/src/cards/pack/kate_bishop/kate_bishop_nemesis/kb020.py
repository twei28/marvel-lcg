from . import *

# Golden Shot (2/2) — trahison nemesis de Hawkeye (Kate Bishop)
# Exemplaire physique 2 de 2, contenu identique a kb019 (voir ce fichier pour
# le detail du modele repris).


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
