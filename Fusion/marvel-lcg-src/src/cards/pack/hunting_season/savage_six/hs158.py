from . import *

# hs158 * Vulture
# [star] Forced Response : apres que Vulture vous attaque, distribuez-vous une carte de rencontre, puis melangez Vulture
# dans le paquet de rencontre. Boost : apres l'activation, melangez cette carte dans le paquet de rencontre.

def GetAbilities() -> Sequence['Ability']:

    def fuir(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        joueur = message.GetAgainstPlayer()
        joueur.DealEncounterCards(1, effect)
        Faces.ShuffleAllTo([effect.this], Worlds.GetEncounterDeck(effect), effect)

    return [
        AbilityFactory.AfterUnitAttackEnd(AbilityType.ForcedResponse, "This", fuir, against_who="You"),
        AbilityFactory.WhenBoostShuffleThisIntoEncounterDeckAfterActivationEnd(),
    ]
