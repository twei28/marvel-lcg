from . import *

# * Overdrive — SBIRE UNIQUE. CRIMINAL. VEHICLE. SCH 0, ATQ 2, 3 PV, Boost 1. Quickstrike. Amplify 1.
# Forced Response : After the round ends, attach Overdrive to an unoccupied location, if able. (He remains in play.)
# Forced Interrupt : When a player enters Overdrive's location, he engages them.
#
# Cartes de reference : `Ville.AttacherSbire / DegagerSbire` (brique M5 : sbire glisse sous le lieu, PV gardes), `AbilityFactory.AfterRoundEnd`
# (turn_phase.py), `EngageQuandOnEntreDansSonLieu` (module du set). Quickstrike / Amplify : desc.
# ⚠ « After the round ENDS » : fin du round, pas de la phase ; « if able » : aucun lieu libre = il reste avec son joueur ; le joueur engage choisit
# le lieu ; « he engages THEM » : le joueur qui entre.

def GetAbilities() -> Sequence['Ability']:

    def s_attache(effect: 'Effect', message: 'Message.AfterRoundEnd') -> None:
        AttacherAuLieuInoccupe(effect, effect.this, SbireEngagePar(effect.this))

    def en_jeu_engage(effect: 'Effect', message: 'Message2') -> bool:
        return effect.this.IsInPlay() and SbireEngagePar(effect.this) is not None

    return [
        AbilityFactory.AfterRoundEnd(AbilityType.ForcedResponse, s_attache, conditions=[en_jeu_engage]),
        EngageQuandOnEntreDansSonLieu(),
    ]
