from . import *

# Emma Frost, face A1 (standard, face ACTIVE, 7 PV par joueur). « [star] Forced Response : After Emma Frost activates, discard 1 card from the top of the
# encounter deck, if it has the PSIONIC trait, place 1 threat on each scheme. Forced Interrupt : When Emma Frost would be defeated, remove 5 threat from
# each scheme in play, and flip this card instead. »
# Cartes de reference : 16080a Collector (`WhenUnitWouldBeDefeated` + `SetBeInstead` + `RemoveThreatFromSchemes` + `card.Flip`), 02030 / hf101a (carte
# defaussee lue par `Worlds.DiscardEncounterTopCard`), `AfterEnemyActivationEnd` (activate.py).
# ⚠ « each scheme » = la manigance PRINCIPALE et les manigances ANNEXES (`"EachScheme"`), pas seulement les annexes (le livret resume « chaque complot »).
# ⚠ « after Emma Frost activates » : apres CHAQUE activation (attaque contre un heros, complot contre un alter-ego), une fois par joueur.


def GetAbilities() -> Sequence['Ability']:
    def apres_activation(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        face = Worlds.DiscardEncounterTopCard(effect)
        if face is not None and face.HasTrait(PSIONIQUE):
            MenaceSurChaqueManigance(effect, 1)

    return [
        AbilityFactory.AfterEnemyActivationEnd(AbilityType.ForcedResponse, "This", apres_activation),
        InterruptionDefaiteEmma(),
    ]
