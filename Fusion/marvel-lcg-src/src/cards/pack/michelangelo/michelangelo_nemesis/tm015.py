from . import *

# * Wyrm — sbire nemesis. WORMS! SCH 1 / ATQ 3 / PV 3 / Boost 2. Toughness.
# When Defeated: Shuffle Wyrm into the encounter deck.
# (Michelangelo's nemesis minion.)
#
# Cartes de reference :
#  - `ab016` Zombie Wolvie et `aos/50098` Machete : EXACTEMENT la meme phrase,
#    `WhenUnitBeDefeated(WhenDefeated, "This", op)` +
#    `Faces.ShuffleAllTo([this], "EncounterDeck", effect)` ;
#  - Toughness : base automatique (desc), fiche mots-cles/toughness.md ;
#  - sbire nemesis : `desc.Nemesis` = nom du heros (ls014).
#
# ⚠ Mots-pieges :
#  - « Shuffle Wyrm INTO the encounter deck » : remelange, pas defausse.
#  - Le trait imprime « WORMS! » est ecrit « WORMS » (sans ponctuation).

def GetAbilities() -> Sequence['Ability']:

    def wyrm(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)

        Faces.ShuffleAllTo([this], "EncounterDeck", effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            wyrm,
        ),
    ]
