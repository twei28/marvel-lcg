from . import *

# No Quarter (TMNT Standard 1/7) — TRAITRISE. Etoile de boost.
# When Revealed: Discard an upgrade or support you control. If no cards were
#   discarded this way, daze your identity.
# [star] Boost: After this activation resolves, daze your identity.
#
# Cartes de reference : `01188` Caught Off Guard (`player.DiscardControlCards(
# effect, upgrade=True, support=True)`, rendu None si rien de defausse) ;
# `hs042` (`message.AfterThisActivation`). « Daze » : voir `Daze` (carte d'etat
# livree par le pack Baxter Stockman).
#
# Mots-pieges : « discard an upgrade OR support YOU CONTROL » (pas un allie) ;
# « If NO cards were discarded » = le retour de la defausse est None ; « daze YOUR
# identity ».


def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        if joueur.DiscardControlCards(effect, upgrade=True, support=True) is None:
            Daze(effect, joueur.GetIdentity())

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetToPlayer()
        message.AfterThisActivation(effect, lambda: Daze(effect, joueur.GetIdentity()))

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
