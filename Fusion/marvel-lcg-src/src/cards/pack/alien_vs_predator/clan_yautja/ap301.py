from . import *

# * Yautja Young Blood — SBIRE unique. YAUTJA. SCH 1, ATK 1, PV 4. Boost 1.
# Patrol. Incite 2 (3 instead if Predator Warlord is the active villain).
# When Defeated: Place 2 threat on The Ultimate Hunt, if you cannot shuffle Yautja Young Blood into the encounter deck.
#
# Cartes de reference : Patrol, Incite natifs (`desc`) ; « 3 instead if ... » : `ThisGainIncite` (50094, comme ap018) ; « shuffle into the
#   encounter deck » : `Faces.ShuffleAllTo(.., "EncounterDeck")` (pd003).
#
# ⚠ Mots-pieges :
#  - « The Ultimate Hunt » = le complot du stade 1 (par son NOM) : aux stades 2 a 4 on ne peut pas -> melange ;
#  - 4 PV imprimes : Expanding Hive le donne d'abord comme boost, il y RESTE (arbitrage du 25/10/2026).


def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this
        Unused(message)
        complot = LeComplot(effect)
        if complot is not None and complot.IsName(ULTIMATE_HUNT):
            this.PlaceThreatOnSchemes([complot], 2, effect)
        elif EncoreLibre(this):
            Faces.ShuffleAllTo([this], "EncounterDeck", effect)

    return [
        *AbilityFactory.ThisGainIncite(lambda effect: 1 if EstLeMechantActif(effect, WARLORD) else 0, incite=1),
        # NoOutOfPlayLimit : Expanding Hive a peut-etre deja donne la carte en boost ; son « When Defeated » se resout quand meme.
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu).NoOutOfPlayLimit(),
    ]
