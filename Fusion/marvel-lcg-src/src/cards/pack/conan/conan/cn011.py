from . import *

# * Atlantean Sword — amelioration (15/16), cout 2 [energy]. WEAPON. Restricted.
# Hero Response (attack/thwart): After you play an event, exhaust Atlantean
#   Sword -> deal damage to an enemy or remove threat from a scheme equal to
#   that event's printed cost.
#
# CARTES DE REFERENCE
#  - « After you play an event, exhaust X -> » : rs012 Bloodmoon Battleaxe
#    (`AfterPlayerPlayedCard(..., Event, op).SetCostFunc(CostFunc.Exhaust("This"))`).
#  - « that event's printed cost » : 42001c Archangel, `FacesCounter.GetPrintedCost([message.played_face])`.
#  - Restricted : lu dans `desc`, aucun script (base automatique).
#
# TEXTE CONTRE CODE
#  « printed cost » : le cout IMPRIME (1 pour un « 1* » a Discount), pas le cout paye.


def GetAbilities() -> Sequence['Ability']:

    def atlantean_sword(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Upgrade)
        joueur = JoueurDe(effect)
        if joueur is None:
            return
        cout = FacesCounter.GetPrintedCost([message.played_face])
        if cout <= 0:
            return
        ChoisirDegatsOuMenace(joueur, this, effect, cout, cout)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.HeroResponse,
            "You",
            Event,
            atlantean_sword,
        ).SetLabel('attack', 'thwart')
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
