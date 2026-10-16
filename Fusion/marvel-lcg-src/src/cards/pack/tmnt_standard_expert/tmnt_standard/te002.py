from . import *

# Outmatched (x2, TMNT Standard 2/7 et 3/7) — TRAITRISE. Etoile de boost. Incite 2.
# When Revealed: Daze your identity.
# [star] Boost: After this activation resolves, daze your identity.
#
# Cartes de reference : `te001` (le boost) ; Incite 2 lu dans `desc`
# (`qsv 14025`, `sk101`).


def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Daze(effect, message.GetToPlayer().GetIdentity())

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetToPlayer()
        message.AfterThisActivation(effect, lambda: Daze(effect, joueur.GetIdentity()))

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
