from . import *

# Grounded

# « While the total cost of all upgrades and supports in play is less than
# 10[per_hero], the villain cannot be defeated. »
#
# Le cout compte les cartes des JOUEURS en jeu, ameliorations et soutiens
# confondus : le scenario demande de s'equiper avant de pouvoir frapper, et
# c'est ce que le livret annonce (« Electro ... can only be defeated when the
# players are "grounded" »).

def _cout_du_materiel(effect: 'Effect') -> int:
    total = 0
    for face in Worlds.FindCardsOnField(effect):
        if Upgrade.IsType(face) or Support.IsType(face):
            total += face.printed_cost.val
    return total


def GetAbilities() -> Sequence['Ability']:

    def pas_encore_a_la_terre(effect: 'Effect') -> bool:
        return _cout_du_materiel(effect) < Worlds.ConvertPerPlayerIconToInt("10*", effect)

    def defaite(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        # « Forced Response: After the villain is defeated, remove this card
        # from the game → each player draws 2 cards. »
        this = effect.this.CastTo(Environment)
        Faces.RemoveAllFromGame([this], effect)
        Players.ForEachPlayer(effect, lambda joueur: joueur.DrawUp(2, effect))

    return [
        *AbilityFactory.UnitCannotBeDefeatedWhile(
            AbilityType.NonKeywordBold,
            CardFinder(card_type=Villain),
            condition=pas_encore_a_la_terre,
            change_on_event=OnEvent.CardInPlay(None),
        ),
        AbilityFactory.AfterUnitBeDefeated(
            AbilityType.ForcedResponse,
            CardFinder(card_type=Villain),
            defaite
        ),
    ]
