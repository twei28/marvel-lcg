from . import *

# * Annihilus — custom « Nugget » (némésis de Lockjaw)
# Forced Interrupt: When Annihilus would be defeated, shuffle him into the
#   encounter deck instead.
# [star] Boost: After this activation ends, shuffle this card into the
#   encounter deck.


def GetAbilities() -> Sequence['Ability']:

    def survit(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        message.SetBeInstead(effect)
        Faces.ShuffleAllTo([this], "EncounterDeck", effect)

    return [
        AbilityFactory.WhenUnitWouldBeDefeated(
            AbilityType.ForcedInterrupt,
            "This",
            survit,
        ),
        # CORRECTIF 4/8/2026 : le handler appelait
        # `ShuffleThisCardIntoEncounterDeckAfterActivation`, qui n'existe pas,
        # sous une garde `in globals()`. La branche etait donc morte et le repli
        # melangeait la carte IMMEDIATEMENT au lieu d'attendre la fin de
        # l'activation. Le moteur a la fabrique exacte, employee par Monster
        # 02025.
        AbilityFactory.WhenBoostShuffleThisIntoEncounterDeckAfterActivationEnd(),
    ]
