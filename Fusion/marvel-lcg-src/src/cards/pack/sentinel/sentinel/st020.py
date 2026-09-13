from . import *

# Size Advantage — Evenement 2 [energy], AGRESSIVITE. Carte EXTRA, hors set du
# heros : elle entre au vivier general et devient jouable par tout le monde.
# Hero Action (attack): Deal 3 damage to an enemy (6 damage instead if you have
#   the [[GIANT]] trait or more remaining hit points than that enemy).
#
# Cartes de reference :
#  - `04044` Piercing Strike pour la forme d'un evenement d'attaque.
#  - `dt005` Blast Radius : `hero.health` est le total RESTANT, pas l'imprime.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **or** » : une seule des deux conditions suffit. Sentinel a GIANT, donc
#    la carte fait toujours 6 pour lui — mais elle est jouable par n'importe
#    quel heros d'Agressivite, et c'est alors la comparaison de points de vie
#    qui tranche.
#  - « **more remaining** hit points **than that enemy** » : strictement plus,
#    et sur les PV RESTANTS des deux cotes, pas sur les valeurs imprimees.
#  - La comparaison se fait AVANT les degats, sur la cible choisie.


def GetAbilities() -> Sequence['Ability']:

    def size_advantage(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        joueur = effect.GetInitiator()
        hero = joueur.GetHero()

        for cible in effect.targets:
            unite = cible.CastTo(Unit2)
            plus_de_pv = unite is not None and hero.health > unite.health
            degats = 6 if (hero.HasTrait("GIANT") or plus_de_pv) else 3
            hero.DealDamage([cible], degats, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            size_advantage,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
