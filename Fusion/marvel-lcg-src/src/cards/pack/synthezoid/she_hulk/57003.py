from . import *
def GetAbilities() -> Sequence['Ability']:
    def setup(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(Leader)
        face = Search.EncounterCard(effect, None, include_discard_pile=False, include_set_aside=True, name='Superhuman Strength', card_type=Attachment)
        if face:
            face.CastTo(Attachment).AttachTo2(this, effect)
    def alter_ego_flips(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Leader)
        identity = message.trigger
        this.DealDamage([identity], 1, effect)
    return [AbilityFactory.WhenCardSetup('This', setup),
            AbilityFactory.AfterUnitChangeForm(AbilityType.ForcedResponse, None, alter_ego_flips, to_form=Hero)]
