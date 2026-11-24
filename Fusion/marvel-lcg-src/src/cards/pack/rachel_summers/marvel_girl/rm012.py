from . import *

# Telekinetic Sword — AMELIORATION, cout 3 (physique), Restricted. PSIONIC. WEAPON.
# You get +3 hit points.
# Marvel Girl attacks gain piercing.
# Hero Response: After you attack, exhaust Telekinetic Sword -> draw 1 card.
#
# CARTES DE REFERENCE : `01039` Rocket Boots (`GiveKeywordToAttached("You", health=N)`), `uw010`
# (`UnitAttackGainKeyword("You", piercing=True)`), `27187a` (Response apres une attaque, ici `AfterUnitAttackEnd`).
#
# MOTS-PIEGES : « Marvel Girl ATTACKS gain piercing » = TOUTES ses attaques (pas seulement les attaques de base) ; « After you
# attack » : toute attaque, de base ou non.
def GetAbilities() -> Sequence['Ability']:
    def telekinetic_sword(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        effect.GetInitiator().DrawUp(1, effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            health=3,
        ),
        AbilityFactory.UnitAttackGainKeyword(
            "You",
            piercing=True,
        ),
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.HeroResponse,
            "You",
            telekinetic_sword,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
