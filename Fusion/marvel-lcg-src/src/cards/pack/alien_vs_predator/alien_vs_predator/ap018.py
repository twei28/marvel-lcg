from . import *

# Xenomorph Drone — SBIRE. XENOMORPH. SCH 0, ATK 2, PV 3. Boost 2. Deux exemplaires (18, 19).
# Guard. Incite 2 (3 instead if Alien Queen is the active villain).
# When Defeated: Remove 2 threat from Expanding Hive. If you cannot, shuffle Xenomorph Drone into the encounter deck.
#
# Cartes de reference :
#  - Guard, Incite 2 : `desc`, natifs (fiches guard.md, incite.md) ; « 3 instead if ... » : `ThisGainIncite(fn, incite=1)` (50094) ;
#  - « Remove X threat from <manigance> » : `RemoveThreatFromSchemes` ; « shuffle into the encounter deck » :
#    `Faces.ShuffleAllTo([..], "EncounterDeck")` (pd003, modele `WhenUnitBeDefeated(WhenDefeated, "This")`).
#
# ⚠ Mots-pieges :
#  - « If you CANNOT » : Expanding Hive absente (retiree au stade 3/4) ou sans menace ; une seule menace retiree compte comme « pu » ;
#  - le Drone (3 PV imprimes) est d'abord donne au mechant actif par Expanding Hive : il RESTE alors en boost, le melange n'a pas lieu
#    (arbitrage du 25/10/2026).


def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this
        Unused(message)
        hive = ManiganceDe(effect, REINE)
        if hive is not None and hive.threat > 0:
            this.RemoveThreatFromSchemes([hive], 2, effect)
            return
        if EncoreLibre(this):
            Faces.ShuffleAllTo([this], "EncounterDeck", effect)

    return [
        *AbilityFactory.ThisGainIncite(lambda effect: 1 if EstLeMechantActif(effect, REINE) else 0, incite=1),
        # NoOutOfPlayLimit : Expanding Hive (Interruption forcee) a peut-etre deja donne la carte en boost ; son « When Defeated » se
        # resout quand meme (arbitrage du 25/10/2026).
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu).NoOutOfPlayLimit(),
    ]
