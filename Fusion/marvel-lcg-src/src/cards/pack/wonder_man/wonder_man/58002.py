from . import *
def GetAbilities() -> Sequence['Ability']:
    def power_recycling(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Upgrade)
        player = this.GetControlByPlayer()
        face = message.played_face
        if not (face.card.area.flags.is_discards or face.IsInProcessingArea()):
            return
        this.TuckCardUnderHere(face, effect)
        identity = player.GetIdentity()
        identity.HealHealth(1, effect)
    def check_energy_event(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> bool:
        this = effect.this
        face = message.played_face
        if not Event.IsType(face):
            return False
        if not HasPrintedEnergy(face):
            return False
        if (message.to_player != this.GetControlByPlayer()):
            return False
        return (len(this.GetPlacedCardArea().Get()) < 3)
    return [AbilityFactory.AfterPlayerPlayedCard(AbilityType.Response, 'You', None, power_recycling, conditions=[check_energy_event])]
