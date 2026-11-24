from . import *

# * Plantman : SBIRE (CRIMINAL. ELITE.), nemesis de Mantis. SCH 1, ATQ 3*, PV 4, boost 2. Stalwart. Toughness.
# [star] Forced Interrupt: When Plantman attacks, his attacks gain overkill.
# Forced Interrupt: When Plantman is defeated, give the villain a tough status card.
#
# CARTES DE REFERENCE
#  - `tc012` Persuader (fiche `mots-cles/piercing.md`) : `WhenUnitWouldAttack(.., op)` + `message.GainOverKill(effect)` sur le message d'ATTAQUE ; fiche `mots-cles/overkill.md`.
#  - `01143` Advanced Ultron Drone / `13028` Beetle : `WhenUnitBeDefeated(AbilityType.ForcedInterrupt, "This", op)` pour « When X is defeated » (Interruption forcee).
#  - `mots-cles/stalwart.md`, `mots-cles/toughness.md` : mots-cles lus NATIVEMENT dans `desc` (`Stalwart`, `Toughness`), aucun script pour eux.
#
# TEXTE CONTRE CODE
#  « When Plantman ATTACKS, HIS attacks gain overkill » : l'excedent d'une attaque qui abat un allie va a l'identite du joueur. « When Plantman is DEFEATED, give THE VILLAIN a tough status card » :
#  le vilain, pas un autre ennemi ; un vilain deja Robuste au plafond n'en recoit pas. Interruptions FORCEES : obligatoires. Chiffres : ATQ 3, PV 4, boost 2.


def GetAbilities() -> Sequence['Ability']:

    def plantman_attaque(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.GainOverKill(effect)

    def plantman_vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        vilain = Worlds.FindVillain(effect)
        if vilain is not None:
            Faces.GiveStatus([vilain], "Tough", effect)

    return [
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.ForcedInterrupt,
            "This",
            plantman_attaque,
        ),
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.ForcedInterrupt,
            "This",
            plantman_vaincu,
        ),
    ]
