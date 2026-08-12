from . import *

# Analysis Paralysis (obligation) — custom « Rainy »
# Give to the Amadeus Cho player.
# You may flip to alter-ego form. Choose:
#  • Exhaust Amadeus Cho → remove Analysis Paralysis from the game.
#  • You are stunned and confused. If you were already stunned and confused,
#    this card gains surge. Discard this obligation.
#
# Le « You may flip to alter-ego form » est une FACILITE offerte avant le choix,
# pas une obligation : sans elle, un joueur en forme heros ne pourrait jamais
# prendre la premiere option, qui demande d'epuiser l'alter-ego.
#
# Piege connu : la methode « change de forme » sans argument n'existe pas sur
# les identites, c'est bien `ChangeToForm(AlterEgo, effect)` qu'il faut. Ni
# test_cards ni test_capacites ne l'attrapent quand l'appel est derriere un
# choix optionnel — seul `verifier_api_cartes.py` le voit.

def GetAbilities() -> Sequence['Ability']:

    def analysis_paralysis(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)

        joueur = message.GetGaveToPlayer()
        if joueur is None:
            return

        identite = joueur.GetIdentity()

        if joueur.IsHero() and identite is not None:
            joueur.MayChooseOneAbility(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Flip to alter-ego form",
                    lambda targets: identite.ChangeToForm(AlterEgo, effect),
                ),
            )

        def subir(targets: Sequence['CardFace']) -> None:
            identite_courante = joueur.GetIdentity()
            if identite_courante is None:
                return
            deja = identite_courante.IsStunned() and identite_courante.IsConfused()
            Faces.GiveStatus([identite_courante], "Stunned", effect)
            Faces.GiveStatus([identite_courante], "Confused", effect)
            if deja:
                ThisCardGainSurge(effect)
            Faces.DiscardAll([this], effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust Amadeus Cho -> remove Analysis Paralysis from the game",
                lambda targets: Faces.RemoveAllFromGame([this], effect),
                condition=joueur.IsAlterEgo(),
            ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
            AbilityFactory.ForChoiceAbility(
                "You are stunned and confused",
                subir,
            ),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            analysis_paralysis,
        ),
    ]
