# Cas test_capacites du scenario THE VAULT, 2e fichier : L'ACTIVATION DES VILAINS PAR « ACTIVATION ORDER » (livret p.1-2) et « le vilain »
# (plus petit Activation Order). Memes conventions et memes aides que `the_vault.py` ; prefixe de nom « [vt] ».
#
# Montage : heros en FORME HEROS et EPUISES (ils ne defendent pas : un vilain qui les attaque inflige son ATK pleine, que `degats_joueurs`
# lit sur l'identite de chaque joueur dans l'ordre des sieges). A deux joueurs : `spider_man` (01001a/b) et `hawkeye` (04001a/b).
# Hydra Mercenary (01101) : ATK 1, Guard. ATK des vilains (stade I) : Batroc 2, Mentallo 1, Grey Gargoyle 2, Hydro-Man 2, Mad Thinker 0, Nekra 2, Vapor 1, Venom 2.
import importlib.util as _imp
import os as _os

_spec = _imp.spec_from_file_location("cas_vt_aides", _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "the_vault.py"))
_h = _imp.module_from_spec(_spec)
_spec.loader.exec_module(_h)
_c, en_jeu, mechants_en_jeu, sous_le_vault = _h._c, _h.en_jeu, _h.mechants_en_jeu, _h.sous_le_vault
SC, SCX, HEROS = _h.SC, _h.SCX, _h.HEROS

UN = [HEROS, "Puzzle.Exhaust('01001a')"]
DEUX = [HEROS, "Puzzle.ChangeToFace('04001b', '04001a')", "Puzzle.Exhaust('01001a')", "Puzzle.Exhaust('04001a')"]
PHASE = ["Puzzle.RunVillainPhase()"]
J2 = {"heros2": "hawkeye", "main_exclusive": ["01090"]}

CAS = [
    # ============================================================ plus de vilains que de joueurs
    _c("vt-activation 2 vilains, 1 joueur : CHACUN active contre lui (Batroc 2 + Hydro-Man 2 = 4 degats)",
       "livret p.2 : plus de vilains que de joueurs -> « continue like this until all villains in play activate once »",
       UN + mechants_en_jeu("vt001", "vt007") + sous_le_vault("vt003"), PHASE, {"degats_joueurs": [4]}, main_exclusive=["01090"]),
    # ============================================================ autant de vilains que de joueurs : l'ordre
    _c("vt-activation 2 vilains, 2 joueurs : le plus petit ordre (Batroc 1) contre le 1er joueur, l'autre (Mentallo 2) contre le 2e",
       "livret p.2 : « The villain with the lowest activation order value activates against the first player. Then ... the second »",
       DEUX + mechants_en_jeu("vt001", "vt003") + sous_le_vault("vt005"), PHASE, {"degats_joueurs": [2, 1]}, **J2),
    _c("vt-activation l'ordre n'est PAS l'ordre d'arrivee en jeu : Mentallo (2) revele AVANT Batroc (1), Batroc agit quand meme contre le 1er joueur",
       "tri par Activation Order croissant, pas par place dans la zone des vilains",
       DEUX + mechants_en_jeu("vt003", "vt001") + sous_le_vault("vt005"), PHASE, {"degats_joueurs": [2, 1]}, **J2),
    # ============================================================ moins de vilains que de joueurs
    _c("vt-activation 1 vilain, 2 joueurs : il active contre CHAQUE joueur (Batroc 2 + 2)",
       "livret p.2 : moins de vilains que de joueurs -> « repeat this process until an activation is resolved against each player once »",
       DEUX + mechants_en_jeu("vt001") + sous_le_vault("vt005"), PHASE, {"degats_joueurs": [2, 2]}, **J2),
    # ============================================================ plus de vilains que de joueurs, 2 joueurs (exemple 2 du livret)
    _c("vt-activation 4 vilains, 2 joueurs (exemple du livret) : Batroc->J1, Mentallo->J2, Nekra->J1, Venom->J2 : J1 = 2+2, J2 = 1+2",
       "livret p.2 : exemple « two player game and four villains in play, Batroc 1, Mentallo 2, Nekra 6, Venom 8 »",
       DEUX + mechants_en_jeu("vt001", "vt003", "vt011", "vt015") + sous_le_vault("vt005"), PHASE, {"degats_joueurs": [4, 3]}, **J2),
    # ============================================================ « the villain »
    _c("vt-activation « the villain » d'une carte de rencontre = le plus petit Activation Order (Batroc 1 malgre Hydro-Man 4 revele avant)",
       "livret p.1 : « Encounter cards that refer to \"the villain\" only refer to the villain with the lowest activation order value »",
       mechants_en_jeu("vt007", "vt001") + sous_le_vault("vt003"), [], {"le_mechant": "vt001", "tous": 2}),
    # ============================================================ les sbires (livret p.2, « Minions activation »)
    _c("vt-activation sbires, 3 vilains pour 2 joueurs (exemple du livret) : le sbire du 1er joueur active UNE fois, apres la 1re activation d'un vilain contre lui",
       "livret p.2 : « minions activate after the first villain activation against a player to whom those minions are engaged ». Batroc->J1 (2), Nekra->J2 (2), Venom->J1 (2) + 1 sbire ATK 1 (Hydra Mercenary) : J1 = 2+1+2, J2 = 2",
       DEUX + mechants_en_jeu("vt001", "vt011", "vt015") + sous_le_vault("vt005") + ["Puzzle.PutIntoPlay('01101')"], PHASE,
       {"degats_joueurs": [5, 2]}, **J2),
    _c("vt-activation sbires, autant de vilains que de joueurs : le sbire du 1er joueur active apres SON vilain (J1 = Batroc 2 + sbire 1, J2 = Mentallo 1)",
       "livret p.2 : « If the number of villains is equal to or less than the number of players, minions activate as usual after the villain activates »",
       DEUX + mechants_en_jeu("vt001", "vt003") + sous_le_vault("vt005") + ["Puzzle.PutIntoPlay('01101')"], PHASE,
       {"degats_joueurs": [3, 1]}, **J2),
    # ============================================================ FAQ du livret : vilain etourdi
    _c("vt-activation FAQ : le vilain d'ordre 1 est etourdi, son activation est REMPLACEE par la carte d'etat ; le suivant (Mentallo 2) active contre le 2e joueur",
       "livret p.2, F.A.Q. : « It activates against the second player. The first player avoided its activation because the stunned status card replaced it. »",
       DEUX + mechants_en_jeu("vt001", "vt003") + sous_le_vault("vt005") + ["Puzzle.Stun('vt001')"], PHASE,
       {"degats_joueurs": [0, 1], "statuts_absents": [["vt001", "Stunned"]]}, **J2),
]
