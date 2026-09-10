from . import *

# * U.S. Agent — ALLIE d'aspect PROTECTION, cout 4, 4 PV, CTR 1*, ATQ 2**,
# RES [physical]. AVENGER.
# Hero Interrupt: When an enemy initiates an attack against you, deal 1 damage
#   to U.S. Agent -> deal 2 damage the attacking enemy.
#
# ⚠ « deal 2 damage THE attacking enemy » : la coquille est imprimee (il
# manque « to »). Elle reste dans le texte de la carte.
#
# CARTES DE REFERENCE
#  - `an006` Angelic Ribbons / `as015` * Scarlet Spider :
#    `WhenEnemyActivateAgainstYou`... mais ici le texte dit « INITIATES an
#    attack », ce qui est `WhenUnitInitiatesAttackAgainst` — la fenetre
#    s'ouvre AVANT que le defenseur ne soit declare.
#  - `CostFunc.TakeDamage(1, "This")` : les degats a soi comme COUT, deja
#    utilises par `sw013` Shroud juste au-dessus.
#    ⚠ L'ORDRE DES ARGUMENTS EST (valeur, cible), pas (cible, valeur)
#    (cost_func.py:409). Ecrit a l'envers, le moteur appelle `value(effect)` sur
#    une chaine, leve un TypeError qu'il AVALE, et la capacite ne part jamais.
#    Les deux allies du pack etaient touches ; seul le harnais l'a vu.
#
# TEXTE CONTRE CODE
#  ⚠ 4 PV pour 1 degat par declenchement : il tient quatre attaques, et rend
#    8 degats. C'est le meilleur echange de l'aspect, et il est lent.
#  ⚠ « against YOU » : l'attaque doit viser CE joueur.
#  ⚠ « the ATTACKING ENEMY » : l'attaquant, pas une cible au choix.


def GetAbilities() -> Sequence['Ability']:

    def agent(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Ally)
        # Le degat sur U.S. Agent a deja ete paye par le COUT.
        attaquant = message.attacker
        if attaquant is not None:
            this.DealDamage([attaquant], 2, effect)

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.WhenUnitAttackYou(
            AbilityType.HeroInterrupt,
            Enemy,
            agent,
        ).SetCostFunc(CostFunc.TakeDamage(1, "This")),
    ]
