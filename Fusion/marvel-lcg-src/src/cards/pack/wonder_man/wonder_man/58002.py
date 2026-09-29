from . import *
def GetAbilities() -> Sequence['Ability']:
    def power_recycling(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Upgrade)
        player = this.GetControlByPlayer()
        face = message.played_face
        # Errata RRG 1.8 (MC4DB, 29/09/2026) : « -> » devient « Then, ». Le tuck
        # n'est plus un cout : plafond atteint (« Max 3 cards tucked here ») ou
        # evenement deja parti ailleurs, on ne glisse rien MAIS on soigne
        # quand meme.
        if (len(this.GetPlacedCardArea().Get()) < 3
                and (face.card.area.flags.is_discards or face.IsInProcessingArea())):
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
        return message.to_player == this.GetControlByPlayer()
    return [AbilityFactory.AfterPlayerPlayedCard(AbilityType.Response, 'You', None, power_recycling, conditions=[check_energy_event])]
