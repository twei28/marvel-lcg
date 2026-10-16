from . import *

# Pounce (x2) — EVENEMENT, cout 0, [mental]. ATTACK.
# Hero Action (attack): Deal 1 damage to an enemy. You may spend up to 2
#   [mental] resources to deal 2 additional damage to that enemy for each
#   [mental] resource spent this way.
#
# Cartes de reference :
#  - evenement d'attaque a degats variables : `im002` Repulsor Barrage /
#    `61004` « Big Mistake » : on calcule le TOTAL puis UN seul
#    `this.DealDamage(effect.targets, total, effect)` (une attaque, un coup) ;
#  - depense facultative dans le corps : `dt107` Zenpool,
#    `RessourcesMentalesDepensees` (helper du set).
#
# Mots-pieges :
#  - « 1 damage » + « 2 ADDITIONAL damage FOR EACH resource » : 1 + 2n, n de 0 a 2 ;
#  - « to THAT enemy » : la cible choisie au depart, jamais une seconde ;
#  - « (attack) » : `SetLabel('attack')` (ouvre Sonne / Desoriente / Prey) ;
#  - cout 0 : la carte se joue gratuitement, la depense des [mental] est a part.


def GetAbilities() -> Sequence['Ability']:

    def pounce(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        depenses = RessourcesMentalesDepensees(joueur, effect, 2)
        this.DealDamage(effect.targets, 1 + 2 * depenses, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            pounce,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
