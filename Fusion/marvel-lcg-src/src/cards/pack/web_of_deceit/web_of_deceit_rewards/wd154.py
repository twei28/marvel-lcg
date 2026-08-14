from . import *

# Spider-Bots

def GetAbilities() -> Sequence['Ability']:

    def essaim(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        # « Hero Action (thwart): Exhaust Spider-Bots and remove 1 bot counter
        # from here → remove threat from a scheme equal to the total number of
        # printed [mental] and [wild] resources in your hand. »
        this = effect.this.CastTo(Upgrade)
        joueur = effect.GetInitiator()

        # `printed_resource` expose un compteur par couleur, lu AVANT tout
        # effet : c'est bien « printed » que la carte demande.
        valeur = 0
        for carte in joueur.hand_cards.Get():
            icones = carte.printed_resource
            valeur += icones.b + icones.g
        if valeur > 0:
            this.RemoveThreatFromSchemes(effect.targets, valeur, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            essaim
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'bot'))
        .SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
