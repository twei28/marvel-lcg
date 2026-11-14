from . import *

# * Oracle — SBIRE (Imperial Guard). IMPERIAL GUARD. PV 4, MNG 3, ATQ 1. 1 icone(s) de boost.
# When Revealed: You are confused. If you were already confused, resolve the "Special" ability on the SETTING environment.
#
# Cartes de reference :
#  - « When Revealed ... If you cannot, resolve the "Special" ability on the SETTING environment » : `QuandRevele`
#    (imperial_guard/__init__.py, `WhenThisRevealed` + `ResolveSpecialAbility`, modele baxter_stockman `ResoudreLeSpecial`).
#  - « You are confused » : `Faces.GiveStatus([identite], "Confused", effect)` (modele sk151 / 52037 pour `GiveStatus`) ; le
#    moteur refuse une 2e carte d'etat (Solide/steady en accepte deux : alors on n'etait pas « deja confused »).
#
# ⚠ Mots-pieges : « If you WERE ALREADY confused » : le statut deja pose ; « YOU » = l'identite du joueur (alter ego compris) ; la regle d'etat de la carte (Steady, immunites) decide si le statut est pose.


def GetAbilities() -> Sequence['Ability']:

    def effet_imprime(effect: 'Effect', joueur: 'Player') -> bool:
        return bool(Faces.GiveStatus([joueur.GetIdentity()], "Confused", effect))

    return [
        QuandRevele(effet_imprime),
    ]
