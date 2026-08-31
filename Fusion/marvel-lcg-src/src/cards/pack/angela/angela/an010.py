from . import *

# Banished from Asgard — obligation. Boost 2. GiveTo: Aldrif Odinsdottir.
# Give to the Aldrif Odinsdottir player.
# You may flip to alter-ego form. Choose:
#  • Exhaust Aldrif Odinsdottir -> remove Banished from Asgard from the game.
#  • Discard 1 ASGARD card you control. You are stunned. If no card was
#    discarded this way, this card gains surge. Discard this obligation.
#
# Carte de reference : 48026 Crisis of Faith (pack ncrawler), squelette exact.
#
# ⚠ CONTRASTE AVEC vp011 One Too Many Voices (pack venompool), portee il y a
# quelques heures : celle-la disait « You MUST flip » et forcait le changement
# de forme. Celle-CI dit « You MAY flip » — on repasse donc bien par le helper
# `YouMayFlipToYourAlterEgoForm`, comme 48026 et 16053. Le mot compte.
#
# ⚠ Le surge n'est pas conditionne au choix de la puce mais au fait qu'AUCUNE
# carte ASGARD n'ait ete defaussee (« If no card was discarded THIS WAY ») :
# un joueur qui choisit la seconde puce sans carte ASGARD declenche le surge.
# L'etourdissement, lui, tombe dans tous les cas de cette puce.

def GetAbilities() -> Sequence['Ability']:

    def banished(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        player = message.GetGaveToPlayer()
        if player is None:
            return

        YouMayFlipToYourAlterEgoForm(player, effect)

        def defausser_asgard(targets: Sequence['CardFace']) -> None:
            cartes = [f for f in targets if f is not None]
            if cartes:
                Faces.DiscardAll(cartes, effect)
            else:
                this.GainSurge(1, effect)
            identite = player.GetIdentity()
            if identite is not None:
                Faces.GiveStatus([identite], "Stunned", effect)
            Faces.DiscardAll([this], effect)

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust Aldrif Odinsdottir → remove Banished from Asgard from the game",
                lambda targets:
                    Faces.RemoveAllFromGame([this], effect),
                condition=player.IsAlterEgo(),
            ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
            AbilityFactory.ForChoiceAbility(
                "Discard 1 [[ASGARD]] card you control. You are stunned. Discard this obligation",
                defausser_asgard,
            ).SetTarget(CardFinder(trait="ASGARD"), range=("Zero", 1),
                        from_where=["YouControlCards"], canbe_discard=True),
            AbilityFactory.Otherwise(defausser_asgard),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            banished
        ),
    ]
