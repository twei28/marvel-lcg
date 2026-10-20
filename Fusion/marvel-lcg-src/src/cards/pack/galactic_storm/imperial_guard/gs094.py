from . import *

# * Astra — SBIRE (Imperial Guard). IMPERIAL GUARD. PV 4, MNG 2, ATQ 1. 1 icone(s) de boost.
# When Revealed: Discard an identity-specific card you control. If you cannot, resolve the "Special" ability on the SETTING environment.
#
# Cartes de reference :
#  - « When Revealed ... If you cannot, resolve the "Special" ability on the SETTING environment » : `QuandRevele`
#    (imperial_guard/__init__.py, `WhenThisRevealed` + `ResolveSpecialAbility`, modele baxter_stockman `ResoudreLeSpecial`).
#  - « Discard a ... » : `Faces.DiscardAll([carte choisie])`, choix du joueur `AskChooseFace` (modele gs240 Energy Transfer
#    pour la defausse, bt021 Dark Transformation pour la lecture de la classe).
#  - « identity-specific » : `face.IsClass("IdentitySpecific")`, modele beast bt021 Dark Transformation.
#  - « a card you control » : `joueur.GetControlCards()` (allies, ameliorations, soutiens ; l'identite elle-meme ne se defausse pas).
#
# ⚠ Mots-pieges : « If you CANNOT » = aucune carte a defausser (le sbire n'a alors AUCUN autre effet : il s'engage normalement) ; « YOU » = le joueur a qui il est revele ; la clause « Special » vise l'environnement SETTING EN JEU. « you CONTROL » = en jeu (pas la main) ; « IDENTITY-SPECIFIC » = classe propre a l'identite (pas Basic, pas un aspect, pas une carte de rencontre).


def GetAbilities() -> Sequence['Ability']:

    def effet_imprime(effect: 'Effect', joueur: 'Player') -> bool:
        candidates = [f for f in joueur.GetControlCards()
                      if ClassCard.IsType(f) and not Identity.IsType(f) and f.IsClass("IdentitySpecific")]
        return DefausserUneParmi(effect, joueur, candidates)

    return [
        QuandRevele(effet_imprime),
    ]
