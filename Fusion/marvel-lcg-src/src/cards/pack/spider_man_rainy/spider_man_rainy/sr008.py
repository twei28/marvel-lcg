from . import *

# Great Responsibility — custom « Rainy » (ressource signature)
# Hero Response (thwart): After you spend this card, remove 2 threat from a
#   scheme. Montage identique a Great Power (sr007).
#
# DECLENCHEUR : `AfterPlayerPlayedCard` (la carte payee a ete JOUEE), pas
# `AfterCardResolveAbility`. Rapport de bug n°115 (08/11/2026, vu sur sr007) :
# le moteur n'envoie `AfterEffectResolved` que pour une capacite d'evenement ;
# une amelioration ou un allie payes avec cette carte n'en ont aucune, et la
# reponse ne partait jamais.

def GetAbilities() -> Sequence['Ability']:

    def great_responsibility(effect: 'Effect', message: 'Message.WhenCardBeSpendAsResource') -> None:
        initiator = effect.GetInitiator()
        identity = initiator.GetIdentity()

        def apres_resolution(effect2: 'Effect', message2: 'Message.AfterPlayerPlayedCard') -> None:
            joueur = effect2.GetInitiator()

            def retirer(targets: Sequence['CardFace']) -> None:
                effect2.this.RemoveThreatFromSchemes(list(targets), 2, effect2)

            joueur.ChooseAbilities(
                effect2,
                AbilityFactory.ForChoiceAbility(
                    "Remove 2 threat from a scheme",
                    retirer,
                ).SetTarget(Scheme2, range=(1, 1)),
            )

        identity.effect.RegisterTemp(
            AbilityFactory.AfterPlayerPlayedCard(
                AbilityType.Response,
                "You",
                CardFace,
                apres_resolution,
                conditions=[
                    lambda effect2, message2: message2.play_effect == message.for_effect,
                ],
            ),
            # Pas de `until_resolve_effect` : il retirerait la reponse avant l'envoi de
            # `AfterPlayerPlayedCard` ; la condition sur `play_effect` la garde.
            unregister_after_exec=True,
        )

    return [
        AbilityFactory.WhenYouSpendThisCardToPlay(
            AbilityType.HeroResponse,
            great_responsibility,
        ),
    ]
