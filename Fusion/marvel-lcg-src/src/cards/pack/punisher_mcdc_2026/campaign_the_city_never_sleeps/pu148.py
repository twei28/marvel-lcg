from . import *

# Power to the People — AMELIORATION de campagne (combat 4, p270, verso 1B de pu147). Permanent.
# Action : Remove 1 counter from here -> choose (any player may trigger this ability, each choice may only be chosen once per group per round):
#   • Remove 2 threat from a scheme.
#   • Play a card from your hand, reducing its cost by 1.
#
# Cartes de reference : 01084 Nick Fury (`ChooseAbilities` + `ForChoiceAbility(...).SetTarget(Scheme2)` + `RemoveThreatFromSchemes(cibles, 2, effect)`), pu034 Midtown
# (`PlayCardsLikeInTurn(cartes, effect, update_resources_cost=-1)` + cible `canbe_play=True, from_where=["YourHandCards"]`), pu141 (`CostFunc.Counter("This", 1, ...)`,
# `AnyPlayerCanDoThis`).
# ⚠ Mots-pieges :
#  - « Remove 1 counter -> » : le retrait est le COUT, paye avant le choix ; sans jeton l'Action n'est pas offerte ;
#  - « any player » : `AnyPlayerCanDoThis` ; « each choice ONCE per group per round » : PAS une limite de l'Action (on peut l'utiliser deux fois par round si
#    les deux choix sont differents) : memorise par (round, choix) sur le monde ; une table = un groupe ; l'Action n'est offerte que s'il reste un choix libre ;
#  - « a scheme » : n'importe quelle manigance ; « from YOUR hand » : la main du joueur qui declenche ; « reducing its cost by 1 » : -1 (cout en ressources) ;
#  - le jeton est un jeton `counter` (comme pu141/pu143). La Pod Action (mode multi-tables, pas ici) y DEPLACERA un jeton de SOUTIEN : a convertir en `counter` a ce moment-la.

MENACE = "Remove 2 threat from a scheme"
JOUER = "Play a card from your hand, reducing its cost by 1"


def GetAbilities() -> Sequence['Ability']:

    def deja_choisis(effect: 'Effect') -> set:
        monde = effect.world
        if getattr(monde, 'pu148_round', None) != monde.round_id:
            monde.pu148_round = monde.round_id
            monde.pu148_choisis = set()
        return monde.pu148_choisis

    def un_choix_libre(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        return len(deja_choisis(effect)) < 2

    def action(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        choisis = deja_choisis(effect)

        def retirer_menace(cibles: Sequence['CardFace']) -> None:
            choisis.add(MENACE)
            effect.this.RemoveThreatFromSchemes(cibles, 2, effect)

        def jouer(cartes: Sequence['CardFace']) -> None:
            choisis.add(JOUER)
            joueur.PlayCardsLikeInTurn(cartes, effect, update_resources_cost=-1)

        options = []
        if MENACE not in choisis:
            options.append(AbilityFactory.ForChoiceAbility(MENACE, retirer_menace).SetTarget(Scheme2))
        if JOUER not in choisis:
            options.append(AbilityFactory.ForChoiceAbility(JOUER, jouer).SetTarget(canbe_play=True, from_where=["YourHandCards"]))
        joueur.ChooseAbilities(effect, *options)

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, action, conditions=[un_choix_libre])
        .SetCostFunc(CostFunc.Counter("This", 1, 'counter'))
        .AnyPlayerCanDoThis(),
    ]
