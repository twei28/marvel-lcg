from . import *

# Creeping Corruption (face A) — AMELIORATION. Permanent. Setup. Max 1 per player.
# If there are at least 5 corruption counters here, remove each of them from here and flip this card.
# Action : Exhaust Creeping Corruption and place 1 corruption counter here -> draw 1 card.
#
# Cartes de reference : tt/enchantress/55007a Hypnotic Gaze (`IfThereAreAtLeastCounterHere(5, ..., op)` + `RemoveCountersOn("All")` + `Flip`),
#  core/captain_marvel/01015 Alpha Flight Station (`Action` + `CostFunc.Exhaust("This")`), gambit/37008 (`CostFunc.PlaceCounter` en cout).
# ⚠ Mots-pieges : « Permanent », « Setup », « Max 1 per player » (`MaxPerUnit`) sont lus dans `desc` : aucun script. « remove EACH of them » = TOUS les
#  compteurs (`"All"`), meme si une pose de 2 passe de 4 a 6 ; la face B repart donc a 0. « Action » (pas Hero Action) : jouable en alter-ego comme en heros.
#  Le compteur est un COUT (« place 1 corruption counter here → draw ») : pose avant l'effet ; si c'est le 5e, la carte se retourne avant la pioche (la pioche a lieu).


def GetAbilities() -> Sequence['Ability']:

    def retourner(effect: 'Effect', message: 'Message.AfterCardPlacedCounter') -> None:
        this = effect.this.CastTo(Upgrade)
        Faces.RemoveCountersOn([this], "All", 'corruption', effect)
        this.card.Flip(effect)

    def piocher(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        effect.GetInitiator().DrawUp(1, effect)

    return [
        AbilityFactory.IfThereAreAtLeastCounterHere(SEUIL_CORRUPTION, 'corruption', retourner),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, piocher)
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.PlaceCounter("This", 1, 'corruption')),
    ]
