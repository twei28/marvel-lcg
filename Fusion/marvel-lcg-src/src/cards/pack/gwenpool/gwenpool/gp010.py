from . import *

# THE END — custom « ekAugust » (obligation de Gwenpool)
# Give to the Gwendolyn Poole player.
# You cannot use speech bubbles from Gwenpool cards.
#   (vérifié dans ResolveBlank, __init__.py du set)
# Alter-Ego Action: Exhaust Gwendolyn Poole and discard Unbelievable
# Gwenpool -> remove THE END from the game.

def GetAbilities() -> Sequence['Ability']:

    def the_end(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        # La carte reste en jeu : son interdiction est permanente tant
        # qu'elle n'est pas retirée de la partie.
        pass

    def retirer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Obligation)

        ug = Worlds.FindCardOnField(effect, name="Unbelievable Gwenpool", card_type=Upgrade)
        if not ug:
            return
        Faces.DiscardAll([ug], effect)
        Faces.RemoveAllFromGame([this], effect)

    def ug_en_jeu(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        return Worlds.FindCardOnField(effect, name="Unbelievable Gwenpool", card_type=Upgrade) is not None

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            the_end
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            retirer,
            conditions=[ug_en_jeu],
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
    ]
