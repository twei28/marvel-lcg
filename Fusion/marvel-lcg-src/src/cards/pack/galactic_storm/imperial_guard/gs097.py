from . import *

# * Fang — SBIRE (Imperial Guard). IMPERIAL GUARD. PV 5, MNG 1, ATQ 2. 2 icone(s) de boost.
# When Revealed: Discard a card you control with a printed [wild] resource. If you cannot, resolve the "Special" ability on the SETTING environment.
#
# Cartes de reference :
#  - « When Revealed ... If you cannot, resolve the "Special" ability on the SETTING environment » : `QuandRevele`
#    (imperial_guard/__init__.py, `WhenThisRevealed` + `ResolveSpecialAbility`, modele baxter_stockman `ResoudreLeSpecial`).
#  - « Discard a ... » : `Faces.DiscardAll([carte choisie])`, choix du joueur `AskChooseFace` (modele gs240 Energy Transfer
#    pour la defausse, bt021 Dark Transformation pour la lecture de la classe).
#  - « a card you control with a printed [wild] resource » : `joueur.GetControlCards(CardFinder(has_printed_res="G"))`
#    (modele 28024 War Delivery pour `has_printed_res`, `convert_green_res=False` : seule une icone WILD imprimee compte).
#    L'icone du texte (etoile) = wild, comme l'etoile du coin de sk010 (RES=G declare).
#
# ⚠ Mots-pieges : « If you CANNOT » = aucune carte a defausser (le sbire n'a alors AUCUN autre effet : il s'engage normalement) ; « YOU » = le joueur a qui il est revele ; la clause « Special » vise l'environnement SETTING EN JEU. « you CONTROL » = en jeu ; « PRINTED [wild] » = l'icone imprimee, pas un generateur de ressource ni une conversion.


def GetAbilities() -> Sequence['Ability']:

    def effet_imprime(effect: 'Effect', joueur: 'Player') -> bool:
        candidates = [f for f in joueur.GetControlCards(CardFinder(has_printed_res="G")) if not Identity.IsType(f)]
        return DefausserUneParmi(effect, joueur, candidates)

    return [
        QuandRevele(effet_imprime),
    ]
