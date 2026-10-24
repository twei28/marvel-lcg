from . import *

# Dragon Strike — EVENEMENT, cout 2, impression 8/15 : ressource(s) imprimee(s) energie. ATTACK. (card_id shc010)
# Hero Action (attack): Deal 5 damage to an enemy.
# Flow: [energy] → this attack gains piercing, ranged, and overkill.
#
# ⚠ IMPRESSIONS : Dragon Strike existe en DEUX cartes (shc009) qui ne different que par l'ICONE DE RESSOURCE du coin ;
#   `shc` les separe parce que le Flow de la carte SUIVANTE lit cette icone (correspondance stricte, decision du 24/10).
#
# Cartes de reference :
#  - `nt006` Melon Grab : `DealDamage(cibles, N, effect, property=AttackProperty(piercing=True, overkill=True))` ;
#    `ra007` : `AttackProperty(ranged=True)`.
#
# ⚠ Mots-pieges :
#  - le Flow modifie l'ATTAQUE : il est resolu AVANT les degats (sinon rien a modifier) ; Flow [energy] exige un eclair imprime.
#  - piercing + ranged + overkill ensemble : les trois proprietes ou aucune.
#  - 5 degats dans les deux cas : le Flow ne change pas le nombre.


def GetAbilities() -> Sequence['Ability']:

    def dragon_strike(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = JoueurDeCetteCarte(effect)
        cibles = [t for t in effect.targets if t is not None]
        if joueur is not None and AccepterFlow(effect, joueur, "Y"):
            this.DealDamage(cibles, 5, effect,
                            property=AttackProperty(piercing=True, ranged=True, overkill=True))
            FlowResolu(joueur, this)
            return
        this.DealDamage(cibles, 5, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            dragon_strike,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
