from . import *

# Radioactive Burst

def GetAbilities() -> Sequence['Ability']:

    def special(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Upgrade)

        player = this.GetControlByPlayer()
        if player is None:
            return
        valeur = player.GetHero().attack
        for cible in effect.targets:
            avant = cible.CastTo(CanHealth).health
            this.DealDamage([cible], valeur, effect)
            if avant - cible.CastTo(CanHealth).health >= 3:
                Faces.GiveStatus([cible], "Stunned", effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            health=-1,
        ),
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.HeroResponse,
            "You",
            special
        ).SetCostFunc(CostFunc.Discard("This"))
        .SetTarget(Enemy),
    ]
