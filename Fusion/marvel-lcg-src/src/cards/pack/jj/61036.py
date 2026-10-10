from . import *

# Innate Perception
# Starting. (You may add this card to your hand before drawing your starting hand.)
# Your hero gets +1 THW.
#
# Voir 61034 : le mot-cle « Starting » se code, il n'a pas de champ de donnees.

def GetAbilities() -> Sequence['Ability']:

    def starting(effect: 'Effect', message: 'Message.WhenGameBeginSetup') -> None:
        this = effect.this.CastTo(Upgrade)
        if not this.card.area.flags.is_player_deck:
            return
        player = this.GetControlByOrOwner()

        def ajouter(targets: Sequence['CardFace']) -> None:
            Faces.AddToHand([this], player, effect)

        player.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility('Add this card to your starting hand', ajouter),
        )

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(Hero, thwart=1),
        AbilityFactory.WhenGameBeginSetup(starting).NoOutOfPlayLimit(),
    ]
