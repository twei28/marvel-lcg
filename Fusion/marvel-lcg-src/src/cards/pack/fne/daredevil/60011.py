from . import *
def GetAbilities() -> Sequence['Ability']:
    def raising_hell(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        initiator = effect.GetInitiator()
        per_upgrade = 3 if initiator.GetIdentity().HasTrait('AERIAL') else 2
        for enemy in Worlds.FindCardsOnField(effect, card_type=Enemy):
            n = len(enemy.GetAttachedUpgrades())
            if n > 0:
                this.DealDamage([enemy], per_upgrade * n, effect)
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, raising_hell).SetPlay().SetLabel('attack')]
