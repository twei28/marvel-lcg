from . import *
def GetAbilities() -> Sequence['Ability']:
    def check_overpay_card(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> bool:
        face = message.paying_for_effect.this
        return (face.paper.name in ('Ionic Blast', 'Active Altruism', 'Starstruck'))
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.CanGenerateResources(AbilityType.Resource, Resources('Y'), is_play_card=True, conditions=[check_overpay_card])]
