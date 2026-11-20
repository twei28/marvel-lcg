from . import *
# Far-Flung Family (Leadership, evenement 4 [mental]). Alliance.
# Action: Exhaust a STARJAMMER character and an X-MEN character → as a group, the players search their decks for a total of 1 STARJAMMER ally
# and 1 X-MEN ally and put them into play exhausted.
#
# Cartes de reference : 26035 Joining Forces (« a total of 1 X ally and 1 Y ally » : `range=(1, 2)` + `select_rule="MustIncludeTraits"` : UNE carte
# qui porte les deux traits satisfait les deux) ; 48032 Gunboat Diplomacy (`desc.Alliance` + `CostFunc.Exhaust(Select.Alliance([T1, T2]))`) ;
# 08011 (`Search.PlayerCard`).
# ⚠ « as a group, the players search THEIR decks » : les joueurs, DANS L'ORDRE, cherchent chacun dans son deck ce qui manque encore (le 1er joueur
# d'abord, une recherche par ligne manquante) ; une carte STARJAMMER et X-MEN a la fois comble les deux lignes. Mise en jeu INCLINEE, sous le controle du proprietaire du deck.
def GetAbilities() -> Sequence['Ability']:
    def far_flung(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        manque = ["STARJAMMER", "X-MEN"]
        def action(joueur: 'Player') -> None:
            nonlocal manque
            if not manque:
                return
            while manque:
                face = Search.PlayerCard(effect, joueur, include_player_deck=True, may=True, card_type=Ally, traits=list(manque))
                if not face:
                    break
                manque = [t for t in manque if not face.HasTrait(t)]
                face.PutIntoPlay(joueur, effect)
                Faces.ExhaustAll([face], effect)
        Players.ForEachPlayer(effect, action)
    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            far_flung,
        ).SetPlay().SetLabel()
        .SetCostFunc(CostFunc.Exhaust(Select.Alliance(["STARJAMMER", "X-MEN"]))),
    ]
