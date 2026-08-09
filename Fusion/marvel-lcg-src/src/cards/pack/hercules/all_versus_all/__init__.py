from cards.pack import *
def RevealAllVersusAll(effect: 'Effect', player: 'Player') -> None:
    if Worlds.FindCardOnField(effect, name='All Versus All'):
        return
    face = Search.EncounterCard(effect, player, include_discard_pile=True, include_set_aside=True, name='All Versus All', card_type=EncounterSideScheme)
    if face:
        face.Reveal(player, effect)
def PlaceThreatOnAllVersusAll(effect: 'Effect', this: 'CardFace', size: int) -> bool:
    scheme = Worlds.FindCardOnField(effect, name='All Versus All', card_type=EncounterSideScheme)
    if scheme:
        this.PlaceThreatOnSchemes([scheme], size, effect)
        return True
    return False
