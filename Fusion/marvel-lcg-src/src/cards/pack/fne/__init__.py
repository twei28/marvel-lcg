from cards.pack import *

def DiscountAbility(value: int, traits: Sequence['CardFace.TRAITS']) -> 'Ability':
    def check_control_trait(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> bool:
        player = effect.this.GetControlByOrOwner()
        if not Player.IsType(player):
            return False
        for face in Worlds.FindCardsOnField(effect):
            if (face.GetControlBy() == player) and any(face.HasTrait(t) for t in traits):
                return True
        return False
    return AbilityFactory.ReduceCostToPlayThis(value, conditions=[check_control_trait])
