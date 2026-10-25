# Cas test_capacites d'ALIEN VS. PREDATOR (prefixe `ap`), 4e fichier : deck Xenomorph (Alien Scout, ap101-ap104), Apex Standard
# (ap204-ap205) et Clan Yautja (ap301-ap306). Montage : voir tools/cas/alien_vs_predator.py (meme verificateur `ap_etat`).
#
# Valeurs utiles : Apex Predator ATK 3 ; Avengers Mansion (01091) soutien cout 4 > Surveillance Team (01064) cout 2.
import importlib.util as _imp
import os as _os

_spec = _imp.spec_from_file_location("cas_ap_aides", _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "alien_vs_predator.py"))
_h = _imp.module_from_spec(_spec)
_spec.loader.exec_module(_h)
HEROS, SC, SCX, _c = _h.HEROS, _h.SC, _h.SCX, _h._c


def deck_avec(*ids):
    """Deck de rencontre sans boost + ces cartes au DESSUS (la derniere citee est la carte du dessus)."""
    return ["Puzzle.EmptyEncounterDeck()",
            "Puzzle.CreateEncounterDeck(" + ", ".join(repr(i) for i in ["01105"] * 6 + list(ids)) + ")"]


def scout_pioche(cid, version, pioche):
    return _c(f"{cid} Alien Scout ({version}) pioche : distribue face cachee au joueur" + (", qui pioche 1 carte a la place" if pioche
                                                                                          else ", SANS pioche de remplacement"),
              "« Forced Interrupt: When you would draw ... this card from your deck, " + ("draw 1 card. " if pioche else "")
              + "Deal this card to yourself as a facedown encounter card »",
              ["Puzzle.EmptyHand()", f"Puzzle.CreatePlayerDeck('01090', '{cid}')"], ["Puzzle.Draw(1)"],
              {"scouts_distribues": 1, "taille_main": 1 if pioche else 0, "scouts_deck_joueur": 0})


