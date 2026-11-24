from . import *

# Unconditional Love : EVENEMENT (CONDITION.), cout 1, [wild]. Classe Hero.
# Action: If Mystique/Raven Darkholme is in play, ready Mystique/Raven Darkholme and Destiny/Irene Adler. Otherwise, search your deck and discard pile for Mystique and add her to your hand. (Shuffle your deck.)
#
# CARTES DE REFERENCE
#  - `01040b` : `Search.PlayerCard(.., include_player_deck=True, name=..)` + `GainCard` ; `include_discard_pile=True` pour la defausse (`ab001b`).
#  - `Faces.ReadyAll` (mt/dy003).
#
# TEXTE CONTRE CODE
#  « Mystique/Raven Darkholme » : notation nom/alter-ego, donc toute carte en jeu nommee Mystique (l'allie dy003, ou l'identite du heros Mystique) ou Raven Darkholme (son alter-ego) ; « Destiny/Irene Adler » : l'identite
#    du joueur (deux faces). « ready ... AND ... » : les deux se redressent. « Otherwise, search YOUR DECK AND DISCARD PILE » : les deux zones, une seule carte, deck melange. Question de lecture signalee en fin de travail.
#  Chiffres : cout 1.


def GetAbilities() -> Sequence['Ability']:

    def unconditional_love(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        joueur = effect.GetInitiator()
        enjeu = [f for f in Worlds.FindCardsOnField(effect) if (f.name in (NOM_MYSTIQUE, NOM_RAVEN))
                 and (Ally.IsType(f) or Hero.IsType(f) or AlterEgo.IsType(f))]
        if enjeu:
            Faces.ReadyAll(enjeu + [joueur.GetIdentity()], effect)
            return
        face = Search.PlayerCard(
            effect,
            joueur,
            include_player_deck=True,
            include_discard_pile=True,
            name=NOM_MYSTIQUE,
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
