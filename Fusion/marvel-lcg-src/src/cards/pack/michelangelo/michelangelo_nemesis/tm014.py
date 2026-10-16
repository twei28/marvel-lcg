from . import *

# Sewer Problems — manigance annexe nemesis. Crisis (icone), StartingThreat 4
# par heros, Boost 3 (3 icones).
# When Revealed: Each player discards the top 3 cards of their deck.
#
# Cartes de reference :
#  - `core/01149` Invasive AI : EXACTEMENT la meme phrase —
#    `Players.ForEachPlayer(effect, lambda p: p.DiscardDeckTopCards(3, effect))` ;
#  - Crisis : base automatique (desc), fiche mots-cles/crisis.md.
#
# ⚠ Mots-pieges :
#  - « EACH PLAYER » : tous les joueurs, pas seulement le premier.
#  - « the top 3 cards of THEIR deck » : le deck de chaque joueur, pas le deck
#    rencontre.
#  - L'icone CRISIS n'est pas ecrite dans le texte : c'est le glyphe central
#    (eclat avec « ! »), identique a 01108 Crowd Control (Crise 1), verifie
#    par decoupe (decision de l'utilisateur, 15/10/2026).

def GetAbilities() -> Sequence['Ability']:

    def sewer_problems(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this, message)

        def action(player: 'Player'):
            player.DiscardDeckTopCards(3, effect)

        Players.ForEachPlayer(effect, action)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            sewer_problems,
        ),
    ]
