from . import *

# * Human Torch — custom « DesignHacker »
# Flame On! — Interrupt: When you place a flame counter on an enemy, deal 1
# damage to that enemy. An enemy cannot have more than 3 flame counters on
# them.
#
# LENIENT : le moteur groupe les compteurs posés en un seul message. On
# inflige donc 1 dégât PAR compteur effectivement posé (poser 3 compteurs =
# 3 dégâts), ce qui suit l'intention de la carte. Le déclenchement est traité
# en Response (après pose) plutôt qu'en Interrupt : le moteur n'expose pas la
# cible avant la pose, et le résultat visible est le même.

def GetAbilities() -> Sequence['Ability']:

    def flame_on(effect: 'Effect', message: 'Message.AfterCardPlacedCounter') -> None:
        this = effect.this.CastTo(Hero)

        if message.counters <= 0:
            return
        this.DealDamage([message.trigger], message.counters, effect)

    def par_toi(effect: 'Effect', message: 'Message.AfterCardPlacedCounter') -> bool:
        # « When YOU place a flame counter » : seulement le joueur Human Torch.
        return message.place_player == effect.GetInitiator()

    def maximum_3(effect: 'Effect', message: 'Message.WhenCardWouldBePlacedCounter') -> None:
        message.maximum = 3

    return [
        AbilityFactory.AfterCounterPlacedOn(
            AbilityType.Response,
            Enemy,
            'flame',
            flame_on,
            conditions=[par_toi],
        ).SetName("Flame On!"),

        AbilityFactory.WhenCardWouldBePlacedCounter(
            AbilityType.Rule,
            CardFinder(card_type=Enemy),
            'flame',
            maximum_3,
        ),
    ]
