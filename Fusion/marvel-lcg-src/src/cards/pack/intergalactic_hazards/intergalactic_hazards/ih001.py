from . import *

# Bounty Hunter — SBIRE CRIMINAL (×2). MNG 1 / ATQ 1 — 3 PV, 2 icones de boost.
#
# Patrol.
# [star] Forced Interrupt: When Bounty Hunter attacks, if you are confused,
#   they get +2 ATK for this attack.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - `Patrol` (mots-cles/patrol.md) et `Boost` (mots-cles/boost.md) : BASES
#   AUTOMATIQUES, lues dans `desc`. Aucun script.
# - Le `[star]` coiffe une Interruption Obligatoire (mots-cles/special.md) :
#   le type reste `ForcedInterrupt`, l'etoile ne fait que la designer.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « When X attacks, ... +N ATK for this attack » : bt008 et 19029 pour
#   `GainATKForThisAttack` sur le message d'attaque en cours.
# - Condition « si tu es desoriente » : le statut se lit sur l'identite du
#   joueur vise, `IsConfused()`.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « if YOU are confused » -> le joueur ATTAQUE, pas le sbire ni le premier
#   joueur : `message.GetAgainstPlayer()`.
# « THEY get +2 ATK » -> le sbire, pas le joueur.
# « FOR THIS ATTACK » -> ponctuel : le bonus ne survit pas a l'attaque.


def GetAbilities() -> Sequence['Ability']:

    def prime_sur_la_tete(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)

        joueur = message.GetAgainstPlayer()
        if not isinstance(joueur, Player):
            return
        identite = joueur.GetIdentity()
        if identite is None or not identite.IsConfused():
            return
        message.GainATKForThisAttack(2, effect)

    return [
        AbilityFactory.WhenUnitAttackYou(
            AbilityType.ForcedInterrupt,
            "This",
            prime_sur_la_tete,
        ),
    ]
