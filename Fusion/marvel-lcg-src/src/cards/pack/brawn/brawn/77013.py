from . import *

# * Brawn's Suit — custom « Rainy »
# You get +2 hit points.
# Hero Response: After you play a card from your reserve, deal 1 damage to an
#   enemy.
#
# Amelioration SIGNATURE : pas de `CanPlayThisUpgradeCard`, et le bonus de PV
# vise "You" et non le type Hero (leçon du pack totally_awesome_hulk, ou
# Motivation ne s'appliquait jamais parce qu'elle visait un type de carte au
# lieu du porteur).

def GetAbilities() -> Sequence['Ability']:

    def un_degat(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Upgrade)

        if effect.targets:
            this.DealDamage(effect.targets, 1, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            "You",
            health=2,
        ),

        ApresCarteJoueeDepuisLaReserve(
            AbilityType.HeroResponse,
            un_degat,
            hero_form_only=True,
        ).SetTarget(Enemy),
    ]
