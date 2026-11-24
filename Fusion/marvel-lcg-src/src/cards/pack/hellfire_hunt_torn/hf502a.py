from . import *

# Emma Frost, face B1 (expert, face ACTIVE, 8 PV par joueur). « [star] Forced Response : After Emma Frost activates, discard 2 cards from the top of the
# encounter deck, for each PSIONIC card discarded in this way, place 1 threat on each scheme. Forced Interrupt : When Emma Frost would be defeated, remove
# 5 threat from each scheme in play, and flip this card instead. »
# Cartes de reference : hf501a (meme famille), `Worlds.DiscardEncounterCards(2, effect)` rend les cartes defaussees.


def GetAbilities() -> Sequence['Ability']:
    def apres_activation(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        faces = Worlds.DiscardEncounterCards(2, effect)
        for face in faces:
            if face.HasTrait(PSIONIQUE):
                MenaceSurChaqueManigance(effect, 1)

    return [
        AbilityFactory.AfterEnemyActivationEnd(AbilityType.ForcedResponse, "This", apres_activation),
        InterruptionDefaiteEmma(),
    ]
