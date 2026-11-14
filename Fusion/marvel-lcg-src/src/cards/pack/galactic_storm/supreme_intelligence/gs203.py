from . import *

# * Ren-Varr — SBIRE (Supreme Intelligence). GENIUS. KREE. SCH 2, ATK 1, 5 PV, 2 icones de boost, icone
# d'ACCELERATION au centre de la boite de texte.
# Vulnerable.
# When Defeated: Give the villain a tough status card.
#
# Cartes de reference :
#  - **`sm/sandman/27067`** : `WhenUnitBeDefeated(WhenDefeated, "This", op)`.
#  - **`next_evol/40156`** Impervious : `Faces.GiveStatus([villain], "Tough", effect)` = « give the villain a
#    tough status card ».
#  - Vulnerable et Acceleration : bases AUTOMATIQUES (`desc.Vulnerable`, `desc.Acceleration`, fiches
#    vulnerable.md / acceleration.md), aucun code.
#
# ⚠ Mots-pieges : « When DEFEATED » : un Ren-Varr DEFAUSSE par Vulnerable (sonne ou desoriente) n'est pas
# vaincu (livret p.3) et ne donne rien ; « the VILLAIN » ; mechant deja Tenace : aucune seconde carte
# (plafond natif).


def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        Unused(message)
        mechant = LeMechant(effect)
        if mechant is not None:
            Faces.GiveStatus([mechant], "Tough", effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
    ]
