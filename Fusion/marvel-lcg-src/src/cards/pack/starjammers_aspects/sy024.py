from . import *
# Longarm Blaster (Aggression, amelioration 2 [mental]). TECH. WEAPON.
# Attach to a STARJAMMER ally. Max 1 per ally.
# Response: After you defend against an attack, exhaust the attached ally → deal X damage to an enemy, where X is the attached ally's printed attack.
#
# Cartes de reference : sk019 / ra008 (`AfterUnitDefendAgainstAttack(Response, "You", op)`) ; falcon/53024 (`CostFunc.Exhaust("Attached",
# card_type=Ally)` pour « exhaust the attached ally ») ; 01074 Inspired (`CanPlayThisUpgradeCard(..)`).
# « After YOU defend » : l'identite du joueur qui defend (pas l'allie porteur) ; « the attached ally's PRINTED attack » : l'ATQ IMPRIMEE
# (`printed_attack`), sans les bonus (Pirate's Rapier, Blade of the Phoenix).
def GetAbilities() -> Sequence['Ability']:
    def longarm(effect: 'Effect', message: 'Message.AfterUnitDefendEnd') -> None:
        this = effect.this.CastTo(Upgrade)
        porteur = this.GetBindFace()
        x = getattr(porteur, "printed_attack", 0) if porteur is not None else 0
        this.DealDamage(effect.targets, x, effect)
    return [
        AbilityFactory.CanPlayThisUpgradeCard(CardFinder(card_type=Ally, trait="STARJAMMER")),
        AbilityFactory.AfterUnitDefendAgainstAttack(
            AbilityType.Response,
            "You",
            longarm,
        ).SetCostFunc(CostFunc.Exhaust("Attached", card_type=Ally))
        .SetTarget(Enemy),
    ]
