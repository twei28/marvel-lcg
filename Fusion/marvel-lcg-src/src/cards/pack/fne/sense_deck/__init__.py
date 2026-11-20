from cards.pack import *
from cards.pack.fne.daredevil import SENSE_DECK_IDS
Unused(SENSE_DECK_IDS)
ENEMY_OR_SCHEME = (CardFinder(card_type=Enemy) | CardFinder(card_type=Scheme2))
def SenseDiscard(this: 'CardFace', by_effect: 'Effect') -> None:
    Faces.DiscardAll([this], by_effect)
def DerniereMenaceDuComplotPrincipal(ability_type: 'AbilityType', operation: 'Callable[..., None]') -> 'Ability':
    # « remove the last threat from attached scheme » sur un complot PRINCIPAL : il n'est jamais vaincu
    # (`RemoveThreatInternal` exclut `MainScheme`), donc `WhenSchemeBeDefeated` ne part pas. On lit le retrait lui-meme.
    def check(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> bool:
        this = effect.this
        hote = this.bind_face
        if (message.trigger != hote) or (not MainScheme.IsType(hote)):
            return False
        if message.value < hote.CastTo(Scheme2).threat:
            return False
        joueur = message.by_face.GetControlBy()
        if not Player.IsType(joueur):
            joueur = message.by_effect.initiator
        return joueur == this.GetControlByPlayer()
    return AbilityFactory.WhenSchemeWouldRemoveThreat(ability_type, None, operation, conditions=[check])
