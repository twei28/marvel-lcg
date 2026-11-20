from . import *

# * Hobgoblin — SBIRE (Imperial Guard). IMPERIAL GUARD. PV 4, MNG 3, ATQ 1. 2 icone(s) de boost.
# When Revealed: Resolve a "When Revealed" ability of another IMPERIAL GUARD minion in play. If no ability was resolved this way, resolve the "Special" ability on the SETTING environment.
#
# Cartes de reference :
#  - « When Revealed ... If you cannot, resolve the "Special" ability on the SETTING environment » : `QuandRevele`
#    (imperial_guard/__init__.py, `WhenThisRevealed` + `ResolveSpecialAbility`, modele baxter_stockman `ResoudreLeSpecial`).
#  - « Resolve a When Revealed ability of another card » : `Faces.ResolveAbility([carte], joueur, AbilityType.WhenRevealed,
#    effect)`, modeles sm 27083 For Whom the Bell Tolls et skrull_menace/lyja sk046 Mole (resout l'effet SEUL, sans le reste de la revelation).
#
# ⚠ Mots-pieges : « ANOTHER » sbire IMPERIAL GUARD (pas lui-meme) EN JEU ; « a » : le joueur choisit s'il y en a plusieurs ; « If NO ability was resolved » = aucun autre sbire IMPERIAL GUARD en jeu ; « YOU » reste le joueur qui resout.


def GetAbilities() -> Sequence['Ability']:

    def effet_imprime(effect: 'Effect', joueur: 'Player') -> bool:
        autres = SbiresImperialGuard(effect, sauf=effect.this)
        if not autres:
            return False
        choisi = autres[0] if len(autres) == 1 else joueur.AskChooseFace(autres, effect)
        if choisi is None:
            return False
        return bool(Faces.ResolveAbility([choisi], joueur, AbilityType.WhenRevealed, effect))

    return [
        QuandRevele(effet_imprime),
    ]
