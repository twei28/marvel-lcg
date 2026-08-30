from . import *

# Teleport (2/2) — exemplaire physique 2 de 2, contenu identique a wc011
# (voir ce fichier pour le detail des modeles et des arbitrages).


def GetAbilities() -> Sequence['Ability']:

    def teleport(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        icones = IconesBoostDuDessus(effect, effect.GetInitiator())

        for target in effect.targets:
            joueur = target.GetControlByPlayer()
            if joueur is None:
                continue

            identite = joueur.GetIdentity()
            if identite is not None:
                Faces.ReadyAll([identite], effect)

            YouMayChangeForm(joueur, effect)

            if icones < 2:
                continue

            identite = joueur.GetIdentity()
            if identite is None:
                continue

            def bonus(pouvoir: str, face: 'CardFace'):
                def appliquer(targets: Sequence['CardFace']) -> None:
                    Unused(targets)
                    face.TemporaryGain(
                        effect,
                        None,
                        Message.WhenRoundEnd,
                        ignore_flip=True,
                        render_ui=True,
                        **{pouvoir: 1},
                    )
                return appliquer

            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "+1 ATK until the end of the round",
                    bonus("attack", identite),
                ),
                AbilityFactory.ForChoiceAbility(
                    "+1 THW until the end of the round",
                    bonus("thwart", identite),
                ),
                AbilityFactory.ForChoiceAbility(
                    "+1 DEF until the end of the round",
                    bonus("defense", identite),
                ),
                AbilityFactory.ForChoiceAbility(
                    "+1 REC until the end of the round",
                    bonus("recover", identite),
                ),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            teleport,
        ).SetPlay()
        .SetTarget("Players"),
    ]
