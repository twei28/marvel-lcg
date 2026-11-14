from . import *


def GetAbilities() -> Sequence['Ability']:
    def emp_rounds(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        joueur = effect.GetInitiator()

        def statut(nom: str, melanger: bool):
            def fn(cibles: Sequence['CardFace']) -> None:
                if melanger:
                    Faces.ShuffleAllTo([this], joueur.player_deck, effect)   # « You may shuffle this card into your deck »
                Faces.GiveStatus(list(cibles), nom, effect)
            return fn

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Stun a minion", statut("Stunned", False)).SetTarget(Minion, canbe_stunned=True),
            AbilityFactory.ForChoiceAbility("Confuse a minion", statut("Confused", False)).SetTarget(Minion, canbe_confused=True),
            AbilityFactory.ForChoiceAbility("Shuffle this card into your deck → stun the villain", statut("Stunned", True)).SetTarget(Villain, canbe_stunned=True),
            AbilityFactory.ForChoiceAbility("Shuffle this card into your deck → confuse the villain", statut("Confused", True)).SetTarget(Villain, canbe_confused=True),
        )

    return [
        RessourceEnhancedCombatSense(CostFunc.Exhaust("This")),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            emp_rounds,
            conditions=[ActionPayable("Y")],
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCost(Cost("Y")),
    ]
