from . import *

# * Xenomorph Queen — SBIRE nemesis de Predator (set « Predator Nemesis »). ELITE. XENOMORPH. PV 9, MNG 1, ATQ 3★, Boost 2.
# Toughness.
# ★ Xenomorph Queen's attacks gain piercing and overkill.
# (Predator's nemesis minion.)
#
# Cartes de reference :
#  - `UnitAttackGainKeyword("This", piercing=True, overkill=True)` (27078, ho016 ; Throg al002 pour overkill) : « X's attacks
#    gain ... » ; fiches mots-cles/piercing.md, overkill.md ;
#  - `Toughness` : base automatique (`desc.Toughness`, fiche toughness.md), AUCUN code ; `desc.Nemesis` : base automatique.
#
# ⚠ Mots-pieges :
#  - « ★ » devant la phrase = icone etoile imprimee, PAS un « Boost: » : la capacite est CONSTANTE (convention moteur,
#    RECETTES §3), pas liee a une carte de boost ; l'ATQ imprimee « 3★ » porte la meme etoile.
#  - « Xenomorph Queen's attacks » : ses attaques a elle (`attacker="This"`), pas celles des autres Xenomorphes.
#  - « piercing AND overkill » : les deux ; la Reine est ELITE (pas de limite en jeu, une seule carte).


def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.UnitAttackGainKeyword(
            "This",
            piercing=True,
            overkill=True,
        ),
    ]
