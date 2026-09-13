from . import *

# Exterminate — Evenement 2 [physical], classe Hero. ATTACK.
# [star] As an additional cost to play this event, exhaust or destroy Arms
#   (Intact) and any one other [[COMPONENT]] upgrade ([[INTACT]] side up).
# Hero Action (attack): Deal 7 damage to an enemy. This attack gains ranged,
#   piercing, and overkill. Expose 2 enemies.
#
# Cartes de reference :
#  - `06005` Hammer Throw : un evenement d'attaque dont le cout additionnel
#    incline une amelioration nommee, et `AttackProperty(overkill=True)`.
#  - `04044` Piercing Strike : `hero.DealDamage(..., property=AttackProperty)`.
#  - `st002a` pour l'exposition, `st007` a `st009` pour le cout a une seule
#    piece.
#
# ⚠ MOT-CLE MAISON DESTROY (docs/reference/mots-cles/destroy.md).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **Arms (Intact) AND any one other** » : DEUX pieces, et la premiere est
#    imposee. Le selecteur de cout ne demande donc que la SECONDE (`exclure`
#    ecarte Arms) ; la presence d'Arms est une CONDITION de la capacite, pas
#    une cible — sans elle la carte est injouable, ce qui est exactement ce que
#    dit le texte.
#  - Le choix « inclinez ou detruisez » se pose pour CHACUNE des deux pieces,
#    separement (helper `InclinerOuDetruire`).
#  - « ranged, piercing, and overkill » : les trois d'un coup, dans un seul
#    `AttackProperty`. C'est le HEROS qui frappe (le texte parle d'une attaque
#    du personnage), modele 04044, donc `hero.DealDamage`.
#  - « Expose 2 enemies » vient APRES les degats et n'est pas lie a la cible de
#    l'attaque : deuxieme selecteur, et le vilain tue entre-temps n'y est plus.


def GetAbilities() -> Sequence['Ability']:

    def exterminer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        hero = effect.GetInitiator().GetHero()
        hero.DealDamage(
            effect.targets, 7, effect,
            property=AttackProperty(ranged=True, piercing=True, overkill=True),
        )
        Exposer(effect.targets2, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            exterminer,
            conditions=[
                lambda effect, message:
                    ComposantIntactNomme(effect, NOM_ARMS) is not None
            ],
        ).SetPlay().SetLabel('attack')
        .SetCostFunc(CostFunc.Custom(
            SelecteurComposantIntact(exclure=NOM_ARMS),
            lambda cibles, e: InclinerOuDetruire(
                [ComposantIntactNomme(e, NOM_ARMS), *cibles], e),
        ))
        .SetTarget(Enemy)
        .SetTarget2(Enemy, range=("Zero", 2)),
    ]
