from . import *

# Hit the Weak Spot — EVENEMENT AGRESSION, cout 2 [mental]. ATTACK.
# Hero Action (attack): Deal 2 damage to a minion for each icon (★ and Y) in that
#   minion's boost area. This attack gains piercing.
#
# Cartes de reference :
#  - **`04009`** Vibranium Arrow : « attack » avec perçant =
#    `this.DealDamage(cibles, n, effect, property=AttackProperty(piercing=True))`,
#    `.SetPlay().SetLabel('attack').SetTarget(...)`.
#  - **`sn014`** / RECETTES §3 : `FacesCounter.CountTotalBoostStarAndBoost` additionne
#    l'etoile (`boost_star`, une capacite Boost) ET les icones chiffrees ; c'est la
#    fonction du texte « each icon (★ and Y) ».
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « each icon (★ AND Y) in THAT MINION'S BOOST AREA » : decision de l'utilisateur
#    (15/10/2026) : les icones IMPRIMEES dans le champ de boost du sbire (icones
#    chiffrees + etoile), PAS les cartes de boost posees face cachee.
#  - « a MINION » : un sbire (pas le vilain) ; « 2 damage FOR EACH icon » : 2 x icones.
#  - « This attack gains PIERCING » : perçant (defausse le statut Tenace au lieu d'etre
#    bloque) ; sans icone, aucun degat.


def GetAbilities() -> Sequence['Ability']:

    def hit_the_weak_spot(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        for sbire in effect.targets:
            degats = 2 * FacesCounter.CountTotalBoostStarAndBoost([sbire])
            if degats > 0:
                this.DealDamage([sbire], degats, effect, property=AttackProperty(piercing=True))

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            hit_the_weak_spot,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Minion),
    ]
