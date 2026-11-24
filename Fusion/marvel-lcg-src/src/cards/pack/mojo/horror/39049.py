from . import *

# Cultist

def GetAbilities() -> Sequence['Ability']:

    def cultist(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)

        player = message.GetAgainstPlayer()

        face = Search.EncounterCard(
            effect,
            include_discard_pile=True,
            name="The Kraken",
            card_type=Minion,
        )

        if face:
            face.PutIntoPlay(player, effect)
            Faces.DiscardAll([this], effect)
        else:
            # RR « Then » : sans The Kraken a mettre en jeu, « Then, discard Cultist » ne se resout pas ; le joueur doit le savoir
            # (decision de l'utilisateur du 26/10/2026, meme avis que Safe House #30).
            player.NotifyNoResult(this, "The Kraken was not found: Cultist is not discarded.")


    return [
        AbilityFactory.AfterEnemyActivatesAgainstYou(
            AbilityType.ForcedResponse,
            "This",
            cultist,
        ),
    ]

