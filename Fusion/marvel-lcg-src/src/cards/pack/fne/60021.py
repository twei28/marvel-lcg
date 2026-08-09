from . import *
def GetAbilities() -> Sequence['Ability']:
    def cloak_in_play(effect: 'Effect') -> int:
        face = Worlds.FindCardOnField(effect, CardFinder(name='Cloak', card_type=Ally))
        return (-1 if face else 0)
    return [*AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder(name='Cloak', card_type=Ally), acceleration_icon=-1),
            AbilityFactory.WhenAllyWouldTakeConsequentialDamage('This', update_damage=cloak_in_play)]
