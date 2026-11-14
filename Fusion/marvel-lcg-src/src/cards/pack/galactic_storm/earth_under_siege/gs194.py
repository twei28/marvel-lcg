from . import *

# Secret Invasion — MANIGANCE ANNEXE (ensemble Veranke). Hinder 1.
# Forced Interrupt: When an ally leaves play, place 1 acceleration token here.
#
# Cartes de reference :
#  - « When an ally leaves play, place 1 acceleration token here » : `AbilityFactory.AfterCardLeavePlay`
#    (modele gs119 Majestrix's Verdict pour le declencheur « leaves play ») +
#    `CanAccelerationToken.PlaceAccelerationToken` (modele natif, `scenario.py` l'utilise deja pour le
#    jeton d'acceleration standard d'un deck rencontre remelange).
#
# ⚠ Mots-pieges : « AN ally » = n'importe quel allie de n'importe quel joueur (pas seulement ceux du
# joueur qui controle cette manigance) ; « leaves play » couvre la defausse, le retrait, la remise en main
# — pas seulement la defaite au combat.


def GetAbilities() -> Sequence['Ability']:

    def allie_quitte(effect: 'Effect', message: 'Message.AfterCardLeavePlay') -> None:
        Unused(message)
        this = effect.this.CastTo(EncounterSideScheme)
        this.PlaceAccelerationToken(1, effect)

    return [
        AbilityFactory.AfterCardLeavePlay(
            AbilityType.ForcedInterrupt,
            CardFinder(card_type=Ally),
            allie_quitte,
        ),
    ]
