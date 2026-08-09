from . import *

# Lovers Quarrel — custom « DesignHacker » (obligation de Cloak & Dagger)
# Give to the Cloak & Dagger player. Flip to alter-ego form, then choose one:
# - Exhaust Tyrone Johnson and Dagger -> remove Lovers Quarrel from the game.
# - You cannot change form during the next round -> discard this obligation.
# (Le texte d'origine flippe LES DEUX identités et paralyse Tyrone un round
#  entier ; adaptation mono-identité documentée au §9.)


def GetAbilities() -> Sequence['Ability']:

    def lovers_quarrel(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        player = message.GetGaveToPlayer()

        # Flip FORCÉ en alter-ego (contrairement à Chemotherapy, pas de choix).
        if player.IsHero():
            player.GetIdentity().ChangeToForm(AlterEgo, effect)

        dagger = TrouverDagger(effect, player)

        def penalite_puis_defausse(targets: Sequence['CardFace']) -> None:
            Players.CannotChangeFormDuringNextTurn(player, effect)
            Faces.DiscardAll([this], effect)

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust Tyrone Johnson and Dagger → remove Lovers Quarrel from the game",
                lambda t: Faces.RemoveAllFromGame([this], effect),
                condition=(player.IsAlterEgo() and dagger is not None),
            ).SetCostFunc(CostFunc.Exhaust("YourIdentity"))
            .SetCostFunc(CostFunc.Exhaust(
                name=NOM_DAGGER,
                card_type=Hero,
                from_where=["YouControlCards"])),
            AbilityFactory.ForChoiceAbility(
                "You cannot change form during the next round. Discard this obligation",
                penalite_puis_defausse,
            ),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            lovers_quarrel
        )
    ]
