from . import *

# Causing a Commotion — COMPLOT ANNEXE nemesis (N 3/5). 2 icones de boost.
#   Menace de depart 1[per_hero]. Icone de HASARD.
# When Revealed: Each player discards the top 3 cards of their deck and places
#   1 threat here for each different card type they discarded this way.
#
# MOT-CLE : HAZARD — fiche `docs/reference/mots-cles/hazard.md`. BASE
# AUTOMATIQUE, `desc.Hazard = "1"`. Aucun script. L'icone a ete identifiee par
# COMPARAISON D'IMAGE (un « + » sur une carte inclinee), jamais a vue : c'est
# la leçon Lockjaw, et la carte voisine tg012 porte, elle, un « ! » etoile,
# c'est-a-dire une CRISE. Deux icones differentes dans le meme set.
#
# CARTE DE REFERENCE
#  - `06030` Trickster, le complot nemesis de THOR : « When Revealed: Discard
#    the top 3 cards of your deck. Place 1 threat on the main scheme for each
#    different card type discarded this way. » MOT POUR MOT la meme carte, a
#    deux differences pres (voir ci-dessous). Montage :
#    `player.DiscardDeckTopCards(3, effect)` puis
#    `FacesCounter.GetDifferentTypesCount(faces)`.
#  - `02026` Goblin Reinforcements : `this.PlaceThreatOnSchemes([this], n,
#    effect)` pour « place N threat HERE ».
#  - `01151` Under Attack : `Players.ForEachPlayer(effect, action)` pour
#    « EACH PLAYER ».
#
# TEXTE CONTRE CODE
#  ⚠ DEUX DIFFERENCES AVEC `06030`, et elles comptent toutes les deux :
#    1. « EACH PLAYER discards » et non « discard the top 3 cards of YOUR
#       deck » : a plusieurs, tout le monde defausse et tout le monde
#       contribue. Mot-piege « each » (`wd001b`, `wd014`).
#    2. « places 1 threat HERE » et non « on the main scheme » : la menace
#       s'empile sur CE complot annexe, ce qui le rend d'autant plus dur a
#       vaincre. `[this]`, pas `"MainScheme"`.
#  « for each DIFFERENT CARD TYPE » -> le nombre de TYPES distincts parmi les
#    3 cartes (evenement / soutien / amelioration / ressource / allie), pas le
#    nombre de cartes. Trois evenements ne posent qu'UNE menace ; trois types
#    differents en posent trois. `FacesCounter.GetDifferentTypesCount` fait
#    exactement ce decompte.
#  « discarded THIS WAY » -> seulement les cartes defaussees a l'instant, pas
#    la defausse entiere. C'est le RETOUR de `DiscardDeckTopCards` qu'on
#    compte, jamais la pile.
#  ⚠ Un joueur dont le deck contient moins de 3 cartes en defausse moins : le
#    decompte porte sur ce qui est REELLEMENT parti.


def GetAbilities() -> Sequence['Ability']:

    def faire_du_grabuge(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(message)

        def pour_chaque_joueur(joueur: 'Player') -> None:
            faces = joueur.DiscardDeckTopCards(3, effect)
            valeur = FacesCounter.GetDifferentTypesCount(faces)
            if valeur > 0:
                this.PlaceThreatOnSchemes([this], valeur, effect)

        Players.ForEachPlayer(effect, pour_chaque_joueur)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            faire_du_grabuge,
        ),
    ]
