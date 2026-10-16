from . import *

# Cloak of Shadows (x2) — TRAITRISE. Etoile de boost.
# When Revealed: Cloak each enemy. If you are not engaged with a minion, reveal
#   the topmost FOOT CLAN minion in the encounter discard pile.
# [star] Boost: After this activation resolves, cloak Shredder.
#
# Cartes de reference : `Faces.GiveStatus(Worlds.GetOnFieldEnemies(effect), ...)`
# (`ts005b`) ; `cw 56108` Arrest Order (`Worlds.GetEncounterDiscardPile(effect)
# .FindTopmost(CardFinder2(trait, Minion))`) ; `hs042` (`AfterThisActivation`).
#
# Mots-pieges : « EACH enemy » = vilain + TOUS les sbires en jeu ; « IF YOU are
# not engaged with a minion » : le joueur qui revele, lu APRES avoir pose les
# Cloaked ; « topmost » ; le boost cloake SHREDDER (pas « the villain »).


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        Faces.GiveStatus(Worlds.GetOnFieldEnemies(effect), "Cloaked", effect)
        if joueur.engaged_minions.GetSize() == 0:
            RevelerLePlusHautDeLaDefausse(effect, joueur, CardFinder2("FOOT CLAN", Minion))

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        message.AfterThisActivation(effect, lambda: Cloak(effect, TrouverShredder(effect)))

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
