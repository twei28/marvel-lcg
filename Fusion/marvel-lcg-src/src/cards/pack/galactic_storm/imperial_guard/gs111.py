from . import *

# * Warstar — SBIRE (Imperial Guard). IMPERIAL GUARD. ROBOT. PV 5, MNG 1, ATQ 2. 2 icone(s) de boost.
# When Revealed: Discard the top card of the encounter deck. If that card is an IMPERIAL GUARD minion, reveal it. Otherwise, resolve the "Special" ability on the SETTING environment.
#
# Cartes de reference :
#  - « When Revealed ... If you cannot, resolve the "Special" ability on the SETTING environment » : `QuandRevele`
#    (imperial_guard/__init__.py, `WhenThisRevealed` + `ResolveSpecialAbility`, modele baxter_stockman `ResoudreLeSpecial`).
#  - « Discard the top card of the encounter deck » : `Worlds.DiscardEncounterCards(1, effect)` ; « reveal it » : `face.Reveal(joueur,
#    effect)` sur la carte defaussee (modele baxter_stockman tx009).
#
# ⚠ Mots-pieges : « IF that card is an IMPERIAL GUARD MINION » (une traitrise IMPERIAL GUARD ne compte pas) ; « OTHERWISE » = Special ; deck vide : le moteur melange la defausse (regle du deck vide).


def GetAbilities() -> Sequence['Ability']:

    def effet_imprime(effect: 'Effect', joueur: 'Player') -> bool:
        faces = Worlds.DiscardEncounterCards(1, effect)
        if faces and Minion.IsType(faces[0]) and faces[0].HasTrait(IG):
            faces[0].Reveal(joueur, effect)
            return True
        return False

    return [
        QuandRevele(effet_imprime),
    ]
