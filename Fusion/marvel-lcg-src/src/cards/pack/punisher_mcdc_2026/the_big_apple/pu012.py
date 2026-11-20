from . import *

# * Black Tarantula — SBIRE UNIQUE. CRIMINAL. MARTIAL ARTIST. SCH 2, ATQ 2, 4 PV, Boost 1.
# If the total number of LEAD cards in the victory display is at least:
#   • 1[per hero] — This minion gains quickstrike.
#   • 2[per hero] — This minion gets +3 hit points.
#
# Cartes de reference : galactic_storm/supreme_intelligence/gs204.py (`ThisGainKeyword(fn, ..., change_on_event=OnEvent.Victory(...))` : un bonus qui
# suit le contenu de la pile de victoire), fiche quickstrike.md.
# ⚠ « at least 1[per hero] » : 1 x joueurs ; « at least 2[per hero] » : 2 x joueurs ; LES DEUX paliers se cumulent (quickstrike ET +3 PV a 2 par joueur).

def GetAbilities() -> Sequence['Ability']:

    def au_moins(n_par_joueur: int) -> 'Callable[[Effect, List[CardFace]], int]':
        def condition(effect: 'Effect', ui: 'List[CardFace]') -> int:
            return 1 if len(PistesEnVictoire(effect)) >= n_par_joueur * Worlds.GetPlayerNum(effect) else 0
        return condition

    return [
        AbilityFactory.ThisGainKeyword(au_moins(1), quickstrike=1, change_on_event=OnEvent.Victory(CardFinder(trait="LEAD"))),
        AbilityFactory.ThisGainKeyword(au_moins(2), health=3, change_on_event=OnEvent.Victory(CardFinder(trait="LEAD"))),
    ]
