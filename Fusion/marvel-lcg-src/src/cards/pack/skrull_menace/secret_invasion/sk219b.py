from . import *

# * Ssrov — SBIRE (paquet IMPOSTOR, face B). IMPOSTOR. REVEALED. SKRULL. 4 PV, SCH 1, ATQ 2.
# [star] While the villain has the [[REVEALED]] trait, Ssrov gets +1 SCH and +1 ATK.
# When Revealed: Heal all damage from Ssrov and put him into play engaged with you.
#
# Cartes de reference :
#  - « When Revealed: Heal all damage from X and put it into play engaged with you » : **`gambit 37034`** Psionic Shield
#    (`HealthUnits([unite], "All", effect)`) et **`sk098`** (le sbire engage le joueur qui revele) ; helper `SbireImpostor()`.
# ★ « While the villain has the REVEALED trait, X gets +1 SCH and +1 ATK » : **`hela 21136a`** (`ThisGainKeyword(check_fn, scheme=1,
# attack=1, change_on_event=...)`, valeur recalculee a chaque evenement) ; evenement : le retournement du mechant (`OnEvent.Faceup`).
#
# ⚠ Mots-pieges : « heal ALL damage » (un allie retourne arrive blesse) ; « engaged with YOU » : le joueur qui revele
# (pour un allie retourne : celui qui le controlait avant, livret p. 16) ; la face sbire quitte le jeu vers la DEFAUSSE
# IMPOSTOR (livret p. 16, liaison `BindDiscardPile`).


def GetAbilities() -> Sequence['Ability']:
    def mechant_revele(effect: 'Effect', faces: List['CardFace']) -> int:
        Unused(faces)
        return 1 if VerankeRevelee(effect) else 0

    return [
        *SbireImpostor(),
        AbilityFactory.ThisGainKeyword(mechant_revele, scheme=1, attack=1,
                                       change_on_event=[OnEvent.Faceup(Villain)]),
    ]
