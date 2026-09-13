from . import *

# Rocket Punch — Evenement 1 [energy], classe Hero. ATTACK.
# [star] As an additional cost to play this event, exhaust Arms (Intact) or
#   destroy it.
# Hero Action (attack): Deal 5 damage to an enemy. This attack gains overkill.
#
# Cartes de reference : `06005` Hammer Throw (cout par inclinaison d'une
# amelioration nommee + `AttackProperty(overkill=True)`), `04044` pour
# `hero.DealDamage`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « exhaust Arms (Intact) **or destroy it** » : le « it » designe Arms, pas
#    un Component au choix. Le selecteur de cout est donc nomme.
#  - Arms deja incline ? La carte reste jouable : il reste la destruction.
#    C'est la boucle de jeu du pack, pas un effet de bord (fiche destroy.md).


def GetAbilities() -> Sequence['Ability']:

    def rocket_punch(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        hero = effect.GetInitiator().GetHero()
        hero.DealDamage(
            effect.targets, 5, effect,
            property=AttackProperty(overkill=True),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            rocket_punch,
        ).SetPlay().SetLabel('attack')
        .SetCostFunc(CostFunc.Custom(
            SelecteurComposantIntact(nom=NOM_ARMS),
            InclinerOuDetruire,
        ))
        .SetTarget(Enemy),
    ]
