from . import *

# * Starbolt — SBIRE (Imperial Guard). IMPERIAL GUARD. PV 5, MNG 2, ATQ 2. 1 icone(s) de boost.
# When Revealed: Remove 1 all-purpose counter from a card you control. If you cannot, resolve the "Special" ability on the SETTING environment.
#
# Cartes de reference :
#  - « When Revealed ... If you cannot, resolve the "Special" ability on the SETTING environment » : `QuandRevele`
#    (imperial_guard/__init__.py, `WhenThisRevealed` + `ResolveSpecialAbility`, modele baxter_stockman `ResoudreLeSpecial`).
#  - « Remove 1 all-purpose counter from a card » : `Faces.RemoveCountersOn([carte], 1, 'all-purpose', effect)` (fiche
#    all-purpose-counter.md : le compteur polyvalent prend le nom du compteur que la carte porte).
#
# ⚠ Mots-pieges : « If you CANNOT » = aucune carte a defausser (le sbire n'a alors AUCUN autre effet : il s'engage normalement) ; « YOU » = le joueur a qui il est revele ; la clause « Special » vise l'environnement SETTING EN JEU. « ALL-PURPOSE counter » = un compteur defini par la carte qui le porte (pas des degats, pas de la menace) ; « a card YOU CONTROL » = identite, allie, amelioration ou soutien en jeu.


def GetAbilities() -> Sequence['Ability']:

    def effet_imprime(effect: 'Effect', joueur: 'Player') -> bool:
        candidates = [f for f in joueur.GetControlCards()
                      if CanPlaceCounter.IsType(f) and f.IsInPlay() and f.GetAllCounters() > 0]
        if not candidates:
            return False
        choisie = candidates[0] if len(candidates) == 1 else joueur.AskChooseFace(candidates, effect)
        if choisie is None:
            return False
        return bool(Faces.RemoveCountersOn([choisie], 1, 'all-purpose', effect))

    return [
        QuandRevele(effet_imprime),
    ]
