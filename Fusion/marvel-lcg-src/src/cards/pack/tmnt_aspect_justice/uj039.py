from . import *

# * Zebulon — ALLIE 2 [mental], aspect Justice (TMNT Aspects, Inkwire). DIMENSION X. NOVA POSSE.
# Bandeau « ✦ Squirrel Girl » (unique_also, decision Q-R1).
# PV 2, THW 1 (1 degat consecutif), ATK 1 (1 degat consecutif).
# Response: After you play Zebulon from your hand, place 1 scorch counter here for each card in your hand
#   (to a maximum of 4).
# Action: Remove 1 scorch counter from here → remove 1 threat from a scheme.
#
# MODIFIEE par rapport a `61017` Squirrel Girl (Doreen Green) : « squirrel counter » -> « scorch counter ».
# Pas d'`ability_link` (le compteur change) : script propre, copie de 61017 adaptee. Compteur « scorch »
# AJOUTE a `CardFace.COUNTER` (card_face.py) : sans lui `PlaceCountersInternal` refuse le nom.
#
# CARTES DE REFERENCE
#  - `61017` (officielle) : `AfterYouPlayThisFromHand(Response, op)` + `PlaceCountersInternal(len(main),
#    ..., maximum=4)` ; Action `CostFunc.Counter("This", 1, ...)` + `SetTarget(Scheme2, range=(1, 1))`.
#
# TEXTE CONTRE CODE (PROCESSUS-CARTE etape 5)
#  ⚠ « After you PLAY Zebulon FROM YOUR HAND » : pas une mise en jeu par un effet.
#  ⚠ « for each card in your hand (to a maximum of 4) » : la main APRES avoir joue Zebulon, plafond 4.
#  ⚠ « Remove 1 scorch counter from here → » : COUT ; sans compteur, pas d'Action.
#  Aucune limite imprimee (l'Action se repete tant qu'il reste des compteurs).


def GetAbilities() -> Sequence['Ability']:

    def placer(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        joueur = effect.GetInitiator()
        this.PlaceCountersInternal(len(joueur.hand_cards.Get()), 'scorch', effect, maximum=4)

    def retirer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        this.RemoveThreatFromSchemes(effect.targets, 1, effect)

    return [
        AbilityFactory.AfterYouPlayThisFromHand(AbilityType.Response, placer),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, retirer)
        .SetCostFunc(CostFunc.Counter("This", 1, 'scorch')).SetTarget(Scheme2, range=(1, 1)),
    ]
