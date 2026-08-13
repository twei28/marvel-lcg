from . import *

# Duo-Gun

def GetAbilities() -> Sequence['Ability']:

    def duo_gun(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)

        allie = this.GetBindFace()
        initiator = effect.GetInitiator()
        if allie is None or initiator is None:
            return

        def prochaine_attaque(nom_compteur: str, piercing: bool, overkill: bool) -> None:
            Faces.RemoveCountersOn([this], 1, nom_compteur, effect)

            def gagner(effect2: 'Effect', message2: 'Message.WhenUnitWouldAttack') -> None:
                if piercing:
                    message2.GainPiercing(effect2)
                if overkill:
                    message2.GainOverKill(effect2)

            allie.effect.RegisterTemp(
                AbilityFactory.WhenUnitMakeAttack(
                    AbilityType.ForcedInterrupt,
                    "This",
                    gagner,
                ),
                unregister_after_exec=True,
            )

        choix = []
        if this.GetCounters('ammo') > 0:
            choix.append(AbilityFactory.ForChoiceAbility(
                "Remove 1 ammo counter: next attack gains piercing",
                lambda targets: prochaine_attaque('ammo', True, False)
            ).SetHasNoTargetEffect())
        if this.GetCounters('charge') > 0:
            choix.append(AbilityFactory.ForChoiceAbility(
                "Remove 1 charge counter: next attack gains overkill",
                lambda targets: prochaine_attaque('charge', False, True)
            ).SetHasNoTargetEffect())
        if choix:
            initiator.ChooseAbilities(effect, *choix)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            CardFinder(card_type=Ally)
        ),
        AbilityFactory.ThisEnterPlayWithCounters(1, 'ammo'),
        AbilityFactory.ThisEnterPlayWithCounters(1, 'charge'),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            duo_gun
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
