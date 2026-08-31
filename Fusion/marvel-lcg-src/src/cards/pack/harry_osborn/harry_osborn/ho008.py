from . import *

# * Goblin Armor — amelioration signature. ARMOR. TECH. Cout 3.
# You get +3 hit points.
# Hero Action (thwart): Exhaust Goblin Armor -> remove 1 threat from a
#   scheme (2 threat instead if you have the AERIAL trait).
#
# Cartes de reference :
#  - « You get +3 hit points » : an008 * Siri's Dress / 05023 Endurance,
#    `GiveKeywordToAttached("You", health=3)` ;
#  - la variante conditionnee au trait : 01038 Powered Gauntlets officiel
#    (« 2 damage instead if you have the [[Aerial]] trait »), meme test
#    `hero.HasTrait("AERIAL")` au moment de la resolution ;
#  - l'action de thwart sur epuisement : vp001a / an004 pour
#    `RemoveThreatFromSchemes` + `SetTarget(Scheme2)`.

def GetAbilities() -> Sequence['Ability']:

    def goblin_armor(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)

        initiator = effect.GetInitiator()
        hero = initiator.GetHero()
        montant = 1
        if hero is not None and hero.HasTrait("AERIAL"):
            montant = 2
        this.RemoveThreatFromSchemes(effect.targets, montant, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            health=3,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            goblin_armor
        ).SetLabel('thwart')
        .SetTarget(Scheme2)
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
