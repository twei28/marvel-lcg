from . import *

# * Muse — SBIRE UNIQUE. CRIMINAL. SCH 1★, ATQ 2★, 4 PV, Boost ★, Acceleration 2.
# ★ Forced Response : After Muse activates, attach him to an unoccupied location, if able. (He remains in play.)
# Forced Interrupt : When a player enters Muse's location, he engages them.
# ★ Boost : Reveal this card.
#
# Cartes de reference : pu013 (attache / engage), `AbilityFactory.AfterEnemyActivationEnd` (activate.py), sk115 (`WhenCardBecomeBoost("This",
# RevealThisCard)`).
# ⚠ « After Muse ACTIVATES » (attaque ou manigance) ; le joueur contre qui il s'est active choisit le lieu ; « if able » : sinon il reste engage ;
# ★ = capacite de la carte (pas un mode expert) ; Acceleration 2 : desc.

def GetAbilities() -> Sequence['Ability']:

    def s_attache(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        if effect.this.IsInPlay():
            AttacherAuLieuInoccupe(effect, effect.this, SbireEngagePar(effect.this))

    return [
        AbilityFactory.AfterEnemyActivationEnd(AbilityType.ForcedResponse, "This", s_attache),
        EngageQuandOnEntreDansSonLieu(),
        AbilityFactory.WhenCardBecomeBoost("This", RevealThisCard),
    ]
