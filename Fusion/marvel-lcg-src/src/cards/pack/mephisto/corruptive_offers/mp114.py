from . import *

# * Warring Rage — pacte BARGAIN (Corruptive Offers). Boost 3, Peril (natifs). Communs : `AbilitesDePacteCorrompu`.
# Hero Response : After you attack and defeat an enemy, place 1 corrupt counter here -> ready your hero, heal 1 damage, and draw 1 card.
#
# Cartes de reference : defeated.py `AfterUnitAttackAndDefeatUnit(AbilityType.HeroResponse, "You", ..)`.
# ⚠ Mots-pieges : « Hero Response » : forme heros seulement ; « attack AND DEFEAT » : l'attaque doit vaincre l'ennemi (sbire ou autre ennemi) ; « ready your hero,
# heal 1 damage, draw 1 card » : les trois, dans cet ordre ; une fois par ennemi vaincu.


def GetAbilities() -> Sequence['Ability']:
    def rage(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        this = effect.this.CastTo(Attachment)
        joueur = effect.GetInitiator()
        Faces.PlaceCountersOn([this], 1, 'corrupt', effect)
        heros = joueur.GetIdentity()
        Faces.ReadyAll([heros], effect)
        heros.HealHealth(1, effect)
        joueur.DrawUp(1, effect)

    return [
        *AbilitesDePacteCorrompu(),
        AbilityFactory.AfterUnitAttackAndDefeatUnit(AbilityType.HeroResponse, "You", Enemy, rage),
    ]
