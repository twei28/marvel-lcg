from . import *

# Battle of the Patriots — MANIGANCE ANNEXE NEMESIS (2/5). Menace de depart 4, Acceleration, Boost 2.
# Aggression (red), Basic (gray), and Leadership (blue) cards cost 1 additional resource.
#
# Cartes de reference :
#  - `ar010` Ire of Athena : `AbilityFactory.IncreaseResourceCostToPlay(CardFinder(...), 1, "You")`, la seule fabrique qui
#    AUGMENTE un cout de jeu (RECETTES §5) ; `sk280` : `"AnyPlayer"` pour une carte de rencontre qui vise tout le monde.
#  - `src/game/card/card_finder/checker.py` : `CardFinder(card_classes=[...])` = OU entre classes (`face.IsClass(*classes)`).
#  - `01109` Bomb Scare : `desc.Acceleration` et `desc.StartingThreat` sont NATIFS (aucun script pour l'icone ni la menace).
#
# ⚠ Mots-pieges :
#  - « cards cost 1 ADDITIONAL » : +1 au cout de JEU de CHAQUE carte de ces classes, pour TOUS les joueurs (le texte ne dit
#    pas « you play ») ; Protection, Justice et les cartes signature (classe Hero) ne sont pas touchees.
#  - L'effet est CONTINU : il dure tant que la manigance annexe est en jeu (la carte perd son effet des qu'elle est
#    defaussee ou retiree).
#  - L'icone du centre de la carte est ACCELERATION (verifiee par decoupe contre 01109 Bomb Scare, pas Hazard ni Crisis).
def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.IncreaseResourceCostToPlay(
            CardFinder(card_classes=["Aggression", "Basic", "Leadership"]),  # type: ignore
            1,
            "AnyPlayer",
        ),
    ]
