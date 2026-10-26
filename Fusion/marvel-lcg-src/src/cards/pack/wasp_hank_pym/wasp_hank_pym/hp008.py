from . import *
# * Jocasta — soutien. « Wasp gets +1 THW » (le NOM Wasp = les deux formes heros, pas l'alter ego : cible `Hero`,
# lecon an002). Alter-Ego Response : apres le passage en alter ego, incline Jocasta -> redresse ton identite.
def GetAbilities() -> Sequence['Ability']:
    def jocasta(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)
        Faces.ReadyAll([effect.GetInitiator().GetIdentity()], effect)
    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            Hero,
            control_by="You",
            thwart=1,
        ),
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.AlterEgoResponse,
            "You",
            jocasta,
            to_form=CardFinder2(None, AlterEgo),
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
