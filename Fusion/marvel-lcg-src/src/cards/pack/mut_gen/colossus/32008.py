from . import *

# Steel Fist
#
# ERRATA RRG 1.7 / 1.8 (Annexe V, Mutant Genesis #8) : « You may discard a tough status card from your hero TO stun and confuse that enemy » (la fleche de cout devient « to »).
#   Le script suivait DEJA le nouveau texte : le choix facultatif est tire apres les 5 degats, la carte Tenace est defaussee PUIS les deux statuts sont poses (aucun cout).
#   Cas : `32008` de `tools/cas/errata_rrg.py`. Relu le 03/11/2026 : rien a changer.

def GetAbilities() -> Sequence['Ability']:

    def steel_fist(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        this.DealDamage(effect.targets, 5, effect)

        def action(targets: Sequence['CardFace'], by_effect: 'Effect'):
            Faces.DiscardAll(by_effect.targets2, effect)

            Faces.GiveStatus(targets, "Stunned", effect)
            Faces.GiveStatus(targets, "Confused", effect)

        initiator.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility3(
                "Discard a tough status card from your hero to stun and confuse that enemy",
                action
            )
            .SetTarget(effect.targets, canbe_status=["Stunned", "Confused"])
            .SetTarget2("YourHeroTough", is_optional=False)
        )


    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            steel_fist
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]

