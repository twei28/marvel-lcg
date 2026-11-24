from . import *

# Great Power — custom « Rainy » (ressource signature)
# Hero Response (attack): After you spend this card, deal 2 damage to an
#   enemy.
# Meme montage differe que The Power of Forgiveness (ah007) : l'effet est
# porte par l'identite, la ressource etant defaussee au moment du paiement.
#
# DECLENCHEUR : `AfterPlayerPlayedCard` (la carte payee a ete JOUEE), pas
# `AfterCardResolveAbility`. Rapport de bug n°115 (08/11/2026) : le moteur
# n'envoie `AfterEffectResolved` que pour une capacite d'evenement ; une
# amelioration ou un allie payes avec Great Power n'en ont aucune, et les
# 2 degats ne partaient jamais (seul l'evenement Thwip! marchait).

def GetAbilities() -> Sequence['Ability']:

    def great_power(effect: 'Effect', message: 'Message.WhenCardBeSpendAsResource') -> None:
        initiator = effect.GetInitiator()
        identity = initiator.GetIdentity()

        def apres_resolution(effect2: 'Effect', message2: 'Message.AfterPlayerPlayedCard') -> None:
            joueur = effect2.GetInitiator()
            ennemis = list(Worlds.FindCardsOnField(effect2, card_type=Enemy))
            if not ennemis:
                return
            joueur.ChooseAbilities(
                effect2,
                AbilityFactory.ForChoiceAbility(
                    "Deal 2 damage to an enemy",
                    lambda targets: effect2.this.DealDamage(list(targets), 2, effect2),
                ).SetTarget(Select.From(faces=ennemis), range=(1, 1)),
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
            # Pas de `until_resolve_effect` : il retirerait la reponse a la fin de la
            # resolution, AVANT l'envoi de `AfterPlayerPlayedCard`. La condition sur
            # `play_effect` la garde de tout autre jeu de carte.
            unregister_after_exec=True,
        )

    return [
        AbilityFactory.WhenYouSpendThisCardToPlay(
            AbilityType.HeroResponse,
            great_power,
        ),
    ]
