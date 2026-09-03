from . import *

# Tactical Interface — amelioration signature, x1 (n/15 = 15).
# TECH. Cout 1, ressource [mental].
# Hero Interrupt: When Iron Man makes a basic thwart, remove 1 reactor counter
#   from him -> that thwart removes 2 additional threat and ignores the patrol
#   keyword.
#
# LE MIROIR DE `im008` Mark IVa Repulsors, cote menee : meme cout d'un
# compteur, meme fenetre sur un pouvoir de base, meme structure.
#
# Cartes de reference :
#  - **`32177` Swagger** pour la fenetre : `WhenUnitUseBasicPower(
#    HeroInterrupt, ...)`, filtree sur `message.power == 'THW'`, et
#    `message.GainValue(n, effect)` qui redirige tout seul vers
#    `GainTHWForThisThwart` (sender_unit.py:21) ;
#  - **`61023` Grapnel Launcher** et `42006` Natural Flight pour l'exemption
#    de Patrouille, qui passe par le mecanisme DEDIE du moteur et non par une
#    bidouille de ciblage.
#
# ⚠ POURQUOI PAS `.SetIgnoreKeyword('Patrol')` SUR CETTE ABILITE. C'est ce que
# fait 61023 — mais 61023 EFFECTUE elle-meme la menee, donc son propre effet
# porte l'exemption. Ici la menee est celle du JOUEUR, faite par un autre
# effet : notre `SetIgnoreKeyword` ne serait jamais consulte.
# `effect.IsIgnoreKeyword` (effect.py:493) offre l'autre chemin, un message
# `CheckIfEffectIsIgnoreKeyWord` auquel repond la fabrique
# `UnitIgnoreKeywordIcons(..., while_use_basic_thw=True)` (play.py:443). On
# l'enregistre EN TEMPORAIRE, le temps de cette menee : l'exemption est
# conditionnee au compteur paye, elle ne peut donc pas etre continue.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « makes a **BASIC** thwart » : le filtre sur `message.power == 'THW'` est
#    indispensable, sinon la carte se declencherait aussi sur l'attaque et la
#    defense de base.
#  - « remove 1 reactor counter **->** » : COUT. Sans compteur, la menee part
#    normalement.
#  - « **that** thwart » : la menee en cours.
#  - Patrouille protege le complot PRINCIPAL tant qu'un sbire patrol est
#    engage : sans l'exemption, la carte promettrait quelque chose qu'elle ne
#    ferait pas (leçon gp005, correctif du 30/08/2026).
#
# ⚠ LE RETRAIT DU COMPTEUR EST DANS LE COUT, PAS DANS LE CORPS, ET C'EST UN
# CORRECTIF PAYE EN AUTOPLAY (03/09/2026). Ecrit `if RetirerUnReacteur(...):`
# dans le corps, la capacite RESOUT quand meme quand le reacteur est vide :
# elle ne fait rien, le moteur la repropose a l'identique, et la partie tourne
# en rond. Mesure : 1 partie bloquee sur 32. Dans le COUT (`CoutDuReacteur`,
# helper du set), le False empeche le paiement et l'option n'est pas offerte.


def GetAbilities() -> Sequence['Ability']:

    def seulement_la_menee(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> bool:
        Unused(effect)
        return message.power == 'THW'

    def tactical_interface(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Upgrade)

        # Le compteur a deja ete retire par le COUT.
        message.GainValue(2, effect)

        # « ignores the patrol keyword », le temps de CETTE menee seulement.
        this.effect.RegisterTemp(
            AbilityFactory.UnitIgnoreKeywordIcons(
                "You",
                patrol=True,
                while_use_basic_thw=True,
            ),
            unregister_after_exec=True,
        )

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.HeroInterrupt,
            "You",
            tactical_interface,
            conditions=[seulement_la_menee],
        ).SetCostFunc(CostFunc.Custom(None, CoutDuReacteur)),
    ]
