from . import *

# Temporal Retrieval (x2) — AMELIORATION, cout 1 (energie). PSIONIC. TEMPORAL.
# Action: Exhaust Temporal Retrieval -> attach 1 card from your hand facedown here (to a maximum of 3).
# Response: After you use your "Chronoskimming" ability or play a TEMPORAL card, discard this card -> put each card attached
# to this card into your hand.
#
# CARTES DE REFERENCE : `27003` Parental Guidance (`this.PlaceCardHere(cartes, False, effect)` : carte posee FACE CACHEE sur
# une autre, `SetTarget(.., from_where=["YourHandCards"])`), `us006` (`AfterCardResolveAbility(.., ability_name=..)` pour
# « after you resolve the Action of X »), `AfterPlayerPlayedCard` (jouer une carte).
#
# MOTS-PIEGES : « to a maximum of 3 » (la capacite n'est plus offerte a 3) ; « Chronoskimming » est le NOM de la capacite de
# `rm001a` ; « discard this card -> put each card attached... » : on remet les cartes en main AVANT de defausser la carte
# (sinon elles partent a la defausse avec elle).
def GetAbilities() -> Sequence['Ability']:
    def moins_de_trois(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        Unused(message)
        return len(effect.this.GetPlacedCardArea().Get(True)) < 3

    def attacher(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        this.PlaceCardHere(effect.targets, False, effect)

    def reprendre(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        joueur = effect.GetInitiator()
        cartes = list(this.GetPlacedCardArea().Get(True))
        if cartes:
            Faces.AddToHand(cartes, joueur, effect)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            attacher,
            conditions=[moins_de_trois],
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(from_where=["YourHandCards"]),
        AbilityFactory.AfterCardResolveAbility(
            AbilityType.Response,
            ["Response"],
            CardFinder(name="Marvel Girl"),
            reprendre,
            card_control_by="You",
            ability_name="Chronoskimming",
        ),
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            "You",
            CardFinder(trait="TEMPORAL"),
            reprendre,
        ),
    ]
