from . import *

# Jump-Start : amelioration Basic, cout 3. SUPERPOWER.
# Attach to a friendly character. Max 1 per character.
# Response: After your turn begins, deal 1 damage to attached character -> place 1 power counter here.
# Interrupt: When attached character makes a basic thwart or basic attack action, remove 1 power counter from here -> that character gets
# +1 THW and +1 ATK for that action.
#
# Cartes de reference : 31029 Clarity of Purpose (`CanPlayThisUpgradeCard(Friend)` + `CostFunc.DealDamage(1, "Attached")`), 34007 Telekinetic Shield
# (declencheur "AttachedCharacter"), `message.GainATKForThisAttack` / `GainTHWForThisThwart` (sender_damage.py / sender_friend.py).
# ⚠ « +1 THW and +1 ATK for THAT action » : une seule action (contrer OU attaquer) : le bonus qui compte est celui de l'action faite ;
# « remove 1 power counter from here -> » est un COUT : sans compteur, pas de bonus.
def GetAbilities() -> Sequence['Ability']:
    def compteur(effect: 'Effect', message: 'Message.AfterPlayerTurnBegin') -> None:
        this = effect.this.CastTo(Upgrade)
        Faces.PlaceCountersOn([this], 1, 'power', effect)

    def attaque(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)
        Faces.RemoveCountersOn([this], 1, 'power', effect)
        message.GainATKForThisAttack(1, effect)

    def contre(effect: 'Effect', message: 'Message.WhenUnitWouldThwart') -> None:
        this = effect.this.CastTo(Upgrade)
        Faces.RemoveCountersOn([this], 1, 'power', effect)
        message.GainTHWForThisThwart(1, effect)

    def avec_compteur(effect: 'Effect', message: 'Message2') -> bool:
        return effect.this.GetCounters('power') > 0

    return [
        AbilityFactory.CanPlayThisUpgradeCard(Friend),
        AbilityFactory.AfterPlayerTurnBegin(
            AbilityType.Response,
            "You",
            compteur,
        ).SetCostFunc(CostFunc.DealDamage(1, "Attached")),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.Interrupt,
            "AttachedCharacter",
            attaque,
            is_basic_attack=True,
            conditions=[avec_compteur],
        ),
        AbilityFactory.WhenUnitMakeThwart(
            AbilityType.Interrupt,
            "AttachedCharacter",
            Scheme2,
            contre,
            is_basic_thwart=True,
            conditions=[avec_compteur],
        ),
    ]
