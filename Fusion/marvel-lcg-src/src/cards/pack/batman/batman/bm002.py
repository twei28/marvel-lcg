from . import *
# * Robin (Damian Wayne) — ALLIE. Response : after Robin defeats an enemy or removes the last threat from a scheme, look at the top 3 cards of the
# encounter deck. You may discard one and place the rest on top in any order.
# Cartes de reference : `AfterUnitDefeatedUnit` (defeated.py) et `AfterUnitThwartAndRemoveLastThreat` (thwart.py) ; `ChooseOrder` : paibok.
# ⚠ Une carte de dissuasion defaussee ainsi n'a pas ete RESOLUE : elle part dans la defausse auxiliaire puis revient dans le deck de rencontre
# (RangerSiNonResolue) — c'est le cas d'usage que decrit l'encart.
def GetAbilities() -> Sequence['Ability']:
    def regard(effect: 'Effect', message: 'Message2') -> None:
        joueur = JoueurDeCetteCarte(effect)
        deck = Worlds.GetEncounterDeck(effect)
        dessus = list(deck.GetTops(3))
        if joueur is None or not dessus:
            return
        choisies: List['CardFace'] = []
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Discard one of the top 3 cards of the encounter deck", lambda c: choisies.extend(c))
            .SetTarget(dessus, range=(0, 1), not_move=True, not_shuffle=True),
        )
        if choisies:
            Faces.DiscardAll(choisies, effect)
        reste = [f for f in dessus if f not in choisies]
        if len(reste) > 1:
            reste = list(joueur.ChooseOrder(reste))
        for face in reversed(reste):
            face.card.MoveToTop(deck, effect)
    return [
        AbilityFactory.AfterUnitDefeatedUnit(AbilityType.Response, "This", Enemy, regard).SetName("Robin"),
        AbilityFactory.AfterUnitThwartAndRemoveLastThreat(AbilityType.Response, "This", regard).SetName("Robin"),
    ]
