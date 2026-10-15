from . import *

# * Praxagora — SBIRE (Super-Skrull). ELITE. ROBOT. SCH 1, ATK 3★, 5 PV, 1 icone Y.
# ★ Praxagora's attacks gain overkill.
#
# Carte de reference : **`50107b`** M.O.D.O.K. (`UnitAttackGainKeyword("This",
# overkill=True, ranged=True)`) et fiche mots-cles/overkill.md ; meme fabrique que
# sk070 (Dorrek I, ranged) et sk073 (Dorrek VII, overkill) du scenario 1.
#
# ⚠ Mots-pieges : « attacks gain overkill » = TOUTES ses attaques ; l'exces de
# degats sur un allie vaincu va a l'identite de son controleur (regle native, RR
# 1.8 p.31) ; le ★ de la ligne comme celui du badge ATK renvoient au texte
# (convention validee le 15/10/2026), aucune valeur de plus.


def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.UnitAttackGainKeyword("This", overkill=True),
    ]
