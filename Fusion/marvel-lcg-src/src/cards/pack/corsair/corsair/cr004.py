from . import *
# Pulse Blaster. Amelioration TECH WEAPON, cout 1, Restricted, 3 compteurs « charge ».
#
# Restricted. Uses (3 charge counters).
# Hero Response: After you attack an enemy, remove 1 charge counter from Pulse Blaster → deal 1 damage to an enemy. If
#   you removed the last charge counter from Pulse Blaster this way, tuck it under Corsair.
#
# Cartes de reference : 16036 Particle Cannon (`ThisEnterPlayWithCounters` + `CostFunc.Counter`), 47004 (Hero Response).
# ⚠ PAS de cle `Uses` dans `desc` : le mot-cle officiel DEFAUSSE la carte au dernier compteur (`has_uses.py`), alors que
# le texte la RANGE sous Corsair. Les compteurs sont donc poses et retires a la main, comme 16036.
# Une carte glissee puis rejouee rentre en jeu avec 3 compteurs neufs (`ThisEnterPlayWithCounters` a chaque entree).
def GetAbilities() -> Sequence['Ability']:
    def blaster(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Upgrade)
        this.DealDamage(effect.targets, 1, effect)
        if this.GetAllCounters() <= 0:
            identite = IdentiteDe(effect)
            if identite is not None:
                identite.TuckCardUnderHere(this, effect)
    return [
        AbilityFactory.ThisEnterPlayWithCounters(3, 'charge'),
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.HeroResponse,
            "You",
            blaster,
            against_who=Enemy,
        ).SetCostFunc(CostFunc.Counter("This", 1, 'charge'))
        .SetTarget(Enemy),
    ]
