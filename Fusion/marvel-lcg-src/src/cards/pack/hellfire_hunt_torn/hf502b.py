from . import *

# Emma Frost, face B2 (expert, face RETOURNEE, PV infinis). « [star] Forced Interrupt : When Emma Frost activates against a player, give the player a
# facedown encounter card instead. Forced Response : After the end of the villain phase, flip this card, then set Emma Frost's hit point dial to her printed
# hit points. »
# Cartes de reference : hf501b (meme famille), sl037 (`message.to_player` : l'activation est CONTRE un joueur), `joueur.DealEncounterCards`.


def GetAbilities() -> Sequence['Ability']:
    def avant_activation(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> None:
        joueur = message.to_player
        if joueur is None:
            return
        message.SetBeInstead(effect)
        joueur.DealEncounterCards(1, effect)

    return [
        AbilityFactory.WhenEnemyWouldActivate(AbilityType.ForcedInterrupt, "This", avant_activation),
        RetourSurLaFaceActive(),
    ]
