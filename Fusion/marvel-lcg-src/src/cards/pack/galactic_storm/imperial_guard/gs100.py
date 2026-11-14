from . import *

# * Hussar — SBIRE (Imperial Guard). IMPERIAL GUARD. PV 5, MNG 1, ATQ 2. 2 icone(s) de boost.
# When Revealed: Discard an upgrade you control. If you cannot, resolve the "Special" ability on the SETTING environment.
#
# Cartes de reference :
#  - « When Revealed ... If you cannot, resolve the "Special" ability on the SETTING environment » : `QuandRevele`
#    (imperial_guard/__init__.py, `WhenThisRevealed` + `ResolveSpecialAbility`, modele baxter_stockman `ResoudreLeSpecial`).
#  - « Discard a ... » : `Faces.DiscardAll([carte choisie])`, choix du joueur `AskChooseFace` (modele gs240 Energy Transfer
#    pour la defausse, bt021 Dark Transformation pour la lecture de la classe).
#  - « an upgrade you control » : `joueur.GetControlUpgrade()` (comprend les ameliorations posees sur ses allies).
#
# ⚠ Mots-pieges : « If you CANNOT » = aucune carte a defausser (le sbire n'a alors AUCUN autre effet : il s'engage normalement) ; « YOU » = le joueur a qui il est revele ; la clause « Special » vise l'environnement SETTING EN JEU. « UPGRADE » = type Amelioration (pas un attachement de rencontre, pas un soutien) ; « you control » = en jeu.


def GetAbilities() -> Sequence['Ability']:

    def effet_imprime(effect: 'Effect', joueur: 'Player') -> bool:
        return DefausserUneParmi(effect, joueur, list(joueur.GetControlUpgrade()))

    return [
        QuandRevele(effet_imprime),
    ]
