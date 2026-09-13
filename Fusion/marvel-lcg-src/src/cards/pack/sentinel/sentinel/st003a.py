from . import *

# * Arms (Intact) — COMPONENT. INTACT. TECH.
# Permanent. Setup.
# Hero Action (attack): Exhaust Arms (Intact) → deal 1 damage to an enemy.
#
# Cartes de reference :
#  - `av009` Bear Arms : action de heros ETIQUETEE `attack` sur une
#    amelioration, avec inclinaison en cout.
#  - `nt003b` : `this.DealDamage(effect.targets, 1, effect)`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « <i>(attack)</i> » : l'etiquette compte. `SetLabel('attack')` fait des
#    degats une VRAIE attaque, donc soumise a riposte, Coriace et Exposed.
#    Sans elle, la riposte ne se declencherait pas.
#  - « an enemy » : une seule cible, vilain ou sbire.
#  - C'est le COMPONENT qui inflige les degats, pas le heros : aucune
#    statistique d'attaque n'intervient.


def GetAbilities() -> Sequence['Ability']:

    def coup_de_poing(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        this.DealDamage(effect.targets, 1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            coup_de_poing,
        ).SetLabel('attack')
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Enemy),
    ]
