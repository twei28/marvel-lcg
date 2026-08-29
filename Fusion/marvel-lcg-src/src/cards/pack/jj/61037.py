from . import *

# Innate Inspiration
# Starting. Each ally you control gets +1 hit point.
#
# Effet permanent sur un ensemble variable de cartes : c'est exactement ce que
# fait « Team Training » (04016), qui utilise la fabrique dediee plutot qu'une
# boucle manuelle. Elle suit d'elle-meme les allies qui entrent et sortent.

def GetAbilities() -> Sequence['Ability']:

    def starting(effect: 'Effect', message: 'Message.WhenGameBeginSetup') -> None:
        this = effect.this.CastTo(Upgrade)
        if not this.card.area.flags.is_player_deck:
            return
        player = this.GetControlByOrOwner()
        Faces.AddToHand([this], player, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            Ally,
            control_by="You",
            health=1,
        ),
        # « Starting » : voir 61034, le mot-cle se code.
        AbilityFactory.WhenGameBeginSetup(starting).NoOutOfPlayLimit(),
    ]
