from . import *
# * The Batcave — SOUTIEN cout 2 [energy]. BAT FAMILY. LOCATION. « Bruce Wayne gets +2 REC. » Alter-Ego Action : exhaust The Batcave -> look at the top 5
# cards of your deck. Choose one and add it to your hand. Shuffle the remaining cards into your deck.
# Reference : sk043 (`GiveKeywordToInPlayWhenApplyThis(..., recover=)`), im001b (`GainCard`).
def GetAbilities() -> Sequence['Ability']:
    def batcave(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        dessus = list(joueur.player_deck.GetTops(5))
        if dessus:
            def prendre(choisie: Sequence['CardFace']) -> None:
                for face in choisie:
                    joueur.GainCard(face, effect)
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility("Choose a card to add to your hand", prendre)
                .SetTarget(dessus, range=(1, 1), not_move=True, not_shuffle=True),
            )
        joueur.player_deck.Shuffle(effect)
    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder(name="Bruce Wayne"), recover=2),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.AlterEgoAction, batcave).SetCostFunc(CostFunc.Exhaust("This")),
    ]
