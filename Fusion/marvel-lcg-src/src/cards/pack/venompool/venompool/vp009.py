from . import *

# Klyntar Suit — amelioration. SYMBIOTE. Cout 2.
# You get +3 hit points.
# Hero Response (attack): After you take damage from an enemy attack, exhaust
#   Klyntar Suit -> drain 1 from the attacking enemy. (See insert.)
#
# Cartes de reference :
#  - 05023 Endurance (pack msm) : `GiveKeywordToAttached("You", health=3)`,
#    exactement le meme « You get +3 hit points ».
#  - av009 Bear Arms (pack agent_anti_venom) : le meme « drain N » declenche
#    par une Response, avec le helper local du pack.
#
# Le declencheur EXIGE que l'attaque ait fait des degats (« After you TAKE
# DAMAGE from an enemy attack »), d'ou `AfterUnitAttackAndDamageUnit` et non
# `AfterUnitAttackUnit` : une attaque entierement defendue ne declenche rien.
#
# La cible du drain est « the ATTACKING enemy », pas un ennemi au choix :
# elle est lue sur le message (`message.attacker`), jamais choisie.

def GetAbilities() -> Sequence['Ability']:

    def klyntar_suit(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Upgrade)

        attaquant = message.attacker
        if attaquant is None:
            return
        Drain(this, [attaquant], 1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            health=3,
        ),
        AbilityFactory.AfterUnitAttackAndDamageUnit(
            AbilityType.HeroResponse,
            Enemy,
            "You",
            klyntar_suit,
        ).SetLabel('attack')
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
