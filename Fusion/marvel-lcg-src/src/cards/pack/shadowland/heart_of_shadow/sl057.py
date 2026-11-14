from . import *

# * Krahllak (I) — VILAIN, stade I. DEMON. HAND. SCH 2 / ATQ 3★ / PV 18 par joueur.
# Steady.
# [star] Interrupt : When Krahllak attacks you, you may place 1 corruption counter on your Creeping Corruption. If you do, Krahllak gets –3 ATK for this attack.
#
# Cartes de reference : hs142 Primal Strength (Interrupt facultatif d'une carte ENNEMIE quand le vilain vous attaque : `WhenUnitWouldAttack(Interrupt, ..., against_player="You")`
# + `MayChooseOneAbility`), 19018 Subdue / sk153 (« gets -N ATK for this attack » = `message.GainATKForThisAttack(-N, effect)`).
# ⚠ Mots-pieges : « you may place » : FACULTATIF, c'est le joueur attaque qui decide, et il faut une Creeping Corruption en jeu ; « IF YOU DO » : le -3 ATK n'a lieu que
#  si le jeton est pose ; « for THIS attack » : un malus d'attaque, pas permanent ; Steady est lu dans `desc` (fiche mots-cles/steady.md), rien a coder.


def GetAbilities() -> Sequence['Ability']:
    return [
        InterruptMoinsATQ(),
    ]
