from . import *

# Skulk (x2, TMNT Standard 6/7 et 7/7) — TRAITRISE. Etoile de boost.
# When Revealed: Take 2 indirect damage and cloak the villain.
# [star] Boost: Deal this card to the first player as a facedown encounter card.
#
# Cartes de reference : `gob 02044` / `mts 21151` (`player.GetIdentity()
# .TakeIndirectDamage(this, n, effect)`) ; `tl015` (boost : `FaceCacheeAuPremierJoueur`).
#
# Mots-pieges : « TAKE 2 indirect damage » (le joueur qui revele) ; « cloak THE
# VILLAIN » ; le boost n'a RIEN d'autre : la carte est donnee, pas defaussee.


def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        joueur.GetIdentity().TakeIndirectDamage(this, 2, effect)
        Cloak(effect, Worlds.FindVillain(effect))

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        FaceCacheeAuPremierJoueur(effect, effect.this)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
