from . import *

# Shadow Serpent — SBIRE NECROVERSE (×2). MNG 2 / ATQ 3 — 6 PV, 1 icone de
# boost + une etoile.
#
# [star] Shadow Serpent's attacks gain overkill.
# [star] Boost: Deal yourself 1 facedown encounter card.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - `Overkill` (mots-cles/overkill.md) : AUCUNE cle `desc`, toujours scripte,
#   et il se donne a l'ATTAQUE : `UnitAttackGainKeyword("This", overkill=True)`
#   (modele 50107b).
# - `Boost` etoile (mots-cles/boost.md) : `WhenCardBecomeBoost`, sans quoi le
#   moteur ne voit aucune etoile.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « [star] Boost: Deal yourself 1 facedown encounter card » : 24001 (The
#   Hood) et 21033 pour `player.DealEncounterCards(1, effect)`.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « X's ATTACKS gain overkill » -> permanent, sur les attaques du sbire.
# « Deal YOURSELF » -> le joueur qui retourne la carte de boost, donc celui
#   contre qui l'ennemi s'active.


def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)

        joueur = message.GetToPlayer()
        if joueur:
            joueur.DealEncounterCards(1, effect)

    return [
        AbilityFactory.UnitAttackGainKeyword("This", overkill=True),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
