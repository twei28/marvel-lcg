from . import *

# * Neutron — SBIRE (Imperial Guard). IMPERIAL GUARD. PV 5, MNG 1, ATQ 2. 2 icone(s) de boost.
# When Revealed: Discard a support you control. If you cannot, resolve the "Special" ability on the SETTING environment.
#
# Cartes de reference :
#  - « When Revealed ... If you cannot, resolve the "Special" ability on the SETTING environment » : `QuandRevele`
#    (imperial_guard/__init__.py, `WhenThisRevealed` + `ResolveSpecialAbility`, modele baxter_stockman `ResoudreLeSpecial`).
#  - « Discard a ... » : `Faces.DiscardAll([carte choisie])`, choix du joueur `AskChooseFace` (modele gs240 Energy Transfer
#    pour la defausse, bt021 Dark Transformation pour la lecture de la classe).
#  - « a support you control » : `joueur.GetControlCardsByType(support=True)`.
#
# ⚠ Mots-pieges : « If you CANNOT » = aucune carte a defausser (le sbire n'a alors AUCUN autre effet : il s'engage normalement) ; « YOU » = le joueur a qui il est revele ; la clause « Special » vise l'environnement SETTING EN JEU. « SUPPORT » = type Soutien en jeu sous le controle du joueur.


def GetAbilities() -> Sequence['Ability']:

    def effet_imprime(effect: 'Effect', joueur: 'Player') -> bool:
        return DefausserUneParmi(effect, joueur, joueur.GetControlCardsByType(support=True))

    return [
        QuandRevele(effet_imprime),
    ]
