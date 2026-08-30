from . import *

# Royal Couple — evenement BASIC, custom « CptScorp »
# Cout 1, [wild], classe Basic, trait CONDITION, Max 1 per deck.
# Team-Up (Hulkling and Wiccan). Max 1 per deck.
# Hero Action: Choose one card from the encounter discard pile and put it on
#   top of the encounter deck. Ready your hero.
#
# ARBITRAGE TRANCHE PAR L'UTILISATEUR le 30/08/2026 : le mot-cle « Team-Up »
# n'est PAS rendu par la cle `desc.TeamUp` ni par `.SetTarget("TeamUp")`, qui
# supposent deux IDENTITES HEROS distinctes a la table. Il devient une simple
# CONDITION « Hulkling en jeu, allie OU heros », portee par
# `HulklingEnJeu(effect)` (voir wiccan/__init__.py pour le detail du bornage
# de la recherche par nom). Precedent exact du meme auteur : `il023` Sudden
# Plan Change, Team-Up (Stature and Iron Lad), rendu de la meme facon.
#
# La condition passe par `conditions=[...]` sur `WhenInYourPlayTurn`, et NON
# par `SetPlay(only_if_you_control_face=...)` : correctif deja paye sur il023,
# `only_if_you_control_face` cherche dans `GetInventoryDeck()` (les
# ameliorations equipees), jamais les allies en jeu.
#
# « Wiccan » n'a PAS besoin d'etre verifie : la carte est de classe Basic mais
# elle n'existe que dans le deck de Wiccan, et la moitie « Hulkling » est la
# seule qui puisse manquer. C'est aussi la lecture d'il023, qui ne verifie que
# Stature.
#
# « Choose one card from the encounter discard pile and put it on top of the
# encounter deck » -> modele EXACT : Sharon Carter (`agent_13/agent_13/
# ag001b.py`), meme triplet `Worlds.GetEncounterDiscardPileCards` +
# `AskChooseFace` + `Faces.MoveAllToDeck([choisie], deck, "Top", effect)`.
# Meme garde qu'elle sur la defausse de rencontre VIDE (premier tour de
# partie) : on sort sans rien faire plutot que de poser une question sans
# reponse possible.
#
# « Ready your hero » -> `Faces.ReadyAll([identite], effect)` (modele il015 /
# ok014 / hd001a). Elle est INCONDITIONNELLE : elle a lieu meme si la defausse
# de rencontre etait vide (aucun « if » imprime, et c'est bien la seconde
# phrase, pas la suite de la premiere).
#
# `AbilityType.HeroAction` : « Hero Action » imprime, donc injouable en forme
# civile.

def GetAbilities() -> Sequence['Ability']:

    def hulkling_en_jeu(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        Unused(message)
        return HulklingEnJeu(effect)

    def royal_couple(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return

        defausse = Worlds.GetEncounterDiscardPileCards(effect)
        if defausse:
            choisie = joueur.AskChooseFace(
                defausse,
                effect,
                prompt="Put on top of the encounter deck",
            )
            if choisie is not None:
                deck = Worlds.GetEncounterDeck(effect)
                Faces.MoveAllToDeck([choisie], deck, "Top", effect)

        identite = joueur.GetIdentity()
        if identite is not None:
            Faces.ReadyAll([identite], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            royal_couple,
            conditions=[hulkling_en_jeu],
        ).SetPlay(),
    ]
