from . import *

# Unconditional Love (Amour Eternel) : EVENEMENT (CONDITION.), cout 1, [wild].
# Action: If Destiny/Irene Adler is in play, ready Destiny/Irene Adler and Mystique/Raven Darkhölme. Otherwise, search your deck and discard pile for Destiny and add her to your hand. (Shuffle your deck.)
#
# CARTES DE REFERENCE
#  - `dy011` Unconditional Love (destiny) : meme carte vue du cote de Destiny (`Faces.ReadyAll` + `Search.PlayerCard(include_player_deck, include_discard_pile)` + `GainCard`).
#
# TEXTE CONTRE CODE
#  « Destiny/Irene Adler » : toute carte en jeu nommee Destiny (l'allie my006, ou l'identite du heros Destiny) ou Irene Adler (son alter-ego) ; « Mystique/Raven Darkhölme » : Mystique ou Raven Darkhölme (l'identite
#    du joueur, ou l'allie dy003). « ready ... AND ... » : les deux ensembles se redressent. « Otherwise, search YOUR DECK AND DISCARD PILE for DESTINY » : l'allie Destiny (my006), les deux zones, une carte, deck melange.
#  Chiffres : cout 1.


def GetAbilities() -> Sequence['Ability']:

    def unconditional_love(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        destiny = EnJeuNomme(effect, NOM_DESTINY, "Irene Adler")
        if destiny:
            Faces.ReadyAll(destiny + EnJeuNomme(effect, NOM_MYSTIQUE, NOM_RAVEN), effect)
            return
        face = Search.PlayerCard(
            effect,
            joueur,
            include_player_deck=True,
            include_discard_pile=True,
            name=NOM_DESTINY,
            card_type=Ally,
        )
        if face:
            joueur.GainCard(face, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            unconditional_love,
        ).SetPlay().SetLabel(),
    ]
