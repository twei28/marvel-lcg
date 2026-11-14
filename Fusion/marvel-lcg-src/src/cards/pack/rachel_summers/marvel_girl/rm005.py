from . import *

# Psionic Blasts (x2) — EVENEMENT, cout 2 (energie), ATTACK. PSIONIC. THWART.
# Hero Action (attack/thwart): Deal 3 damage to the enemy. If this attack defeats an enemy, draw 1 card. Remove 3 threat
# from a scheme. If this removes the last threat on that scheme, draw 1 card.
#
# CARTES DE REFERENCE : `18020` Hit and Run (`SetLabel('attack', 'thwart')`, `SetTarget(Enemy)` + `SetTarget2(Scheme2)`),
# `16005` Root Stomp (`DealDamage(.., if_this_attack_defeats=fn)`), `RemoveThreatFromSchemes(.., if_this_remove_last_threat=fn)`.
#
# MOTS-PIEGES : « the enemy » (imprime ainsi) lu comme « an enemy » : le joueur choisit l'ennemi ; DEUX pioches distinctes.
def GetAbilities() -> Sequence['Ability']:
    def psionic_blasts(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        initiator = effect.GetInitiator()
        this.DealDamage(effect.targets, 3, effect, if_this_attack_defeats=lambda unite: initiator.DrawUp(1, effect))
        this.RemoveThreatFromSchemes(effect.targets2, 3, effect, if_this_remove_last_threat=lambda: initiator.DrawUp(1, effect))

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            psionic_blasts,
        ).SetPlay().SetLabel('attack', 'thwart')
        .SetTarget(Enemy)
        .SetTarget2(Scheme2),
    ]
