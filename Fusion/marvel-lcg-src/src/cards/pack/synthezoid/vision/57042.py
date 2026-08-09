from . import *
def GetAbilities() -> Sequence['Ability']:
    def setup(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(Leader)
        for face in Worlds.GetSetAsideAreaCards(effect):
            if (face.paper.name in ('Dense', 'Intangible')):
                if (face.paper.name == 'Intangible'):
                    face.card.Flip(effect)
                face.CastTo(Attachment).AttachTo2(this, effect)
                return
    def after_villain_step(effect: 'Effect', message: 'Message.AfterResolveVillainPhaseStep') -> None:
        FlipMassForm(effect)
    return [AbilityFactory.WhenCardSetup('This', setup),
            AbilityFactory.AfterResolveVillainPhaseStep(AbilityType.ForcedResponse, 1, after_villain_step)]
