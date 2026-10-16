from . import *

# Street Vendor — AMELIORATION Leadership (TMNT Aspects, Inkwire), cout 2, [energy]. NYC.
# Reduce the cost to play this card by 1 if you control a [[NYC]] support.
# Hero Action: Discard Street Vendor -> heal a total of 3 damage from among characters you control.
#
# CARTES DE REFERENCE
#  - `40023` Mission Leader / `al012` Gator Aid : amelioration SANS « Attach to » : aucune capacite Play,
#    `Upgrade.GetAbilities` la pose dans la zone du joueur.
#  - `sk062` / `nt005` : « Reduce the cost ... by 1 if ... » = `ReduceCostToPlayThis(1, conditions=[...])` ;
#    `ua015` : « you control a NYC support » = `joueur.IsControl(CardFinder2("NYC", Support))`.
#  - `43006` Regenerative Longevity : « heal a total of N damage from ... » = `SetTarget(<unites>,
#    repeat_rules="Sustained", range=(1, N))` + `HealthUnits(cibles, 1)` (une cible par point soigne).
#  - « Discard X -> » en cout d'une action : `CostFunc.Discard("This")`.
#
# TEXTE CONTRE CODE
#  ⚠ « Discard Street Vendor » est DEVANT la fleche : un COUT.
#  ⚠ « a total of 3 » : 3 points au plus, repartis librement (un meme personnage peut en recevoir
#    plusieurs, dans la limite de ses degats).
#  ⚠ « characters YOU CONTROL » : votre identite et vos allies.
#  ⚠ « Hero Action » : forme heros uniquement.
#  Aucune limite imprimee.


def GetAbilities() -> Sequence['Ability']:

    def soutien_nyc(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> bool:
        Unused(message)
        joueur = effect.GetInitiator()
        return joueur is not None and joueur.IsControl(CardFinder2("NYC", Support))

    def street_vendor(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        this.HealthUnits(effect.targets, 1, effect)

    return [
        AbilityFactory.ReduceCostToPlayThis(1, conditions=[soutien_nyc]),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            street_vendor,
        ).SetCostFunc(CostFunc.Discard("This"))
        .SetTarget("YouControlUnit", repeat_rules="Sustained", range=(1, 3)),
    ]
