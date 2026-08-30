from . import *

# * Catalina Chavez — SBIRE NEMESIS, custom « jakxin »
# PV 4, ATQ 1*, MNG 1*, `Boost 2`, `Quickstrike 1`,
# `Nemesis "America Chavez"`, trait STARLING.
#
# Quickstrike.
# [star] Catalina Chavez gets each stat modifier in your play area (replacing
#   THW with SCH).
#
# ---------------------------------------------------------------------------
# CE QUI EST LU NATIVEMENT — AUCUN CODE ICI
#
# `Quickstrike 1` (`CanQuickstrike`, fiche mots-cles/quickstrike.md),
# `Boost 2`, `Nemesis` : trois cles de `desc` que le moteur lit tout seul.
# Coder l'attaque d'engagement a la main serait une capacite fantome.
#
# ⚠ `HP: "4"` SANS ETOILE, DELIBEREMENT (voir le grand commentaire du
# ms_america_nemesis/__init__.py). L'etoile imprimee sur les trois stats
# renvoie a la capacite ETOILEE, pas a un par-joueur ; le marqueur par-joueur
# de ce pack est l'icone PERSONNAGE, visible sur ma019. Ne pas « corriger ».
# ATQ/MNG « 1* » restent etoilees : la l'etoile a un autre sens pour le
# moteur, « 1 degat consecutif » (can_attack.py:47), qui est bien ce que la
# carte fait.
#
# ---------------------------------------------------------------------------
# CARTE DE REFERENCE — `08026` Taskmaster (pack bkw)
#
# Sbire NEMESIS lui aussi, dont le texte imprime est « Taskmaster gets +1 ATK
# and +1 SCH for each upgrade in your play area » et qui s'ecrit :
#   AbilityFactory.ThisGainKeyword(
#       lambda effect, ui:
#           len(effect.this.CastTo(Minion).GetEngagedPlayer().GetControlUpgrade()),
#       scheme=1, attack=1,
#       change_on_event=OnEvent.PlayAreaCard("YouControlCards"))
# Meme fabrique, meme declencheur de reevaluation, meme lecture de « ta zone
# de jeu » par `GetEngagedPlayer()`.
#
# DEUX `ThisGainKeyword` ici, et non une seule : Taskmaster ajoute la MEME
# valeur aux deux stats, Catalina non — son ATQ suit les modificateurs d'ATQ
# et son MNG suit ceux de CTR. Il faut donc deux compteurs distincts.
#
# ---------------------------------------------------------------------------
# « EACH STAT MODIFIER IN YOUR PLAY AREA » — ARBITRAGE DE L'UTILISATEUR
#
# Tranche le 30/08/2026 : lecture LITTERALE, TOUT ce qui est dans la zone de
# jeu du joueur, y compris les ameliorations posees sur ses ALLIES (Inspired,
# Laser Blaster, Danger Room Training...), pas seulement celles attachees a
# l'identite. C'est la lecture la plus punitive, et c'est celle qui est
# demandee.
#
# COMMENT ON LES MESURE : voir `SommeDesModificateurs`
# (ms_america/__init__.py). Ecart technique assume et documente la-bas — le
# moteur n'expose nulle part « la liste des modificateurs poses par une
# carte », on lit donc leur RESULTAT sur les personnages amis du joueur
# (`face.attack - face.printed_attack`).
#
# « (REPLACING THW WITH SCH) » : les modificateurs de CTR trouves dans la
# zone de jeu deviennent des modificateurs de MNG sur Catalina. C'est le sens
# de la parenthese, et c'est necessaire : un sbire n'a pas de CTR, seulement
# un MNG (`unit.Gain(thwart=...)` ne s'applique que si `HasThwart.IsType`,
# face_gain.py:120-125 — le bonus serait silencieusement perdu).
#
# Consequence en jeu, assumee : Star Flight (+1 CTR a Ms. America) donne
# +1 MNG a sa sœur, et Edges Syndrome (-1 a chaque pouvoir de base) lui
# donne -1 ATQ et -1 MNG. Les deux sens comptent.


def GetAbilities() -> Sequence['Ability']:

    def joueur_vise(effect: 'Effect') -> 'Player|None':
        this = effect.this.CastTo(Minion)
        try:
            return this.GetEngagedPlayer()
        except AssertionError:
            return None

    def modificateurs_atk(effect: 'Effect', ui: List['CardFace']) -> int:
        Unused(ui)
        return SommeDesModificateurs(joueur_vise(effect), 'attack')

    def modificateurs_thw(effect: 'Effect', ui: List['CardFace']) -> int:
        Unused(ui)
        return SommeDesModificateurs(joueur_vise(effect), 'thwart')

    return [
        AbilityFactory.ThisGainKeyword(
            modificateurs_atk,
            attack=1,
            change_on_event=OnEvent.PlayAreaCard("YouControlCards"),
        ),
        AbilityFactory.ThisGainKeyword(
            modificateurs_thw,
            scheme=1,
            change_on_event=OnEvent.PlayAreaCard("YouControlCards"),
        ),
    ]
