from . import *

# * Doomstadt — soutien signature. LOCATION. LATVERIA. Cout 1.
# Events tucked under Doomstadt can be played as if they were in your hand.
# Action: Exhaust Doomstadt -> tuck a SPELL event from your hand under here
#   (to a maximum of 3).
#
# Carte de reference : aa002 * Scarlet Witch (pack agatha_harkness), qui fait
# EXACTEMENT les deux moities :
#  - `YouMayPlayCardLikeInHand(NonKeyword, Event, from_where="ThisPlacedCard")`
#    rend jouables les cartes glissees sous elle ;
#  - `this.PlaceCardHere(cibles, False, effect)` les y glisse.
# Seule difference : Scarlet Witch les prend dans la DEFAUSSE et les pose face
# cachee a son entree en jeu ; Doomstadt les prend en MAIN, sur une action
# repetable, avec un plafond de 3.
#
# ⚠ « to a maximum of 3 » : plafond sur le nombre de cartes DEJA glissees,
# verifie en condition de l'action — sinon le joueur inclinerait le soutien
# pour rien.
#
# ⚠ Le moteur a un helper au nom exact du texte imprime,
# `TuckCardUnderHere(faces, effect)` (card_face.py:973), qui enveloppe
# `PlaceCardHere`. Et les cartes deja glissees se comptent par
# `GetPlacedCardArea().GetSize()` (card_face.py:969), pas par un
# `GetPlacedCards()` qui n'existe pas.

def GetAbilities() -> Sequence['Ability']:

    def cartes_glissees(effect: 'Effect') -> int:
        return effect.this.GetPlacedCardArea().GetSize()

    def doomstadt(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)

        cibles = [t for t in effect.targets if t is not None]
        if cibles:
            this.TuckCardUnderHere(cibles, effect)

    return [
        *AbilityFactory.YouMayPlayCardLikeInHand(
            AbilityType.NonKeyword,
            Event,
            from_where="ThisPlacedCard",
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            doomstadt,
            conditions=[lambda effect, message: cartes_glissees(effect) < 3],
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(CardFinder2("SPELL", Event), range=(1, 1),
                   from_where=["YourHandCards"]),
    ]
