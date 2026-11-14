from . import *

# * Gladiator — SBIRE (Imperial Guard). ELITE. IMPERIAL GUARD. PV 8, MNG 1, ATQ 3. 3 icone(s) de boost.
# When Revealed: Defeat a non-scenario specific ally you control. If no ally was defeated this way, resolve the "Special" ability on the SETTING environment.
#
# Cartes de reference :
#  - « When Revealed ... If you cannot, resolve the "Special" ability on the SETTING environment » : `QuandRevele`
#    (imperial_guard/__init__.py, `WhenThisRevealed` + `ResolveSpecialAbility`, modele baxter_stockman `ResoudreLeSpecial`).
#  - « Defeat an ally » : `ally.Defeated(None, effect)` (modele gs118a pour `Defeated(None, ..)`).
#  - « Victory 0 » : BASE AUTOMATIQUE `desc.Victory = "0"` (fiche victory.md, modele 60024 De-escalation).
#
# ⚠ Mots-pieges : « NON-SCENARIO SPECIFIC » = ni Rick Jones ni Lilandra (classe Encounter) ; « you CONTROL » ; « If NO ally was defeated » : un allie dont la defaite est empechee (Poigne, immunite) ne compte pas.


def GetAbilities() -> Sequence['Ability']:

    def effet_imprime(effect: 'Effect', joueur: 'Player') -> bool:
        candidates = [f for f in joueur.GetControlAllies() if f.IsInPlay() and not EstSpecifiqueAuScenario(f)]
        if not candidates:
            return False
        choisi = candidates[0] if len(candidates) == 1 else joueur.AskChooseFace(candidates, effect)
        if choisi is None:
            return False
        choisi.Defeated(None, effect)
        return not choisi.IsInPlay()

    return [
        QuandRevele(effet_imprime),
    ]
