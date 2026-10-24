from . import *

# * Norrin Radd (face ALTER-EGO) — COSMIC. ADVENTURER. PV 14, REC 4, main 6.
# Toomie! — Action: Exhaust Norrin Radd -> search your deck and discard pile for The Silver Surfboard
#   upgrade and add it to your hand. Shuffle your deck.
#
# Cartes de reference :
#  - `yd001b` * Yondu Udonta (Whistlin') : « Exhaust Yondu Udonta -> ... add it to your hand », meme cout
#    `CostFunc.Exhaust("YourIdentity")` et meme fouille `Search.SearchForCards`.
#  - `an001b` * Aldrif Odinsdottir, `ok001b` * Okoye : fouille du deck + ajout en main, melange par defaut.
#
# ⚠ Mots-pieges :
#  - « deck AND discard pile » seulement (PAS la main ni le « hors jeu » du mot-cle `summon`) :
#    ce n'est pas un `summon`, le texte ne le dit pas.
#  - « add it to your HAND » : en main, pas en jeu.
#  - « Shuffle your deck » : comportement par defaut de `Search` (rien a coder).
#  - « Exhaust Norrin Radd -> » : la fleche en fait un COUT ; l'alter-ego deja incline ne peut plus chercher.
#  - Aucune limite imprimee.


def GetAbilities() -> Sequence['Ability']:

    def toomie(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        faces = Search.SearchForCards(
            effect, joueur,
            include_player_deck=True,
            include_player_discard_pile=True,
            name=NOM_PLANCHE,
            card_type=Upgrade,
        )
        if faces:
            joueur.GainCard(faces[0], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            toomie,
        ).SetName("Toomie!")
        .SetCostFunc(CostFunc.Exhaust("YourIdentity")),
    ]
