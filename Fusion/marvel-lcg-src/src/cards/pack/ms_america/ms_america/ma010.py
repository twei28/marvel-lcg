from . import *

# America's Anger (2/2) - exemplaire physique 2/2, contenu identique a
# ma009 (voir ce fichier pour le detail des modeles et des arbitrages,
# notamment la fleche lue comme un COUT : identite deja prete = carte
# INJOUABLE, arbitrage explicite de l'utilisateur du 30/08/2026).


def GetAbilities() -> Sequence['Ability']:

    def _pouvoir(identite: 'CardFace', pouvoir: str) -> int:
        attribut = 'thwart' if pouvoir == "THW" else 'attack'
        courant = getattr(identite, attribut, 0)
        imprime = getattr(identite, 'printed_' + attribut, 0)
        return courant - imprime

    def americas_anger(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        player = effect.GetInitiator()
        if player is None:
            return
        identite = player.GetIdentity()
        if identite is None:
            return

        def armer(pouvoir: str):
            def doubler(effect2: 'Effect',
                        message2: 'Message.WhenUnitUseBasicPower') -> None:
                bonus = _pouvoir(identite, pouvoir)
                if bonus > 0:
                    message2.GainValue(bonus, effect2)

            identite.effect.RegisterTemp(
                AbilityFactory.WhenUnitUseBasicPower(
                    AbilityType.Temp2,
                    "You",
                    doubler,
                    powers=[pouvoir],
                ),
                unregister_after_exec=True,
                until_turn_end=True,
            )

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Double all modifiers applied to your THW on its next use",
                lambda targets: armer("THW"),
            ).SetHasNoTargetEffect(),
            AbilityFactory.ForChoiceAbility(
                "Double all modifiers applied to your ATK on its next use",
                lambda targets: armer("ATK"),
            ).SetHasNoTargetEffect(),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            americas_anger,
        ).SetPlay()
        .SetCostFunc(CostFunc.Ready("YourIdentity")),
    ]
