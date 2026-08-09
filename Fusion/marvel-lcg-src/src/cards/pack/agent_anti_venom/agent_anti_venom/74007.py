from . import *

# Unlikely Allies — custom « DesignHacker »
# Hero Action: Exhaust this card and discard a card from your hand. If that
#   card's printed resource area includes:
#   [physical] - Drain 2 from an enemy.
#   [mental]   - Remove 2 threat from a scheme.
#   [energy]   - Draw 2 cards.
#   [wild]     - Choose 2 of the above.
#
# Une carte peut porter PLUSIEURS icones imprimees (Anti-Venom Goo en a deux) :
# chaque icone presente declenche donc sa ligne, et le joker en ouvre deux au
# choix, exactement comme le texte le dit (« includes »).

def GetAbilities() -> Sequence['Ability']:

    def _drain(initiator: 'Player', source: 'CardFace', effect: 'Effect') -> 'Ability':
        return AbilityFactory.ForChoiceAbility(
            "Drain 2 from an enemy",
            lambda targets:
                Drain(source, targets, 2, effect)
        ).SetTarget(Enemy)

    def _thwart(initiator: 'Player', source: 'CardFace', effect: 'Effect') -> 'Ability':
        return AbilityFactory.ForChoiceAbility(
            "Remove 2 threat from a scheme",
            lambda targets:
                source.RemoveThreatFromSchemes(targets, 2, effect)
        ).SetTarget(Scheme2)

    def _draw(initiator: 'Player', source: 'CardFace', effect: 'Effect') -> 'Ability':
        return AbilityFactory.ForChoiceAbility(
            "Draw 2 cards",
            lambda targets:
                initiator.DrawUp(2, effect)
        ).SetHasNoTargetEffect()

    def unlikely_allies(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        initiator = effect.GetInitiator()

        defaussees = [x for x in effect.targets]
        if not defaussees:
            return
        carte = defaussees[0]
        # `printed_resource` expose un compteur par couleur (r/b/y/g), lu AVANT
        # la defausse (cf. Redwing 53018).
        icones = carte.printed_resource
        Faces.DiscardAll(defaussees, effect)

        fabriques = {
            "r": _drain,
            "b": _thwart,
            "y": _draw,
        }

        for lettre, fabrique in fabriques.items():
            if getattr(icones, lettre, 0) > 0:
                initiator.ChooseAbilities(effect, fabrique(initiator, this, effect))

        if getattr(icones, "g", 0) > 0:
            for _ in range(2):
                initiator.MayChooseOneAbility(
                    effect,
                    *[f(initiator, this, effect) for f in fabriques.values()]
                )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            unlikely_allies,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget("YourHandCards", range=(1, 1)),
    ]
