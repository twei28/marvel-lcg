from . import *

# * Trl'k — SBIRE (paquet IMPOSTOR, face B). IMPOSTOR. REVEALED. SKRULL. 2 PV, SCH 2, ATQ 1.
# While the engaged player is engaged with another [[SKRULL]] minion Trl'k cannot take damage.
# When Revealed: Heal all damage from Trl'k and put him into play engaged with you.
#
# Cartes de reference :
#  - « When Revealed: Heal all damage from X and put it into play engaged with you » : **`gambit 37034`** Psionic Shield
#    (`HealthUnits([unite], "All", effect)`) et **`sk098`** (le sbire engage le joueur qui revele) ; helper `SbireImpostor()`.
# « cannot take damage while the engaged player is engaged with another SKRULL minion » : **`msm 05027`** Thomas Edison (MEME
# forme, avec `ThisCannotTakeDamageWhile(conditions=[...])` ; ici l'autre sbire doit etre SKRULL).
#
# ⚠ Mots-pieges : « heal ALL damage » (un allie retourne arrive blesse) ; « engaged with YOU » : le joueur qui revele
# (pour un allie retourne : celui qui le controlait avant, livret p. 16) ; la face sbire quitte le jeu vers la DEFAUSSE
# IMPOSTOR (livret p. 16, liaison `BindDiscardPile`).


def GetAbilities() -> Sequence['Ability']:
    def invulnerable(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        Unused(message)
        this = effect.this.CastTo(Minion)
        joueur = this.engaged_player
        if joueur is None:
            return False
        return any(m is not this and m.HasTrait("SKRULL") for m in joueur.GetEngagedMinions())

    return [
        *SbireImpostor(),
        AbilityFactory.ThisCannotTakeDamageWhile(conditions=[invulnerable]),
    ]
