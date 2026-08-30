from . import *

# * Undead Hand Ninja — sbire ASSASSIN.
# Incite 1.
# Forced Interrupt: When this minion would be defeated, shuffle it back
#   into the encounter deck instead.
# [star] Boost: Reveal this card.
#
# Incite 1 : mot-cle purement declaratif (`desc.Incite`, deja dans
# cards.json), aucun code. "Would be defeated ... instead" : modele
# fan-made exact lj015 (* Annihilus, pack lockjaw), `AbilityFactory.
# WhenUnitWouldBeDefeated(ForcedInterrupt, "This", ...)` +
# `message.SetBeInstead(effect)` + `Faces.ShuffleAllTo([this],
# "EncounterDeck", effect)`. Boost "Reveal this card" : helper
# `RevealThisCard` (modele mut_gen/colossus_nemesis/32029.py Slammed).


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
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            RevealThisCard,
        ),
    ]
