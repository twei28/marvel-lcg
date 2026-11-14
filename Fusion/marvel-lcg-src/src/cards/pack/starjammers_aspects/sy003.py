from . import *
# * Hepzibah (Basic, allie 3 [energy], 1*/1*, PV 3). STARJAMMER.
# Interrupt: When Hepzibah attacks an enemy, exhaust a WEAPON you control → Hepzibah gets +2 ATK for that attack. That attack gains
# overkill.
#
# Cartes de reference : 16019 Rocket Raccoon (`WhenUnitWouldAttackUnit(Interrupt, "This", Enemy-type, op)` + `GainForThisActive(effect,
# message, attack=N)` + `message.GainOverKill(effect)`) ; 27043 / rl006 (`CostFunc.Exhaust(trait="WEAPON", from_where=["YouControlCards"])`).
# « exhaust a WEAPON you control » est DEVANT la fleche : un COUT (Hepzibah ne peut pas se payer elle-meme : elle n'a pas le trait).
# « attacks an ENEMY » : villain ou sbire (`Enemy`) ; l'Interruption est facultative.
def GetAbilities() -> Sequence['Ability']:
    def hepzibah(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
        this = effect.this.CastTo(Ally)
        this.GainForThisActive(effect, message, attack=2)
        message.GainOverKill(effect)
    return [
        AbilityFactory.WhenUnitWouldAttackUnit(
            AbilityType.Interrupt,
            "This",
            Enemy,
            hepzibah,
        ).SetCostFunc(CostFunc.Exhaust(trait="WEAPON", from_where=["YouControlCards"])),
    ]
