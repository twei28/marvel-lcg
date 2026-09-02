from . import *

# * Necro-Raven Gestalt — SBIRE ELITE NECROVERSE, mis de cote au setup.
# MNG 3 / ATQ 3 — 5 PV par joueur, 4 icones de boost.
#
# Guard. Patrol.
# Forced Interrupt: When Necro-Raven Gestalt would be defeated, instead of
#   discarding it, set it aside, out of play instead.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - `Guard` (mots-cles/guard.md) et `Patrol` (mots-cles/patrol.md) : BASES
#   AUTOMATIQUES, lues dans `desc`. Aucun script. Modele dd015, qui porte les
#   deux et dont le module le dit noir sur blanc.
# - `Boost` (mots-cles/boost.md) : `desc.Boost = "4"`, base automatique.
# - `ELITE` est un TRAIT, pas un mot-cle : il vit dans `traits`.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « When X would be defeated, ... instead » : an014 (Disir, pack angela),
#   jumelle exacte — `WhenUnitWouldBeDefeated(ForcedInterrupt, "This", ...)`
#   puis `message.SetBeInstead(effect)` avant de deplacer la carte. Disir
#   retourne au deck de rencontre, le Gestalt part en reserve.
# - « set it aside, out of play » : `Faces.SetAside([this], effect)`
#   (operate/faces.py:158), la meme que le Setup du complot 1A.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « WOULD be defeated » -> Interruption : on remplace l'evenement AVANT qu'il
#   se produise, sinon la carte est deja partie a la defausse.
# « INSTEAD of discarding it » -> remplacement, pas addition : sans le
#   `instead`, le sbire irait a la defausse ET dans la reserve.
# « set it aside, OUT OF PLAY » -> la reserve, d'ou Necro-Raven (gb010) le
#   rappellera : c'est le va-et-vient qui fait le sel du scenario. Un sbire
#   defausse serait perdu.


def GetAbilities() -> Sequence['Ability']:

    def au_lieu_de_mourir(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(Minion)

        message.SetBeInstead(effect)
        Faces.SetAside([this], effect)

    return [
        AbilityFactory.WhenUnitWouldBeDefeated(
            AbilityType.ForcedInterrupt,
            "This",
            au_lieu_de_mourir,
        ),
    ]
