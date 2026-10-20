from . import *

# * Electron — SBIRE (Imperial Guard). IMPERIAL GUARD. SHI'AR. PV 5, MNG 1, ATQ 2. 2 icone(s) de boost.
# When Revealed: Discard a [energy] resource from your hand. If you cannot, resolve the "Special" ability on the SETTING environment.
#
# Cartes de reference :
#  - « When Revealed ... If you cannot, resolve the "Special" ability on the SETTING environment » : `QuandRevele`
#    (imperial_guard/__init__.py, `WhenThisRevealed` + `ResolveSpecialAbility`, modele baxter_stockman `ResoudreLeSpecial`).
#  - « Discard a ... » : `Faces.DiscardAll([carte choisie])`, choix du joueur `AskChooseFace` (modele gs240 Energy Transfer
#    pour la defausse, bt021 Dark Transformation pour la lecture de la classe).
#  - icone de ressource du texte (energie (eclair)) : identifiee par decoupe contre sk148 / sk152 (ressource declaree),
#    gabarit IMPERIAL-GUARD-GABARITS.md ; « a [energy] resource from your hand » = une CARTE de la main portant l'icone
#    (`FacesCounter.GetPrintedResourcesCount`, conversions comprises ; une carte wild n'est pas une ressource [energy] imprimee).
#
# ⚠ Mots-pieges : « If you CANNOT » = aucune carte a defausser (le sbire n'a alors AUCUN autre effet : il s'engage normalement) ; « YOU » = le joueur a qui il est revele ; la clause « Special » vise l'environnement SETTING EN JEU. « [energy] RESOURCE from your HAND » = une carte de la main, pas une carte en jeu, pas une carte sans cette icone.


def GetAbilities() -> Sequence['Ability']:

    def effet_imprime(effect: 'Effect', joueur: 'Player') -> bool:
        return DefausserUneDeLaMain(effect, joueur, "Y")

    return [
        QuandRevele(effet_imprime),
    ]
