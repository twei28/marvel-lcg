from . import *

# Motivation — custom « DesignHacker »
# Your hero gets +1 DEF.
# Hero Response: After your hero defends, take 2 damage → ready your hero.


def GetAbilities() -> Sequence['Ability']:

    def take_2_damage(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        initiator = effect.GetInitiator()
        initiator.GetIdentity().TakeDamage(2, effect)
        return True

    def motivation(effect: 'Effect', message: 'Message.AfterUnitDefendEnd') -> None:
        initiator = effect.GetInitiator()

        Faces.ReadyAll([initiator.GetIdentity()], effect)

    return [
        # « You » = l'identite qui porte l'amelioration. Viser le type `Hero`
        # ne fonctionne QUE pour les cartes explicitement attachees
        # (AttachToFaceWhenPutIntoPlay), pas pour une amelioration jouee sur soi.
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            defense=1,
        ),
        AbilityFactory.AfterUnitDefendEnd(
            AbilityType.HeroResponse,
            "You",
            motivation,
        ).SetCostFunc(CostFunc.Custom(None, take_2_damage)),
    ]
