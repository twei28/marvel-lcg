from . import *

# Master Plan — evenement, cout 0, [mental]. « Action: Choose one: • Choose a character. That character gets +2 to a basic power for
# its next use. • Until the end of the round, when you would generate resources, those resources are considered [wild] resources
# instead. Draw a card. » ("Draw a card" est lue comme faisant partie de la SECONDE puce : question en attente.)
# Cartes de reference : `ma009` America's Anger (temp `WhenUnitUseBasicPower` + `message.GainValue`), `ah001a` Hypermind
# (`CheckEffectGeneratedResources`). Le wild de la 2e puce est lu par `Icone(effect, "G")` (The Oracle peut le changer).


def GetAbilities() -> Sequence['Ability']:

    def master_plan(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        def bonus_a(perso: 'CardFace', pouvoir: str):
            def poser(targets) -> None:
                gain = {"ATK": getattr(perso, "GainAttack", None), "THW": getattr(perso, "GainThwart", None),
                        "DEF": getattr(perso, "GainDefense", None), "REC": getattr(perso, "GainRecover", None)}[pouvoir]
                if gain is None:
                    return
                # ⚠ `WhenUnitUseBasicPower` pose en temp ne part JAMAIS (vu au journal), `ThisGainKeyword` temporaire n'agit pas non
                # plus : on donne le +2 tout de suite (`GainThwart`...) et on le retire apres la prochaine utilisation
                # (`AfterUnitUseBasicPower`, qui, lui, part).
                gain(2, effect)

                def retirer(effect2: 'Effect', message2: 'Message.AfterUnitUseBasicPower') -> None:
                    gain(-2, effect2)
                perso.effect.RegisterTemp(
                    AbilityFactory.AfterUnitUseBasicPower(AbilityType.Temp2, "This", retirer, powers=[pouvoir]),
                    unregister_after_exec=True,
                    until_round_end=True,
                )
            return poser

        def puce_personnage(targets) -> None:
            persos = Worlds.GetOnFieldFriendlyCharacters(effect)
            perso = joueur.AskChooseFace(persos, effect) if persos else None
            if perso is None:
                return
            joueur.ChooseAbilities(
                effect,
                *[AbilityFactory.ForChoiceAbility(f"+2 {p}", bonus_a(perso, p)).SetHasNoTargetEffect()
                  for p in ("ATK", "THW", "DEF", "REC")],
            )

        def puce_wild(targets) -> None:
            couleur = Icone(effect, "G")
            identite = joueur.GetIdentity()

            def convertir(effect2: 'Effect', message2: 'Message.CheckEffectGeneratedResources') -> None:
                res = message2.res
                if res.val > 0:
                    message2.SetResources(Resources(couleur) * res.val, effect2)

            identite.effect.RegisterTemp(
                Ability(AbilityType.NonKeyword, Message.CheckEffectGeneratedResources,
                        [lambda e, m: m.GetToPlayer() == joueur], convertir),
                unregister_after_exec=False,
                until_round_end=True,
            )
            joueur.DrawUp(1, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Choose a character. That character gets +2 to a basic power for its next use.",
                                            puce_personnage).SetHasNoTargetEffect(),
            AbilityFactory.ForChoiceAbility("Until the end of the round, the resources you generate are considered wild resources. Draw a card.",
                                            puce_wild).SetHasNoTargetEffect(),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            master_plan,
        ).SetPlay(),
    ]
