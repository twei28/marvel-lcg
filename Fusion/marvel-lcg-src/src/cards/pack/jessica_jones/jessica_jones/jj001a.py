from . import *

# * Jessica Jones — custom « ekAugust »
# Hard-Hitting Investigation — Response (attack): After you defeat a side
#   scheme, deal damage to an enemy equal to your ATK.

def GetAbilities() -> Sequence['Ability']:

    def hard_hitting_investigation(effect: 'Effect', message: 'Message.AfterUnitDefeatedScheme') -> None:
        this = effect.this.CastTo(Hero)
        this.DealDamage(effect.targets, this.attack, effect)

    return [
        # Marqueur silencieux « manigance secondaire vaincue ce round »,
        # lu par The Truth Hurts (jj007). Voir le __init__.py du set.
        RecordSideSchemeDefeat(),

        AbilityFactory.AfterUnitDefeatedScheme(
            AbilityType.Response,
            "You",
            SchemeSide2,
            hard_hitting_investigation,
        ).SetName("Hard-Hitting Investigation")
        .SetLabel('attack')
        .SetTarget(Enemy),
    ]
