from . import *

# * H.E.R.B.I.E. — custom « DesignHacker »
# Action: Exhaust H.E.R.B.I.E. -> discard X cards from your hand, then draw X
# cards.
# Action: Exhaust then discard H.E.R.B.I.E. -> draw X cards, then discard X
# cards from your hand.
#
# LENIENT : la carte ne chiffre pas X. Il est joué comme « toute ta main »
# (défausser la main puis repiocher autant), la lecture la plus naturelle
# d'un cycleur sans limite imprimée.

def GetAbilities() -> Sequence['Ability']:

    def defausser_puis_piocher(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        initiator = effect.GetInitiator()
        mains = list(initiator.hand_cards.Get())
        if not mains:
            return
        nombre = len(mains)
        Faces.DiscardAll(mains, effect)
        initiator.DrawUp(nombre, effect)

    def piocher_puis_defausser(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)

        initiator = effect.GetInitiator()
        nombre = len(list(initiator.hand_cards.Get()))
        Faces.DiscardAll([this], effect)
        if nombre <= 0:
            return
        initiator.DrawUp(nombre, effect)
        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Discard that many cards from your hand",
                lambda targets: None
            ).SetCostFunc(CostFunc.Discard(
                "YourHandCards",
                range=(nombre, nombre))),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            defausser_puis_piocher
        ).SetCostFunc(CostFunc.Exhaust("This")),

        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            piocher_puis_defausser
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
