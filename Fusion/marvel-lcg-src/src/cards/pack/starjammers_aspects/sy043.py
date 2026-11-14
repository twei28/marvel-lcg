from . import *
# Thorn Crew (Protection, soutien sans cout [physical]). Permanent. Linked (Kalyx).
# Each facedown THORN ally has a base THW of 1, a base ATK of 1 and base hit points of 1.
# Forced Response: After a THORN ally is defeated, place that card in its owner's discard pile.
#
# Cartes de reference : 01140 Ultron Drones (`GiveKeywordToInPlayWhenApplyThis(CardFinder(name="Drone Minion"), base_sch=1, base_atk=1,
# base_health=1)` + `AfterUnitBeDefeated(ForcedResponse, ..)`) ; fiches linked.md, permanent.md.
# ⚠ Le moteur n'a pas de `base_thw` pour un allie : les valeurs de base sont portees par le GABARIT `sy_thorn_ally` (cards.json, ATQ 1, CTR 1,
# PV 1), et la presente carte rend la carte vaincue a la DEFAUSSE de son proprietaire sous sa face imprimee (`SwapBackToPrintedCard`).
def GetAbilities() -> Sequence['Ability']:
    def thorn_vaincu(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        carte = message.trigger.card
        # l'allie vaincu va a la defausse de son PROPRIETAIRE (l'allie a ete pris dans son deck) ; on lui rend sa face imprimee
        carte.SwapBackToPrintedCard(effect)
    return [
        AbilityFactory.AfterUnitBeDefeated(
            AbilityType.ForcedResponse,
            CardFinder(name="Thorn Ally", card_type=Ally),
            thorn_vaincu,
        ),
    ]
