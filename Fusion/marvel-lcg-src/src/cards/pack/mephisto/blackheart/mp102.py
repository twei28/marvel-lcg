from . import *

# * Prince's Offer — MANIGANCE ANNEXE (modulaire Blackheart). Boost 2, Acceleration, menace de depart 2[per_hero], Incite 1 (natifs, `desc`).
# When Defeated : Each player may shuffle 1 BARGAIN attachment they control into the encounter deck. The player who defeated this scheme finds the
# Black-Hearted attachment and reveals it.
#
# Cartes de reference : mp016 (`WhenSchemeBeDefeated`, `message.defeating_player`), mp020 (`Faces.ShuffleAllTo(.., "EncounterDeck", ..)`), mp103 / find.md
# (`Search.EncounterCard` + `Reveal`).
# ⚠ Mots-pieges : « EACH player MAY » : facultatif, un pacte par joueur, ceux de CE joueur ; « THE PLAYER WHO DEFEATED » : un seul joueur trouve Black-Hearted,
# apres les remelanges (le pacte remelange peut donc etre Black-Hearted lui-meme) ; « find » : deck et defausse.


def GetAbilities() -> Sequence['Ability']:
    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        for joueur in JoueursDansLOrdre(effect):
            if not PactsDuJoueur(joueur):
                continue

            def remelange(targets: Any, joueur: 'Player'=joueur) -> None:
                pacte = Search.SearchForCard(effect, joueur, faces=PactsDuJoueur(joueur), not_move=True)
                if pacte is not None:
                    Faces.ShuffleAllTo([pacte], "EncounterDeck", effect)

            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility("Shuffle a BARGAIN attachment you control into the encounter deck", remelange),
                forced=False,
            )
        vainqueur = message.defeating_player or JoueursDansLOrdre(effect)[0]
        trouve = Search.EncounterCard(effect, vainqueur, include_discard_pile=True, name="Black-Hearted", card_type=Attachment)
        if trouve is not None:
            trouve.Reveal(vainqueur, effect)

    return [
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincue),
    ]
