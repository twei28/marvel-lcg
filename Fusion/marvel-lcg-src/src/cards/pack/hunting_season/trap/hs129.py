from . import *

# hs129 Bear Trap
# When Revealed : epuiser son identite ou attacher. Forced Interrupt : fin de phase heros, 1 degat.
# Action : depensez une ressource physique et subissez 2 degats → defaussez.

def GetAbilities() -> Sequence['Ability']:

    def mordre(effect: 'Effect', message: 'Message.WhenPhaseEnd') -> None:
        this = effect.this.CastTo(Attachment)
        cible = this.bind_face
        if cible is not None:
            cible.TakeDamage(this, 1, effect)

    return [
        PiegeAttachement(),
        AbilityFactory.WhenPlayerPhaseEnd(AbilityType.ForcedInterrupt, mordre),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction)
            .SetCost(Cost("R"))
            .SetCostFunc(CostFunc.TakeDamage(2, "YourIdentity")),
    ]
