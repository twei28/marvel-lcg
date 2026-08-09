from cards.pack import *


def ResolveInitiateProtocol(effect: 'Effect') -> None:
    """Résout la capacité « Initiate Protocol » du héros Albert de l'initiateur.

    L'interdiction posée par l'obligation Counterpart Elimination est
    vérifiée dans le gestionnaire Special du héros (62001a).
    """
    initiator = effect.GetInitiator()
    identity = initiator.GetIdentity()
    initiator.ResolveSpecialAbility([identity], effect)
