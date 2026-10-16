from . import *

# Purple Dragon Goons — SBIRE (set nemesis, x3). PURPLE DRAGONS. PV 3, ATQ 2,
# SCH 1, Boost 2.
# Guard. Patrol.
# When Revealed: Place a tough status card on the villain.
#
# MOTS-CLES : GUARD et PATROL — fiches `docs/reference/mots-cles/guard.md` et
# `patrol.md` (`desc.Guard = "1"`, `desc.Patrol = "1"`, AUCUN SCRIPT).
#
# CARTES DE REFERENCE
#  - `tl016` Foot Soldiers / `td015` : `WhenThisRevealed(None, op)` (recette §1)
#    sur un sbire ; `Faces.GiveStatus([vilain], "Tough", effect)` (recette §2).
#  - `Worlds.FindVillain(effect)` : le vilain actif.
#
# TEXTE CONTRE CODE
#  ⚠ « the VILLAIN » : le vilain actif, jamais un sbire ; un vilain qui a deja
#    Tough n'en recoit pas un second (`tough_max`, mots-cles/toughness.md).
#  ⚠ « When Revealed » : a la revelation seulement, pas quand le sbire revient en
#    jeu autrement.
#  ⚠ Trois exemplaires, UN card_id : `tc017` x3 dans le set nemesis.


def GetAbilities() -> Sequence['Ability']:

    def goons(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this, message)

        vilain = Worlds.FindVillain(effect)
        if vilain is not None:
            Faces.GiveStatus([vilain], "Tough", effect)

    return [
        AbilityFactory.WhenThisRevealed(None, goons),
    ]
