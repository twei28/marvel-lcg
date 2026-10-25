# Cas test_capacites d'ALIEN VS. PREDATOR (prefixe `ap`), 2e fichier : complots 2 a 4, manigances permanentes, cartes Apex Standard qui
# touchent au compteur actif. Montage : voir tools/cas/alien_vs_predator.py (memes conventions, meme verificateur `ap_etat`).
import importlib.util as _imp
import os as _os

_spec = _imp.spec_from_file_location("cas_ap_aides", _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "alien_vs_predator.py"))
_h = _imp.module_from_spec(_spec)
_spec.loader.exec_module(_h)
HEROS, SC, SCX, _c = _h.HEROS, _h.SC, _h.SCX, _h._c

# Deck de rencontre sans boost + les cartes que la fouille doit trouver (la DERNIERE citee est le dessus).
def deck_avec(*ids):
    return ["Puzzle.EmptyEncounterDeck()",
            "Puzzle.CreateEncounterDeck(" + ", ".join(repr(i) for i in list(ids) + ["01105"] * 6) + ")"]


CAS = [
    # ============================================================ ap201-ap203 : Advance / Advance Again / Assault et le compteur
    _c("ap201 Advance : la Reine manigance, la menace va au complot principal (pas sur Expanding Hive) ; le compteur passe",
       "« The villain schemes. Place this threat on the main scheme. »",
       [], ["Puzzle.Reveal('ap201')"],
       {"menace": [["ap005b", 2], ["ap009", 2]], "actif": "ap002a"}),
    _c("ap202 Advance Again : la Reine manigance sur Expanding Hive et le compteur RESTE sur elle",
       "« The villain schemes. Do not move the active villain counter. »",
       [], ["Puzzle.Reveal('ap202')"],
       {"menace": [["ap009", 4], ["ap005b", 0]], "actif": "ap001a", "garde": False}),
    _c("ap203 Assault (heros) : la Reine attaque et le compteur RESTE sur elle",
       "« When Revealed (Hero): The villain attacks you. Do not move the active villain counter. »",
       [HEROS], ["Puzzle.Reveal('ap203')"],
       {"degats_identite": 1, "actif": "ap001a", "garde": False},
       passer_sur_option="Defense"),
    _c("ap203 Assault (alter-ego) : la carte gagne surge -> une carte de rencontre distribuee, aucune attaque",
       "« When Revealed (Alter-Ego): This card gains surge. » (le harnais joue l'ancien surge : la carte suivante, 01105, est revelee)",
       [], ["Puzzle.Reveal('ap203')"],
       {"defausse_rencontre": ["01105"], "actif": "ap001a", "degats_identite": 0}),

    # ============================================================ ap006a / ap006b : Battleground Earth
    _c("ap006a 2A : chaque joueur met en jeu, engages avec lui, un sbire YAUTJA et un sbire XENOMORPH du deck de rencontre",
       "« Each player searches the encounter deck and discard pile for a [[YAUTJA]] minion and a [[XENOMORPH]] minion and puts them into play "
       "engaged with them »",
       deck_avec("ap301", "ap018"), ["Puzzle.AdvanceMainScheme()"],
       {"complot": "ap006b", "en_jeu": ["ap301", "ap018"], "menace": [["ap006b", 2]]}),
    _c("ap006b le mechant actif ATTAQUE : il recoit une carte boost face cachee et le compteur passe",
       "« After a villain attacks, give it a facedown boost card, then move the active counter to the next villain »",
       [HEROS, "Puzzle.AdvanceMainScheme()"], ["Puzzle.Attack('ap001a')"],
       {"complot": "ap006b", "boosts_de": [["ap001a", 1]], "actif": "ap002a"},
       passer_sur_option="Defense"),
    _c("ap006b le mechant actif MANIGANCE : ni carte boost, ni deplacement du compteur (au stade 2, seule l'attaque compte)",
       "« After a villain ATTACKS »",
       ["Puzzle.AdvanceMainScheme()"], ["Puzzle.Scheme('ap001a')"],
       {"complot": "ap006b", "boosts_de": [["ap001a", 0]], "actif": "ap001a"}),
    _c("ap006b la Reine SONNEE au moment d'attaquer : le compteur passe, pas de carte boost (arbitrage du 25/10/2026)",
       "« Compteur oui, boost non » (la carte Sonne remplace l'attaque)",
       [HEROS, "Puzzle.AdvanceMainScheme()", "Puzzle.Stun('ap001a')"], ["Puzzle.Attack('ap001a')"],
       {"boosts_de": [["ap001a", 0]], "actif": "ap002a", "degats_identite": 0}),
    _c("ap006b 4[per_hero] menaces atteintes : chaque joueur recoit une carte de rencontre face cachee, puis 2[per_hero] menaces retirees",
       "« if there is at least 4[per_hero] threat here, deal each player a facedown encounter card. Then, remove 2[per_hero] threat »",
       ["Puzzle.AdvanceMainScheme()", "Puzzle.SetThreat('ap006b', 2)"], ["Puzzle.PlaceThreat('ap006b', 2)"],
       {"distribuees": 1, "menace": [["ap006b", 2]]}),
    _c("ap006b contre-cas : 3 menaces seulement -> aucune carte distribuee, la menace reste",
       "« at least 4[per_hero] »",
       ["Puzzle.AdvanceMainScheme()", "Puzzle.SetThreat('ap006b', 2)"], ["Puzzle.PlaceThreat('ap006b', 1)"],
       {"distribuees": 0, "menace": [["ap006b", 3]]}),

    # ============================================================ ap007a/b, ap008a/b : les stades du survivant
    _c("ap007a 3A : la fouille revele le premier attachement WEAPON (Plasmacaster, attache au Warlord) ; ap007b : un sbire YAUTJA revele",
       "3A « Discard ... until a [[WEAPON]] attachment is discarded. Reveal it » ; 3B « searches ... for a [[YAUTJA]] minion and reveals it »",
       deck_avec("ap301", "ap011"), ["Puzzle.Damage('ap001a', 99)"],
       {"complot": "ap007b", "attaches": [["ap002a", "ap011"]], "en_jeu": ["ap301"], "actif": "ap002a"}),
    _c("ap008a 4A : la fouille revele le premier attachement XENOMORPH (Piercing Pharynx, attache a la Reine) ; ap008b : un sbire XENOMORPH revele",
       "4A « until a [[XENOMORPH]] attachment is discarded. Reveal it » ; 4B « searches ... for a [[XENOMORPH]] minion and reveals it »",
       deck_avec("ap018", "ap015"), ["Puzzle.Damage('ap002a', 99)"],
       {"complot": "ap008b", "attaches": [["ap001a", "ap015"]], "en_jeu": ["ap018"], "actif": "ap001a"}),
    _c("ap007b 3B accompli (8[per_hero] menaces) : les joueurs PERDENT (pas de passage au complot suivant)",
       "« If this stage is completed, the players lose the game. »",
       ["Puzzle.Damage('ap001a', 99)"], ["Puzzle.SetThreat('ap007b', 8)"],
       {"fin": "perdu"}),
    _c("ap008b 4B accompli : les joueurs PERDENT",
       "« If this stage is completed, the players lose the game. »",
       ["Puzzle.Damage('ap002a', 99)"], ["Puzzle.SetThreat('ap008b', 8)"],
       {"fin": "perdu"}),

    # ============================================================ ap009 Expanding Hive
    _c("ap009 sans menace, Expanding Hive perd son icone Acceleration (2 -> 1 en jeu)",
       "« While there is no threat here, this scheme loses the [acceleration] icon »",
       [], ["Puzzle.SetThreat('ap009', 0)"],
       {"icones": [["Acceleration", 1]]}),
    _c("ap009 ligne de base : les deux manigances permanentes portent leur icone Acceleration (2 en jeu)",
       "contre-cas : avec de la menace, l'icone reste",
       [], [], {"icones": [["Acceleration", 2]]}),
    _c("ap009 un sbire a 3 PV imprimes (Xenomorph Drone) vaincu : donne au mechant actif comme carte boost face cachee",
       "« When a minion with 3 or more printed hit points is defeated, give it to the active villain as a facedown boost card »",
       ["Puzzle.PutIntoPlay('ap018')"], ["Puzzle.Damage('ap018', 3)"],
       {"boosts_de": [["ap001a", 1]], "defausse_rencontre": []}),
    _c("ap009 contre-cas : un sbire a 2 PV (Alien Scout) vaincu n'est PAS donne en boost",
       "« 3 or more printed hit points »",
       ["Puzzle.PutIntoPlay('ap101')"], ["Puzzle.Damage('ap101', 2)"],
       {"boosts_de": [["ap001a", 0]]}),

    # ============================================================ ap010 Skulls for the Taking
    _c("ap010 un allie vaincu par l'attaque d'un ennemi est glisse sous Skulls for the Taking",
       "« After an ally is defeated by an enemy attack, tuck it under here »",
       ["Puzzle.PutIntoPlay('01002', under_control=True)"], ["Puzzle.EnemyAttacks('ap002a', '01002')"],
       {"pose_sous": [["ap010", "01002"]]},
       passer_sur_option="Defense"),
    _c("ap010 contre-cas : un allie vaincu par des degats hors attaque n'est pas glisse",
       "« by an enemy ATTACK »",
       ["Puzzle.PutIntoPlay('01002', under_control=True)"], ["Puzzle.Damage('01002', 5)"],
       {"taille_pose_sous": [["ap010", 0]], "defausse": ["01002"]}),
    _c("ap010 Skulls quitte le jeu (la Reine vaincue retire les manigances permanentes) : l'allie glisse dessous va a la defausse de son proprietaire",
       "insert : « When this side scheme leaves play, any allies tucked under here are discarded to their owner's discard pile »",
       ["Puzzle.PutIntoPlay('01002', under_control=True)", "Puzzle.EnemyAttacks('ap002a', '01002')"], ["Puzzle.Damage('ap001a', 99)"],
       {"defausse": ["01002"], "hors_jeu": ["ap010"]},
       passer_sur_option="Defense"),
]
