from . import *

# Endgame (2A)
# When Revealed: Each player finds their nemesis minion and reveals it. Each
#   player whose nemesis minion did not enter play this way finds an UNDERLING
#   minion that is not in play and reveals it. In expert mode, the first player
#   finds and reveals the Organized Crime side scheme.
# Modeles : 01190 Shadow of the Past (nemesis par joueur), Find.FindAndReveal
# (if_no_entered_play : le sbire deja en jeu est « revele » sans entrer en jeu,
# un sbire retire du jeu n'est pas trouve : les deux menent a l'UNDERLING).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:

        def par_joueur(joueur: 'Player') -> None:
            entre = True

            def pas_entre() -> None:
                nonlocal entre
                entre = False

            sbire = Find.FindAndReveal(
                effect, joueur,
                finder=CardFinder(card_type=Minion, is_nemesis=joueur),
                if_no_entered_play=pas_entre,
            )
            if sbire is None or not entre:
                TrouverEtRevelerUnderling(effect, joueur)

        Players.ForEachPlayer(effect, par_joueur)
        if Worlds.IsExpert(effect):
            Find.FindAndReveal(effect, Worlds.GetFirstPlayer(effect),
                               name="Organized Crime", card_type=EncounterSideScheme)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
