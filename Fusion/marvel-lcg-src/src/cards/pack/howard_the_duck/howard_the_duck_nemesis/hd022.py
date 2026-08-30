from . import *

# Duck and Cover! — manigance annexe nemesis, menace 2*, Boost 3, HAZARD 1
# When Revealed: Each player must discard cards with a printed [mental] from
#   their hand. Place 1 additional threat here for each card discarded this
#   way.
#
# HAZARD est un mot-cle AUTOMATIQUE lu dans `desc.Hazard` (has_hazard.py) :
# aucun code. L'icone imprimee a ete verifiee par decoupe d'image (carte
# penchee NUE, sans barre de soulignement, temoin `ag011`) — voir l'encadre de
# `docs/reference/mots-cles/hazard.md`. Ne pas la confondre avec l'icone
# ACCELERATION de hd026.
#
# « discard cards with a printed [mental] from their hand » : modele exact
# core/captain_marvel_nemesis/01179.py (Yon-Rogg's Treason),
# `player.hand_cards.FindCards(has_printed_res=<lettre>)` + `Faces.DiscardAll`.
# `has_printed_res` ne convertit PAS le wild (`convert_green_res = False`,
# finder.py:102) : une carte a ressource JOKER n'est donc pas defaussee, ce
# qui est bien ce que dit « a PRINTED [mental] ». Lettre mentale = "B".
# « MUST discard » : defausse forcee, pas de choix (contrairement au
# `AskDiscardFaces` d'une defausse volontaire), et toutes les cartes
# concernees, pas une seule.
# « EACH player » : `Players.ForEachPlayer` (modele ok019/40002).
# « Place 1 ADDITIONAL threat HERE for each card discarded THIS WAY » :
# le total est compte sur les defausses REELLEMENT faites, tous joueurs
# confondus, puis pose sur SOI-MEME (`[this]`, modele ok020 Malevolent Mimic).


def GetAbilities() -> Sequence['Ability']:

    def duck_and_cover(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(message)

        total = 0

        def defausser(player: 'Player') -> None:
            nonlocal total
            faces = player.hand_cards.FindCards(has_printed_res="B")
            if not faces:
                return
            defaussees = Faces.DiscardAll(faces, effect)
            total += len(defaussees) if defaussees else 0

        Players.ForEachPlayer(effect, defausser)

        if total > 0:
            this.PlaceThreatOnSchemes([this], total, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            duck_and_cover,
        ),
    ]
