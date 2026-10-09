from . import *

# hs209 Poisoned! (set de campagne experte)
# When Revealed : depense une ressource [energy] ou subis 2 degats.
# Piochee dans le deck d'un joueur : revelee immediatement par lui, sans remplacement.


def _pioche(effect: 'Effect', message: 'Message.AfterPlayerDrewCards') -> None:
    effect.this.Reveal(message.to_player, effect)


def GetAbilities() -> Sequence['Ability']:

    def empoisonner(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        joueur = message.GetToPlayer()
        if joueur is None:
            return
        identite = joueur.GetIdentity()

        def degats(cibles: Sequence['CardFace']) -> None:
            if identite is not None:
                identite.TakeDamage(this, 2, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbilityWithCost(
                Cost("Y"), "Spend an [energy] resource",
                conditions=[lambda e, m: PeutPayerEnergie(joueur)]),
            AbilityFactory.ForChoiceAbility("Take 2 damage", degats),
        )

    return [
        AbilityFactory.AfterPlayerDrewCards(AbilityType.Campaign, "AnyPlayer", "This", _pioche),
        AbilityFactory.WhenThisRevealed(None, empoisonner),
    ]
