from . import *
def GetAbilities() -> Sequence['Ability']:
    def make_me_angry(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Upgrade)
        target = this.bind_face
        attacker = message.trigger
        if target and attacker:
            target.CastTo(Enemy).BasicAttack([attacker], effect)
        Faces.DiscardAll([this], effect)
    def check_attacked_she_hulk(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> bool:
        this = effect.this
        if not this.bind_face:
            return False
        attacker = message.trigger
        return (Hero.IsType(attacker) or Leader.IsType(attacker))
    return [AbilityFactory.CanPlayThisUpgradeCard(CardFinder(name='She-Hulk', card_type=Leader)),
            AbilityFactory.AfterUnitAttackEnd(AbilityType.ForcedResponse, None, make_me_angry, conditions=[check_attacked_she_hulk])]
