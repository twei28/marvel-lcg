from . import *

# Energy Overflow
# Hero Action: Discard a TECH card you control → deal 6 damage to X enemies
#   in play, where X is equal to the printed resource cost of the discarded
#   card. This damage ignores tough status cards.
#
# Le nombre de cibles (X) n'est connu qu'apres le paiement du cout : choix
# fait a la main dans le handler via `initiator.AskChooseFaces(ennemis, (0,
# X), effect, forced=False)`, pas via un SetTarget statique. Cout imprime lu
# via `face.printed_cost.val` (modele : aos/aim_abduction/50081.py). Degats
# qui ignorent tough : `DamageProperty(6, ignore_tough=True)` (modele :
# mts/thanos/21116.py, Sanctuary).

def GetAbilities() -> Sequence['Ability']:

    def energy_overflow(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        initiator = effect.GetInitiator()

        discarded = effect.cost_func.Get(CostFunc.Discard).return_discarded_cards
        if not discarded:
            return
        x = discarded[0].printed_cost.val
        if x <= 0:
            return

        ennemis = Worlds.FindCardsOnField(effect, card_type=Enemy)
        cibles = initiator.AskChooseFaces(ennemis, (0, x), effect, forced=False)
        for cible in cibles:
            this.DealDamage([cible], DamageProperty(6, ignore_tough=True), effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            energy_overflow
        ).SetPlay()
        .SetCostFunc(CostFunc.Discard(trait="TECH", from_where=["YouControlCards"])),
    ]
