from . import *

# Stairs : ATTACHEMENT (nemesis 3/5), boost 3. SCH ★ ATQ ★ (aucun bonus chiffre : `desc` a 0*).
# Attach to the minion with the highest remaining hit points. Otherwise, this card gains surge.
# [star] Forced Interrupt: When the attached minion would activate, discard Stairs instead.
#
# CARTES DE REFERENCE
#  - `04119` Neurological Implants : `AttachToFaceWhenPutIntoPlay(Minion, most_remaining_hp=True, if_cannot_gain_surge=True)` (texte identique).
#  - `wd161` Webbed : `WhenEnemyWouldActivate(ForcedInterrupt, "AttachedEnemy", fn)` + `message.SetBeInstead(effect)` + `Faces.DiscardAll([this], effect)` (« discard X instead »).
#  - `sv015` Cosmic Power / `pu091a` : une boite SCH/ATQ imprimee « ★ » seule = `desc.ATK+ = "0*"` (valeur 0, texte propre).
#
# TEXTE CONTRE CODE
#  « the minion with the HIGHEST remaining hit points » -> PV restants, pas PV imprimes. « Otherwise, this card gains SURGE » -> aucun sbire en jeu. « When the attached minion
#    WOULD activate, discard Stairs INSTEAD » : l'activation est remplacee (le sbire ne frappe ni ne manigance cette fois) ; Stairs est defaussee.
#  Chiffres : boost 3, bonus SCH/ATQ 0.


def GetAbilities() -> Sequence['Ability']:

    def stairs(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> None:
        this = effect.this.CastTo(Attachment)
        message.SetBeInstead(effect)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            Minion,
            most_remaining_hp=True,
            if_cannot_gain_surge=True,
        ),
        AbilityFactory.WhenEnemyWouldActivate(
            AbilityType.ForcedInterrupt,
            "AttachedEnemy",
            stairs,
        ),
    ]
