from . import *

# * Titan — SBIRE (Imperial Guard). IMPERIAL GUARD. PV 6, MNG 0, ATQ 2. 1 icone(s) de boost.
# When Revealed: Discard a resource card from your hand. If you cannot, resolve the "Special" ability on the SETTING environment.
#
# Cartes de reference :
#  - « When Revealed ... If you cannot, resolve the "Special" ability on the SETTING environment » : `QuandRevele`
#    (imperial_guard/__init__.py, `WhenThisRevealed` + `ResolveSpecialAbility`, modele baxter_stockman `ResoudreLeSpecial`).
#  - « Discard a ... » : `Faces.DiscardAll([carte choisie])`, choix du joueur `AskChooseFace` (modele gs240 Energy Transfer
#    pour la defausse, bt021 Dark Transformation pour la lecture de la classe).
#  - « a resource card » : type Ressource (carte), PAS une carte portant une icone de ressource.
#
# ⚠ Mots-pieges : « If you CANNOT » = aucune carte a defausser (le sbire n'a alors AUCUN autre effet : il s'engage normalement) ; « YOU » = le joueur a qui il est revele ; la clause « Special » vise l'environnement SETTING EN JEU. « RESOURCE CARD » = type Ressource (Energy, Genius, Strength...) : une carte d'un autre type portant une icone ne compte pas.


def GetAbilities() -> Sequence['Ability']:

    def effet_imprime(effect: 'Effect', joueur: 'Player') -> bool:
        return DefausserUneParmi(effect, joueur, [f for f in joueur.hand_cards.Get() if Resource.IsType(f)])

    return [
        QuandRevele(effet_imprime),
    ]
