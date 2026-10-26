from . import *
# Entropic Subversion, manigance annexe nemesis. Menace de depart 3 par heros, boost 2.
#
# Forced Response: After a status card is discarded from a friendly character, if that status was:
#   Stunned  - Deal 2 damage to a friendly character.
#   Confused - Place 2 threat on the main scheme.
#
# Cartes de reference : 32004 Iron Will (`AfterStatusDiscardFrom(.., <qui>, "Tough", op)`) ; sk277 / ra001b (« a friendly character » =
# `SetTarget(Friend)`) ; 01182 (`PlaceThreatOnSchemes("MainScheme", n, effect)`).
# ⚠ DEUX capacites (une par statut) : le filtre de statut est un parametre de la fabrique, pas une condition.
def GetAbilities() -> Sequence['Ability']:
    def stunned(effect: 'Effect', message: 'Message.AfterStatusDiscardFrom') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        this.DealDamage(effect.targets, 2, effect)
    def confused(effect: 'Effect', message: 'Message.AfterStatusDiscardFrom') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        this.PlaceThreatOnSchemes("MainScheme", 2, effect)
    return [
        AbilityFactory.AfterStatusDiscardFrom(
            AbilityType.ForcedResponse,
            Friend,
            "Stunned",
            stunned,
        ).SetTarget(Friend),
        AbilityFactory.AfterStatusDiscardFrom(
            AbilityType.ForcedResponse,
            Friend,
            "Confused",
            confused,
        ),
    ]
