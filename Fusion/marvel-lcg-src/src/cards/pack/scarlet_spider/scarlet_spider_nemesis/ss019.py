from . import *

# * Bella Donna — sbire nemesis de Scarlet Spider. ASSASSIN. ELITE.
# Plotting. (After this minion engages your identity, it schemes.)
# Forced Interrupt: When Bella Donna is defeated, search the encounter deck
#   for another [[ASSASSIN]] minion and reveal it.
#
# ELITE : trait purement declaratif, aucun code (precedent ok021, deja
# porteur du meme trait sans rien coder). Plotting : voir mots-cles/
# plotting.md, `AbilityFactory.AfterMinionEngagePlayer(ForcedResponse,
# "This", "You", ...)` + `this.CastTo(Minion).BasicSchemes(effect)` (modele
# ok021 Malice pour BasicSchemes, declencheur different mais meme brique).
# "Search the encounter deck for another [[ASSASSIN]] minion and reveal it"
# : modele core/ultron/01143.py (Advanced Ultron Drone, `AbilityFactory.
# WhenUnitBeDefeated(ForcedInterrupt, "This", ...)`, la carte est encore
# manipulable a ce point) + core/spider_man_nemesis/01095.py (Rhino,
# `Search.EncounterCard(...) puis face.Reveal(None, effect)`).


def GetAbilities() -> Sequence['Ability']:

    def plotting(effect: 'Effect', message: 'Message.AfterMinionEngagePlayer') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)

        this.BasicSchemes(effect)

    def bella_donna_defeated(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this, message)

        face = Search.EncounterCard(
            effect,
            include_discard_pile=False,
            trait="ASSASSIN",
            card_type=Minion,
        )
        if face:
            face.Reveal(None, effect)

    return [
        AbilityFactory.AfterMinionEngagePlayer(
            AbilityType.ForcedResponse,
            "This",
            "You",
            plotting,
        ).SetName("Plotting"),
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.ForcedInterrupt,
            "This",
            bella_donna_defeated,
        ),
    ]
