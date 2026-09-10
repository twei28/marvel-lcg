from . import *

# * Doctor Doom — SBIRE de nemesis (1/5). 7 PV, ATQ 2, MNG 2, boost 4.
# ELITE. GENIUS. MYSTIC.
# Stalwart. Toughness. Villainous.
# When Revealed: If Cabal Obligations is in play, deal 1 encounter card to each
#   player. Otherwise, find Cabal Obligations and reveal it. (Shuffle.)
# Cabal Rivalry — Special: Shuffle Doctor Doom into the encounter deck -> play
#   an Iron Patriot card from your deck or discard pile, ignoring its resource
#   cost. (Shuffle.)
#
# ⚠⚠ POURQUOI UN SBIRE DE NEMESIS PORTE-T-IL UN « SPECIAL » ?
# Parce que `ip001a` Iron Patriot peut melanger DANS LE DECK REGISTERED
# n'importe quel sbire qu'il vient de vaincre a l'attaque, Doom compris. Doom
# revient alors comme une carte du deck REGISTERED : revele, il coute ses 4
# icones de boost, et paye il devient un allie REGISTERED dont on peut resoudre
# le « Special ». L'insert l'annonce : « he is able to recruit these traitors
# once more after they are defeated ». Rien a arbitrer, tout se tient.
#
# CARTES DE REFERENCE
#  - `04077` * Absorbing Man : la structure EXACTE du « When Revealed » —
#    `Worlds.FindCardOnField` pour la carte deja en jeu, `Players.ForEachPlayer`
#    + `DealEncounterCards(1, ...)` sinon, et le repli qui va CHERCHER la carte.
#  - `56027` * Madame Masque : `Find.FindAndReveal`, qui fouille TOUTES les
#    zones — c'est ce que « find » veut dire (find.py, en-tete).
#  - `dd003` Doombot : `PlayCardsLikeInTurn(..., ignore_resources_cost=True)`.
#
# TEXTE CONTRE CODE
#  ⚠ « If Cabal Obligations IS IN PLAY » : en jeu, pas en defausse. D'ou
#    `Worlds.FindCardOnField` et non `Find.Find`.
#  ⚠ « (Shuffle.) » apres « find » : `Find.FindAndReveal` remelange deja les
#    paquets fouilles. Rien a ajouter.
#  ⚠ « SHUFFLE Doctor Doom into the encounter deck -> » : c'est un COUT, avant
#    la fleche. Si Doom ne peut pas partir, le « Special » ne se resout pas.
#  ⚠ « an IRON PATRIOT card » : une carte du set heros, `set_name="Iron
#    Patriot"`. Pas une carte d'aspect, pas une carte basique.
#  ⚠ « from your deck OR DISCARD PILE » : les deux zones.
#  ⚠ Stalwart, Toughness et Villainous sont des BASES NATIVES lues dans `desc`.


def GetAbilities() -> Sequence['Ability']:

    def doom_revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)

        face = Worlds.FindCardOnField(effect, name="Cabal Obligations",
                                      card_type=Attachment)
        if face:
            def distribuer(joueur: 'Player') -> None:
                joueur.DealEncounterCards(1, effect)
            Players.ForEachPlayer(effect, distribuer)
        else:
            Find.FindAndReveal(effect, message.GetToPlayer(),
                               name="Cabal Obligations")

    def melanger_doom(cibles: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(cibles)
        Faces.ShuffleAllTo([effect.this], "EncounterDeck", effect)
        return True

    def rivalite_du_cabal(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        face = Search.PlayerCard(
            effect,
            joueur,
            include_player_deck=True,
            include_discard_pile=True,
            set_name="Iron Patriot",
        )
        if face:
            joueur.PlayCardsLikeInTurn([face], effect,
                                       ignore_resources_cost=True, forced=True)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            doom_revele,
        ),
        SpecialRegistered("Cabal Rivalry", rivalite_du_cabal)
        .SetCostFunc(CostFunc.Custom(None, melanger_doom)),
    ]
