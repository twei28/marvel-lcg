from . import *

# Flightpack : AMELIORATION (ITEM. TECH.), cout 2, [energy].
# RoboCop gains the AERIAL trait.
# Hero Action (attack): Exhaust this card → deal 1 damage to a minion. Engage that enemy.
#
# CARTES DE REFERENCE
#  - `36007` Storm's Cape : `GiveKeywordToAttached(CardFinder(name=..), trait="AERIAL")`. `ar001a` / `br011` : `Minion.EngagePlayer(joueur, effect)` pour « engage that enemy ».
#
# TEXTE CONTRE CODE
#  « RoboCop gains the AERIAL trait » -> le HEROS (nom propre : la face alter-ego n'a pas de bonus). « deal 1 damage to A MINION » -> un sbire (pas le vilain) ;
#  « engage THAT enemy » -> avec le joueur qui agit, meme si le sbire a survecu seulement ; un sbire vaincu n'est plus engage.
#  Hero Action avec label (attack), cout : s'incliner. Chiffres : cout 2, 1 degat.


def GetAbilities() -> Sequence['Ability']:

    def flightpack(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        joueur = effect.GetInitiator()
        hero = joueur.GetHero()
        hero.DealDamage(effect.targets, 1, effect)
        for sbire in effect.targets:
            if Minion.IsType(sbire) and sbire.card.IsOnField():
                sbire.CastTo(Minion).EngagePlayer(joueur, effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="RoboCop"),
            trait="AERIAL",
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            flightpack,
        ).SetLabel('attack')
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Minion),
    ]
