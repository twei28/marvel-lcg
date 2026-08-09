from . import *
def GetAbilities() -> Sequence['Ability']:
    def with_ionic_physiology(effect: 'Effect', message: 'Message.WhenPlayerSelectHero') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)
        initiator = effect.GetInitiator()
        for area in (initiator.set_aside_deck, initiator.additional_discard_pile):
            for face in list(area.Get()):
                if (face.paper.name == 'Ionic Physiology'):
                    face.CastTo(Upgrade).PutIntoPlay(initiator, effect, under_control=True)
                    return
    return [AbilityFactory.BeginGameWithSetAside(['58002'], with_ionic_physiology)]