CAS = [
    # ============================================================ Alien Scout (deck Xenomorph)
    scout_pioche("ap101", "01-04, Surge", True),
    scout_pioche("ap102", "05-08, Guard", False),
    scout_pioche("ap103", "09-12, Incite 1, Surge", True),
    scout_pioche("ap104", "13-16, Teamwork", True),
    _c("ap101 Alien Scout DEFAUSSE du deck du joueur : distribue face cachee (pas dans la defausse) et le joueur pioche 1 carte",
       "« When you would draw or DISCARD this card from your deck »",
       ["Puzzle.EmptyHand()", "Puzzle.CreatePlayerDeck('01090', 'ap101')"], ["Puzzle.Discard('ap101')"],
       {"scouts_distribues": 1, "scouts_defausse_joueur": 0, "taille_main": 1}),
    _c("ap102 contre-cas : un Alien Scout defausse depuis la MAIN n'est pas intercepte",
       "« from your DECK » seulement",
       ["Puzzle.EmptyHand()", "Puzzle.CreateHandCards('ap102')"], ["Puzzle.Discard('ap102')"],
       {"scouts_distribues": 0}),
    _c("ap101 Alien Scout vaincu : il va dans la defausse du JOUEUR (pas la defausse de rencontre)",
       "« When Defeated: Place Alien Scout in your discard pile »",
       ["Puzzle.PutIntoPlay('ap101')"], ["Puzzle.Damage('ap101', 2)"],
       {"scouts_defausse_joueur": 1, "pas_en_defausse_rencontre": ["ap101"]}),

    # ============================================================ Apex Standard
    _c("ap204 Cruel Intentions : chaque joueur recoit 1 carte de rencontre face cachee, le mechant actif 1 carte boost ; Incite 1",
       "« Deal each player 1 facedown encounter card. Give the villain 1 facedown boost card. » + Incite 1",
       [], ["Puzzle.Reveal('ap204')"],
       {"distribuees": 1, "boosts_de": [["ap001a", 1]], "menace": [["ap005b", 1]]}),
    _c("ap204 Boost : le joueur se distribue 1 carte de rencontre face cachee",
       "« [star] Boost: Deal yourself 1 facedown encounter card »",
       [], ["Puzzle.Boost('ap204')"],
       {"distribuees": 1}),
    _c("ap205 Overwhelming Force : le soutien au cout le plus eleve (Avengers Mansion, 4) est defausse",
       "« Discard the highest cost upgrade or support you control »",
       ["Puzzle.PutIntoPlay('01064', under_control=True)", "Puzzle.PutIntoPlay('01091', under_control=True)"], ["Puzzle.Reveal('ap205')"],
       {"defausse": ["01091"], "en_jeu": ["01064"]}),
    _c("ap205 rien a defausser : la carte gagne surge (la carte suivante, 01105, est revelee)",
       "« If no card was discarded this way, this card gains surge »",
       [], ["Puzzle.Reveal('ap205')"],
       {"defausse_rencontre": ["01105"]}),
    _c("ap205 Boost : le mechant recoit 1 carte boost supplementaire pour cette activation (01105 retournee puis defaussee)",
       "« [star] Boost: Give the villain 1 additional boost card for this activation »",
       [], ["Puzzle.Boost('ap205')"],
       {"defausse_rencontre": ["ap205", "01105"]}),

    # ============================================================ Clan Yautja
    _c("ap301 Yautja Young Blood : Incite 3 quand le Warlord est le mechant actif",
       "« Incite 2 (3 instead if Predator Warlord is the active villain) »",
       ["Puzzle.SetActiveVillain('ap002a')"], ["Puzzle.Reveal('ap301')"],
       {"menace": [["ap005b", 3]]}),
    _c("ap301 Incite 2 quand la Reine est active",
       "« Incite 2 »",
       [], ["Puzzle.Reveal('ap301')"],
       {"menace": [["ap005b", 2]]}),
    _c("ap301 When Defeated au stade 1 : 2 menaces sur The Ultimate Hunt",
       "« Place 2 threat on The Ultimate Hunt »",
       ["Puzzle.PutIntoPlay('ap301')"], ["Puzzle.Damage('ap301', 4)"],
       {"menace": [["ap005b", 2]]}),
    _c("ap301 When Defeated au stade 2, sans Expanding Hive : « if you cannot », melange dans le deck de rencontre",
       "« if you cannot shuffle Yautja Young Blood into the encounter deck »",
       ["Puzzle.AdvanceMainScheme()", "Puzzle.Remove('ap009')", "Puzzle.PutIntoPlay('ap301')"], ["Puzzle.Damage('ap301', 4)"],
       {"complot": "ap006b", "dans_deck_rencontre": ["ap301"]}),
    _c("ap302 Blooded Predator revele : l'identite est sonnee",
       "« When Revealed: Stun your identity »",
       [], ["Puzzle.Reveal('ap302')"],
       {"statuts": [["01001b", "Stunned"]], "degats_identite": 0}),
    _c("ap302 identite deja sonnee : 3 degats a la place",
       "« If you are already stunned, take 3 damage »",
       ["Puzzle.Stun('01001b')"], ["Puzzle.Reveal('ap302')"],
       {"degats_identite": 3}),
    _c("ap302 When Defeated : le Warlord recoit une carte Tenace",
       "« Give Predator Warlord a tough status card »",
       ["Puzzle.PutIntoPlay('ap302')"], ["Puzzle.Damage('ap302', 4)"],
       {"statuts": [["ap002a", "Tough"]]}),
    _c("ap302 Warlord deja Tenace (et pas d'Expanding Hive) : « if you cannot », la carte est donnee au mechant actif comme boost",
       "« If you cannot, give this card to the active villain as a facedown boost card »",
       ["Puzzle.Remove('ap009')", "Puzzle.Tough('ap002a')", "Puzzle.PutIntoPlay('ap302')"], ["Puzzle.Damage('ap302', 4)"],
       {"boosts_de": [["ap001a", 1]]}),
    _c("ap303 Predator Elite revele : un soutien du joueur est defausse",
       "« When Revealed: Discard an upgrade or support you control »",
       ["Puzzle.PutIntoPlay('01064', under_control=True)"], ["Puzzle.Reveal('ap303')"],
       {"defausse": ["01064"]}),
    _c("ap303 When Defeated : carte du dessus du deck (Black Cat, cout 2) -> 2 degats a un ennemi XENOMORPH (la Reine)",
       "« Discard the top card of your deck and deal damage to a [[XENOMORPH]] enemy equal to that cards printed cost »",
       ["Puzzle.CreatePlayerDeck('01002', '01002')", "Puzzle.PutIntoPlay('ap303')"], ["Puzzle.Damage('ap303', 6)"],
       {"degats": [["ap001a", 2]], "defausse": ["01002"]}),
    _c("ap304 Apex Predator attaque : perforante (la Tenace du heros est ignoree), 3 degats",
       "« [star] Apex Predator's attacks gain piercing »",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.PutIntoPlay('ap304')", "Puzzle.Tough('01001a')"], ["Puzzle.Attack('ap304')"],
       {"degats_identite": 3, "statuts_absents": [["01001a", "Tough"]]},
       passer_sur_option="Defense"),
    _c("ap304 attaque par le heros, la carte du dessus du deck de rencontre est une traitrise : l'attaquant est sonne",
       "« After a character attacks Apex Predator, discard the top card of the encounter deck. If that card is a treachery, stun the attacker »",
       [HEROS, "Puzzle.PutIntoPlay('ap304')"], ["Puzzle.Attack('01001a')"],
       {"statuts": [["01001a", "Stunned"]], "defausse_rencontre": ["01105"]}, cibles=["ap304"]),
    _c("ap304 contre-cas : la carte defaussee est un sbire -> pas d'etourdissement",
       "« If that card is a treachery »",
       [HEROS, "Puzzle.PutIntoPlay('ap304')"] + deck_avec("ap018"), ["Puzzle.Attack('01001a')"],
       {"statuts_absents": [["01001a", "Stunned"]], "defausse_rencontre": ["ap018"]}, cibles=["ap304"]),
    _c("ap305 The Hunt Begins : apres l'attaque d'un ennemi YAUTJA (le Warlord), il recoit une carte Tenace",
       "« Forced Response: After a [[YAUTJA]] enemy attacks, give it a tough status card »",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.SetActiveVillain('ap002a')", "Puzzle.Reveal('ap305')"], ["Puzzle.Attack('ap002a')"],
       {"statuts": [["ap002a", "Tough"]]},
       choisir_option="Place_2_threat_on_the_main_scheme"),
    _c("ap305 contre-cas : la Reine (XENOMORPH) attaque -> pas de carte Tenace",
       "« a [[YAUTJA]] enemy »",
       [HEROS, "Puzzle.Reveal('ap305')"], ["Puzzle.Attack('ap001a')"],
       {"statuts_absents": [["ap001a", "Tough"]]}),
    _c("ap305 les allies ne peuvent pas defendre : Black Cat n'est pas un defenseur legal contre la Reine ; le heros, si",
       "« Allies cannot defend against enemy attacks » (le defenseur force du harnais, `Puzzle.Attack(defender=)`, contourne la question : on "
       "mesure la legalite `IsCanDefense` que le moteur consulte avant d'offrir la defense)",
       [HEROS, "Puzzle.PutIntoPlay('01002', under_control=True)"], ["Puzzle.Reveal('ap305')"],
       {"peut_defendre": [["01002", "ap001a", False], ["01001a", "ap001a", True]]}),
    _c("ap305 ligne de base : sans The Hunt Begins, Black Cat peut defendre",
       "contre-cas",
       [HEROS, "Puzzle.PutIntoPlay('01002', under_control=True)"], [],
       {"peut_defendre": [["01002", "ap001a", True]]}),
    _c("ap305 When Defeated : un ennemi est sonne (1re option)",
       "« When Defeated: Stun or confuse an enemy »",
       ["Puzzle.Reveal('ap305')"], ["Puzzle.SetThreat('ap305', 0)"],
       {"statuts": [["ap001a", "Stunned"]]}),
    _c("ap306 Cloaking Device sur le Warlord : -2 degats par attaque (l'attaque de base du heros, 2, ne lui fait rien)",
       "« Reduce the amount of damage attached enemy takes from each attack by 2 »",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.Reveal('ap306')"], ["Puzzle.Attack('01001a')"],
       {"attaches": [["ap002a", "ap306"]], "degats": [["ap002a", 0]]}, cibles=["ap002a"]),
    _c("ap306 Reponse de heros apres une attaque de base contre le porteur : depenser [energy][physical] -> Cloaking Device defaussee",
       "« Hero Action: After a hero makes a basic attack against this enemy, spend [energy][physical] → discard this card » (arbitrage 3 : Reponse)",
       [HEROS, "Puzzle.Reveal('ap306')"], ["Puzzle.Attack('01001a')"],
       {"defausse_rencontre": ["ap306"]}, cibles=["ap002a"], accepter_choix=True,
       main_exclusive=["01002", "01058"], payer_avec=["01002", "01058"]),
]
