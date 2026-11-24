from . import *

# * Armor (Hisako Ichiki) : allie RECRUITED, cout 3, PV 5, THW 1*, ATK 1*.
# Response: After Armor defends against an enemy attack, deal 1 damage to her -> give her a tough status card.
#
# Carte de reference : 22012 Wraith (`SetCostFunc(CostFunc.DealDamage(1, "This"))`), `AfterUnitDefendAgainstAttack` (do_attack.py).
# ⚠ « deal 1 damage to HER -> » est un COUT (la fleche) : le statut Tough n'est donne que si le degat a ete pris.
def GetAbilities() -> Sequence['Ability']:
    def armor(effect: 'Effect', message: 'Message.AfterUnitDefendEnd') -> None:
        this = effect.this.CastTo(Ally)
        Faces.GiveStatus([this], "Tough", effect)

    return [
        AbilityFactory.AfterUnitDefendAgainstAttack(
            AbilityType.Response,
            "This",
            armor,
            attacker=Enemy,
        ).SetCostFunc(CostFunc.DealDamage(1, "This")),
    ]
