from . import *

# Psionic Shield — AMELIORATION, cout 2 (energie). PSIONIC.
# Marvel Girl gets +2 DEF.
# Hero Response: After Marvel Girl defends against an enemy attack, and take no damage, exhaust Psionic Shield -> confuse
# that enemy.
#
# CARTES DE REFERENCE : `01028` (`GiveKeywordToAttached(CardFinder(name=..), ..)`), `09020` Unflappable
# (`AfterUnitDefendAgainstAttack(.., take_no_damage=True)`).
#
# MOTS-PIEGES : « and take no damage » (l'ennemi n'a rien inflige) ; « that enemy » = l'attaquant.
def GetAbilities() -> Sequence['Ability']:
    def psionic_shield(effect: 'Effect', message: 'Message.AfterUnitDefendEnd') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        attaquant = message.would_atk_message.attacker
        if attaquant is not None and attaquant.IsInPlay():
            Faces.GiveStatus([attaquant], "Confused", effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="Marvel Girl"),
            defense=2,
        ),
        AbilityFactory.AfterUnitDefendAgainstAttack(
            AbilityType.HeroResponse,
            "You",
            psionic_shield,
            attacker=Enemy,
            take_no_damage=True,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
