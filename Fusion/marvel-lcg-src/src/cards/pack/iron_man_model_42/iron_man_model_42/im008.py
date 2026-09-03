from . import *

# * Mark IVa Repulsors — amelioration signature, x1 (n/15 = 11).
# TECH. WEAPON. Cout 1, ressource [energy].
# Hero Interrupt: When Iron Man makes a basic attack, remove 1 reactor counter
#   from him -> that attack deals 2 additional damage and gains ranged.
#
# Cartes de reference :
#  - **`41019` Directed Force** pour `DealAdditionalDamage(2, effect)` ;
#  - `WhenUnitWouldAttack(..., is_basic_attack=True)` (do_attack.py:32), qui
#    porte a la fois `DealAdditionalDamage` et `GainRanged`
#    (sender_damage.py) ;
#  - `RetirerUnReacteur` (helper du set) pour le cout.
#
# ⚠ POURQUOI `WhenUnitWouldAttack` ET NON `WhenUnitUseBasicPower`. Les deux
# fenetres existent et 32177 Swagger emploie la seconde — mais Swagger modifie
# la DEF, une valeur du POUVOIR, alors qu'ici il faut modifier l'ATTAQUE
# elle-meme (degats et mot-cle). `DealAdditionalDamage` et `GainRanged` vivent
# sur `WhenUnitWouldAttack` : c'est la seule fenetre qui les porte.
# `is_basic_attack=True` rend le mot « basic » de la carte.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « makes a **BASIC** attack » : `is_basic_attack=True` est indispensable.
#    Sans lui, im002 Repulsor Barrage gagnerait aussi les 2 degats, ce que le
#    texte n'accorde pas.
#  - « remove 1 reactor counter **->** » : COUT. Sans compteur, l'attaque part
#    normalement, sans bonus.
#  - « **that** attack » : l'attaque en cours, pas la suivante.
#  - `ranged` ignore la Riposte : c'est ce qui rend cette carte bonne contre
#    un sbire a Riposte, en plus des degats.
#  - Aucune limite imprimee, mais le compteur borne de fait.
#
# ⚠ LE RETRAIT DU COMPTEUR EST DANS LE COUT, PAS DANS LE CORPS, ET C'EST UN
# CORRECTIF PAYE EN AUTOPLAY (03/09/2026). Ecrit `if RetirerUnReacteur(...):`
# dans le corps, la capacite RESOUT quand meme quand le reacteur est vide :
# elle ne fait rien, le moteur la repropose a l'identique, et la partie tourne
# en rond. Mesure : 1 partie bloquee sur 32, verdict « meme question posee a
# l'identique et le plateau n'a pas bouge ». Dans le COUT
# (`CoutDuReacteur`, helper du set), le False empeche le paiement et l'option
# n'est pas offerte. Meme defaut que le blocage Underling du 20/08.



def GetAbilities() -> Sequence['Ability']:

    def mark_iva(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        # Le compteur a deja ete retire par le COUT.
        message.DealAdditionalDamage(2, effect)
        message.GainRanged(effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.HeroInterrupt,
            "You",
            mark_iva,
            is_basic_attack=True,
        ).SetCostFunc(CostFunc.Custom(None, CoutDuReacteur)),
    ]
