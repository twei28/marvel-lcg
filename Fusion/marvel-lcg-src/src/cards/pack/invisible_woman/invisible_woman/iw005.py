from . import *


def GetAbilities() -> Sequence['Ability']:

    def psionic_form(effect: 'Effect', message: 'Message.CheckIfAttackMessageHasKeyword') -> bool:
        return IsPsionicForm(effect.GetInitiator().GetIdentity())

    def flying_disk(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        this.DealDamage(effect.targets, 4, effect)

    return [
        # CORRECTIF : le scan conditionne LES DEUX effets a la forme PSIONIC
        # (« If you are in PSIONIC hero form, you gain the AERIAL trait AND
        # your attacks gain ranged »). Le trait etait accorde en permanence.
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder2("PSIONIC", Hero),
            trait="AERIAL",
            ex_change_on_event=OnEvent.Form("You"),
        ),
        AbilityFactory.UnitAttackGainKeyword(
            "You",
            ranged=True,
            conditions=[psionic_form],
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            flying_disk,
        ).SetCostFunc(CostFunc.Discard("This"))
        .SetTarget(Enemy)
        .SetName("Flying Disk"),
    ]
