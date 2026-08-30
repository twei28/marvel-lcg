from . import *

# * Hellcow — sbire nemesis ALTERNATIF, ELITE. VAMPIRE — 6 PV, SCH 1, ATK 2
# Quickstrike.
# Forced Interrupt: When the villain phase begins, heal 1 damage from Hellcow.
# Interrupt: When Hellcow would be defeated, shuffle her into the encounter
#   deck instead.
#
# Carte HORS du `nemesis_set` standard : sbire alternatif a utiliser A LA
# PLACE du Collector (hd023) quand on affronte le scenario du Collector, qui
# est un vilain officiel du pack `gmw` (16070-16081). Voir le __init__.py du
# set. Elle est neanmoins scriptee et testee comme n'importe quelle carte.
#
# « Quickstrike » est un mot-cle AUTOMATIQUE lu dans `desc.Quickstrike` :
# aucun code (precedent ss020 Harvester, qui le porte sans rien coder).
#
# « When the VILLAIN PHASE BEGINS » : `AbilityFactory.WhenPhaseBegin(
# AbilityType.ForcedInterrupt, "Villain", ...)` (turn_phase.py:129), modele
# exact determination/dt078.py (Cumbersome Enhancements). Soin sur SOI-MEME :
# `this.HealthUnits([this], 1, effect)` (modele albert/ab012.py, meme
# formule mot pour mot).
#
# « When Hellcow WOULD BE DEFEATED, shuffle her into the encounter deck
# INSTEAD » : modele EXACT ss021 (Undead Hand Ninja) et lj015 (Annihilus),
# `AbilityFactory.WhenUnitWouldBeDefeated(<type>, "This", ...)` +
# `message.SetBeInstead(effect)` + `Faces.ShuffleAllTo([this],
# "EncounterDeck", effect)`. Le piege `instead` du tableau est respecte : la
# defaite n'a jamais lieu, la carte PART du terrain et ARRIVE dans le deck,
# elle n'est pas dupliquee. Seule difference avec ss021 : le texte imprime dit
# « Interrupt » et non « Forced Interrupt », donc `AbilityType.Interrupt`.


def GetAbilities() -> Sequence['Ability']:

    def se_soigne(effect: 'Effect', message: 'Message.WhenPhaseBegin') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)

        this.HealthUnits([this], 1, effect)

    def survit(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(Minion)

        message.SetBeInstead(effect)
        Faces.ShuffleAllTo([this], "EncounterDeck", effect)

    return [
        AbilityFactory.WhenPhaseBegin(
            AbilityType.ForcedInterrupt,
            "Villain",
            se_soigne,
        ),
        AbilityFactory.WhenUnitWouldBeDefeated(
            AbilityType.Interrupt,
            "This",
            survit,
        ),
    ]
