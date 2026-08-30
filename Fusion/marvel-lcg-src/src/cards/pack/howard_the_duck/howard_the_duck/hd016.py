from . import *

# * Iron Suit — ARMOR. TECH — amelioration, cout 2
# Action: Exhaust Iron Suit → move 1 threat from a scheme to here.
# Hero Action: Exhaust Iron Suit and remove X threat from here → deal X damage
#   to a minion or remove X threat from a scheme.
#
# « move 1 threat from a scheme TO HERE » : la menace posee sur une carte
# JOUEUR est un JETON `'threat'`, pas un compteur (deux stocks distincts,
# rappel explicite dans `tools/test_capacites.py`, cle `jetons`). Modele exact
# aos/nick_fury/50046.py (Secret Agent) : `this.RemoveThreatFromSchemes
# (targets, 1, effect)` rend le nombre REELLEMENT retire, puis
# `Faces.PlaceTokensOn([this], <ce nombre>, 'threat', effect)`. On n'utilise
# PAS `Scheme2.MoveThreat` (scheme.py:155) : sa destination doit etre une
# manigance (`PlaceThreatOnSchemes`), jamais une amelioration.
#
# « remove X threat from here → deal X damage to a MINION or remove X threat
# from a scheme » : X est declare par le joueur dans les bornes de ce que la
# carte porte (`initiator.DeclareNumber(1, this.GetTokens('threat'))`, modele
# aos/nick_fury/50043.py Eyepatch Camera qui borne de la meme facon), le
# retrait est un COUT paye avant l'effet, puis un choix a 2 branches
# (`ChooseAbilities`, modele ok004/ok019). Noter la portee ASYMETRIQUE du
# texte imprime : la branche degats vise un SBIRE (`Minion`, pas `Enemy` —
# le vilain n'est pas une cible legale), la branche menace vise n'importe
# quelle manigance (`Scheme2`).


def GetAbilities() -> Sequence['Ability']:

    def deplacer_menace(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)

        if not effect.targets:
            return
        deplacee = this.RemoveThreatFromSchemes(effect.targets, 1, effect)
        if deplacee:
            Faces.PlaceTokensOn([this], deplacee, 'threat', effect)

    def depenser_menace(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        disponible = this.GetTokens('threat')
        if disponible <= 0:
            return

        x = initiator.DeclareNumber(1, disponible)
        if x <= 0:
            return
        Faces.RemoveTokensOn([this], x, 'threat', effect)

        def frapper(targets: Sequence['CardFace']) -> None:
            if targets:
                this.DealDamage(targets, x, effect)

        def nettoyer(targets: Sequence['CardFace']) -> None:
            if targets:
                this.RemoveThreatFromSchemes(targets, x, effect)

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Deal X damage to a minion",
                frapper,
            ).SetLabel('attack').SetTarget(Minion),
            AbilityFactory.ForChoiceAbility(
                "Remove X threat from a scheme",
                nettoyer,
            ).SetLabel('thwart').SetTarget(Scheme2),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            deplacer_menace,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Scheme2),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            depenser_menace,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
