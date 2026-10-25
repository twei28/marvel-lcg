# Cas test_capacites d'ALIEN VS. PREDATOR (prefixe `ap`), 3e fichier : les cartes de rencontre du set « Alien vs. Predator »
# (ap011-ap033). Montage : voir tools/cas/alien_vs_predator.py (memes conventions, meme verificateur `ap_etat`).
#
# Valeurs utiles : Alien Queen A SCH 2 / ATK 1 ; Predator Warlord A SCH 1 / ATK 2 ; Spider-Man ATK 2, DEF 3, main 5 (Peter Parker : 6) ;
# Black Cat (01002, allie propre a Spider-Man) cout 2, PV 2, ressource Y ; Daredevil (01058) ressource R ; Great Responsibility (01061)
# ressource B (le pilote compte les ressources en NOMBRE : payer [energy][physical] avec Energy YY s'arrete a 2 Y et echoue) ; Surveillance Team (01064) soutien cout 2 ; remplissage du deck de rencontre : 01098 (neutre sans Rhino).
import importlib.util as _imp
import os as _os

_spec = _imp.spec_from_file_location("cas_ap_aides", _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "alien_vs_predator.py"))
_h = _imp.module_from_spec(_spec)
_spec.loader.exec_module(_h)
HEROS, SC, SCX, _c = _h.HEROS, _h.SC, _h.SCX, _h._c


def deck_avec(*ids):
    """Deck de rencontre sans boost + ces cartes au DESSUS (la derniere citee est la carte du dessus)."""
    return ["Puzzle.EmptyEncounterDeck()",
            "Puzzle.CreateEncounterDeck(" + ", ".join(repr(i) for i in ["01098"] * 6 + list(ids)) + ")"]


CAS = [
    # ============================================================ ap011 Plasmacaster
    _c("ap011 Plasmacaster s'attache au Warlord avec 3 compteurs plasma",
       "« Attach to Predator Warlord » + « Uses (3 plasma counters) »",
       [], ["Puzzle.Reveal('ap011')"],
       {"attaches": [["ap002a", "ap011"]], "compteurs": [["ap011", "plasma", 3]]}),
    _c("ap011 sans Predator Warlord, Plasmacaster gagne surge (une carte distribuee)",
       "« Otherwise, this card gains surge » (regle v18 : une carte distribuee face cachee)",
       ["Puzzle.RemoveVillain('ap002a')"], ["Puzzle.Reveal('ap011')"],
       {"distribuees": 1}),
    _c("ap011 le Warlord attaque : 1 compteur plasma retire, carte du dessus du deck defaussee (Black Cat, cout 2) -> 2 degats indirects",
       "« remove 1 plasma counter from here and discard the top card of your deck → take indirect damage equal to that card's printed cost »",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.SetActiveVillain('ap002a')", "Puzzle.Reveal('ap011')",
        "Puzzle.CreatePlayerDeck('01002', '01002', '01002')"], ["Puzzle.Attack('ap002a')"],
       {"compteurs": [["ap011", "plasma", 2]], "degats_identite": 2, "defausse": ["01002"]},
       choisir_option="Place_2_threat_on_the_main_scheme"),

    # ============================================================ ap012 Yautja Wrist Blades
    _c("ap012 Wrist Blades sur le Warlord : +2 ATK et attaque perforante (la Tenace du heros est ignoree) -> 4 degats",
       "ATK +2 ; « [star] Attached enemy's attacks gain piercing »",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.SetActiveVillain('ap002a')", "Puzzle.Reveal('ap012')", "Puzzle.Tough('01001a')"],
       ["Puzzle.Attack('ap002a')"],
       {"attaches": [["ap002a", "ap012"]], "degats_identite": 4, "statuts_absents": [["01001a", "Tough"]]},
       choisir_option="Place_2_threat_on_the_main_scheme", passer_sur_option="Defense"),
    _c("ap012 sans Predator Warlord, Wrist Blades s'attache a un sbire YAUTJA",
       "« If you cannot, attach to a [[YAUTJA]] minion »",
       ["Puzzle.RemoveVillain('ap002a')", "Puzzle.PutIntoPlay('ap301')"], ["Puzzle.Reveal('ap012')"],
       {"attaches": [["ap301", "ap012"]]}),
    _c("ap012 Hero Action : depenser [energy][physical] -> Wrist Blades defaussee",
       "« Hero Action: Spend [energy][physical] resources → discard this card »",
       [HEROS, "Puzzle.Reveal('ap012')"], ["Puzzle.Action('ap012', 'HeroAction')"],
       {"defausse_rencontre": ["ap012"]},
       main_exclusive=["01002", "01058"], payer_avec=["01002", "01058"]),

    # ============================================================ ap013 Thermal Target / ap016 Facehugger
    _c("ap013 Thermal Target s'attache a l'identite ; fin du tour : 2 degats et 2 menaces sur le complot principal",
       "« Attach to your identity. Forced Response: After your turn ends, take 2 damage and place 2 threat on the main scheme »",
       ["Puzzle.EmptyHand()", "Puzzle.Reveal('ap013')"], ["Puzzle.EndPlayerTurn()"],
       {"attaches": [["01001b", "ap013"]], "degats_identite": 2, "menace": [["ap005b", 2]]}),
    _c("ap013 Alter-Ego Action : trouver un sbire YAUTJA et le reveler -> Thermal Target defaussee",
       "« Alter-Ego Action: Find a [[YAUTJA]] minion and reveal it → discard this card »",
       deck_avec("ap301") + ["Puzzle.Reveal('ap013')"], ["Puzzle.Action('ap013', 'AlterEgoAction')"],
       {"en_jeu": ["ap301"], "defausse_rencontre": ["ap013"]}),
    _c("ap013 Boost : la carte est revelee (attachee a l'identite)",
       "« [star] Boost: Reveal this card »",
       [], ["Puzzle.Boost('ap013')"],
       {"attaches": [["01001b", "ap013"]]}),
    _c("ap016 Facehugger : fin du tour -> 2 degats et 2 menaces sur le complot",
       "« Forced Response: After your turn ends, take 2 damage and place 2 threat on the main scheme »",
       ["Puzzle.EmptyHand()", "Puzzle.Reveal('ap016')"], ["Puzzle.EndPlayerTurn()"],
       {"attaches": [["01001b", "ap016"]], "degats_identite": 2, "menace": [["ap005b", 2]]}),
    _c("ap016 Alter-Ego Action : chercher un sbire XENOMORPH dans le deck de rencontre et le reveler -> Facehugger defaussee",
       "« Search the encounter deck and discard pile for a [[XENOMORPH]] minion and reveal it → discard this card »",
       deck_avec("ap018") + ["Puzzle.Reveal('ap016')"], ["Puzzle.Action('ap016', 'AlterEgoAction')"],
       {"en_jeu": ["ap018"], "defausse_rencontre": ["ap016"]}),

    # ============================================================ ap015 Piercing Pharynx
    _c("ap015 Piercing Pharynx s'attache a la Reine et lui donne une carte Tenace",
       "« Attach to Alien Queen and give her a tough status card »",
       [], ["Puzzle.Reveal('ap015')"],
       {"attaches": [["ap001a", "ap015"]], "statuts": [["ap001a", "Tough"]]}),
    _c("ap015 la Reine gagne riposte 1 : le heros qui l'attaque subit 1 degat",
       "« Alien Queen gains retaliate 1 »",
       [HEROS, "Puzzle.Reveal('ap015')"], ["Puzzle.Attack('01001a')"],
       {"degats_identite": 1}, cibles=["ap001a"]),
    _c("ap015 Hero Action (Warlord en jeu) : depenser [energy][mental] -> Piercing Pharynx defaussee",
       "« Hero Action: If Predator Warlord is in play, spend [energy][mental] resources → discard this card »",
       [HEROS, "Puzzle.Reveal('ap015')"], ["Puzzle.Action('ap015', 'HeroAction')"],
       {"defausse_rencontre": ["ap015"]},
       main_exclusive=["01002", "01061"], payer_avec=["01002", "01061"]),

    # ============================================================ ap018 Xenomorph Drone
    _c("ap018 Incite 3 quand la Reine est le mechant active",
       "« Incite 2 (3 instead if Alien Queen is the active villain) »",
       [], ["Puzzle.Reveal('ap018')"],
       {"menace": [["ap005b", 3]]}),
    _c("ap018 Incite 2 quand le Warlord est le mechant actif",
       "« Incite 2 »",
       ["Puzzle.SetActiveVillain('ap002a')"], ["Puzzle.Reveal('ap018')"],
       {"menace": [["ap005b", 2]]}),
    _c("ap018 When Defeated : 2 menaces retirees d'Expanding Hive (le Drone part en boost par la Hive)",
       "« Remove 2 threat from Expanding Hive »",
       ["Puzzle.PutIntoPlay('ap018')"], ["Puzzle.Damage('ap018', 3)"],
       {"menace": [["ap009", 0]], "boosts_de": [["ap001a", 1]]}),
    _c("ap018 When Defeated sans Expanding Hive : « if you cannot », le Drone est melange dans le deck de rencontre",
       "« If you cannot, shuffle Xenomorph Drone into the encounter deck »",
       ["Puzzle.Remove('ap009')", "Puzzle.PutIntoPlay('ap018')"], ["Puzzle.Damage('ap018', 3)"],
       {"dans_deck_rencontre": ["ap018"]}),
    _c("ap018 Hive sans menace : le Drone deja donne en boost par la Hive y RESTE (arbitrage du 25/10/2026)",
       "Expanding Hive passe avant le « When Defeated » : pas de melange",
       ["Puzzle.SetThreat('ap009', 0)", "Puzzle.PutIntoPlay('ap018')"], ["Puzzle.Damage('ap018', 3)"],
       {"boosts_de": [["ap001a", 1]]}),

    # ============================================================ ap020 Xenomorph Warrior / ap021 Alien Praetorian
    _c("ap020 When Defeated : defausse le dessus du deck (Alien Praetorian, boost 3) -> 3 degats au Warlord (YAUTJA)",
       "« deal 1 damage to a [[YAUTJA]] enemy for each icon ([star] and [boost]) in that card's boost area »",
       deck_avec("ap021") + ["Puzzle.PutIntoPlay('ap020')"], ["Puzzle.Damage('ap020', 6)"],
       {"degats": [["ap002a", 3]], "defausse_rencontre": ["ap021"]}),
    _c("ap021 Alien Praetorian : au debut de la phase du mechant, il s'engage avec le premier joueur",
       "« Forced Response: After the villain phase begins, Alien Praetorian engages the first player »",
       ["Puzzle.PutIntoPlay('ap021')", "Puzzle.Engage('ap021', 1)"], ["Puzzle.BeginVillainPhase()"],
       {"engage_avec": [["ap021", 0]]}, heros2="hawkeye"),

    # ============================================================ ap022 Chestburster
    _c("ap022 Chestburster s'attache a un sbire XENOMORPH",
       "« Attach to a [[XENOMORPH]] minion »",
       ["Puzzle.PutIntoPlay('ap018')"], ["Puzzle.Reveal('ap022')"],
       {"attaches": [["ap018", "ap022"]]}),
    _c("ap022 sans sbire XENOMORPH, Chestburster s'attache au mechant actif",
       "« Otherwise attach to the active villain »",
       ["Puzzle.SetActiveVillain('ap002a')"], ["Puzzle.Reveal('ap022')"],
       {"attaches": [["ap002a", "ap022"]]}),
    _c("ap022 l'ennemi porteur attaque : attaque perforante (Tenace ignoree) ; a la fin, l'identite est sonnee et Chestburster defaussee",
       "« this attack gains piercing. At the end of this attack, stun your identity and discard this card »",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.PutIntoPlay('ap018')", "Puzzle.Reveal('ap022')", "Puzzle.Tough('01001a')"],
       ["Puzzle.Attack('ap018')"],
       {"statuts": [["01001a", "Stunned"]], "statuts_absents": [["01001a", "Tough"]], "defausse_rencontre": ["ap022"]},
       passer_sur_option="Defense"),

    # ============================================================ ap023 Hive Incursion
    _c("ap023 Hive Incursion : la main est defaussee puis le joueur pioche jusqu'a sa taille de main (6 en alter-ego)",
       "« Discard your hand. Draw up to your hand size. »",
       [], ["Puzzle.Reveal('ap023')"],
       {"taille_main": 6, "defausse_joueur": 6}),
    _c("ap023 Boost : le « When Revealed » est resolu (main defaussee puis repiochee)",
       "« [star] Boost: Resolve the \"When Revealed\" ability on this card »",
       [], ["Puzzle.Boost('ap023')"],
       {"taille_main": 6, "defausse_joueur": 6}),

    # ============================================================ ap024 Predator's Prize
    _c("ap024 Predator's Prize, option 1 : la carte est donnee au mechant actif comme boost face cachee",
       "« give this card to the active villain as a facedown boost card »",
       [], ["Puzzle.Reveal('ap024')"],
       {"boosts_de": [["ap001a", 1]]}),
    _c("ap024 Predator's Prize, option 2 : l'allie propre a l'identite (Black Cat) est retire de la partie",
       "« or find your identity-specific ally and remove it from the game »",
       [], ["Puzzle.Reveal('ap024')"],
       {"retires": ["01002"], "boosts_de": [["ap001a", 0]]},
       choisir_option="Remove_your_identity-specific_ally_from_the_game"),

    # ============================================================ ap025 Brood Breakout
    _c("ap025 Brood Breakout : la fouille revele un sbire XENOMORPH, qui recoit une carte Tenace en entrant en jeu",
       "« When Revealed: Discard ... until a [[XENOMORPH]] minion is discarded. Reveal it » + « After a [[XENOMORPH]] minion enters play, give it a "
       "tough status card »",
       deck_avec("ap018", "01098"), ["Puzzle.Reveal('ap025')"],
       {"en_jeu": ["ap018"], "statuts": [["ap018", "Tough"]]}),

    # ============================================================ ap026 Alien Assault
    _c("ap026 Alien Assault, la Reine active : l'identite est desorientee",
       "« If Alien Queen is the active villain, confuse your identity »",
       [], ["Puzzle.Reveal('ap026')"],
       {"statuts": [["01001b", "Confused"]], "statuts_absents": [["01001b", "Stunned"]]}),
    _c("ap026 Alien Assault, le Warlord actif : l'identite est sonnee",
       "« If Predator Warlord is the active villain, stun your identity »",
       ["Puzzle.SetActiveVillain('ap002a')"], ["Puzzle.Reveal('ap026')"],
       {"statuts": [["01001b", "Stunned"]], "statuts_absents": [["01001b", "Confused"]]}),
    _c("ap026 Boost : apres cette activation, le compteur actif ne bouge pas",
       "« [star] Boost: After this activation ends, do not move the active counter to the next villain »",
       [], ["Puzzle.Boost('ap026')"],
       {"actif": "ap001a", "garde": False}),

    # ============================================================ ap027 Killing Ground
    _c("ap027 Killing Ground : toute la menace de la manigance de mechant la plus chargee (Skulls, 3) passe sur le complot",
       "« Move all threat from the villain's side scheme with the most threat to the main scheme »",
       ["Puzzle.EmptyHand()", "Puzzle.SetThreat('ap010', 3)"], ["Puzzle.Reveal('ap027')"],
       {"menace": [["ap010", 0], ["ap009", 2], ["ap005b", 3]], "pret": ["01001b"]}),
    _c("ap027 aucune menace deplacee : l'identite est inclinee",
       "« If no threat was moved this way, exhaust your identity »",
       ["Puzzle.SetThreat('ap009', 0)", "Puzzle.SetThreat('ap010', 0)"], ["Puzzle.Reveal('ap027')"],
       {"exhausted": ["01001b"]}),
    _c("ap027 identite deja inclinee : « if you cannot », sonnee (1re option)",
       "« If you cannot, stun or confuse your identity »",
       ["Puzzle.SetThreat('ap009', 0)", "Puzzle.SetThreat('ap010', 0)", "Puzzle.Exhaust('01001b')"], ["Puzzle.Reveal('ap027')"],
       {"statuts": [["01001b", "Stunned"]]}),

    # ============================================================ ap028 Predator's Prey
    _c("ap028 Predator's Prey : defausse du deck jusqu'a un allie (Black Cat), mis en jeu, attaque par le Warlord (ATK 2+1), vaincu (glisse sous Skulls), 1 degat d'exces a l'identite",
       "« Discard cards from the top of your deck until you discard an ally, then put that ally into play under your control. The active villain "
       "attacks that ally. This attack gains overkill. »",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.SetActiveVillain('ap002a')", "Puzzle.CreatePlayerDeck('01090', '01002', '01089')"],
       ["Puzzle.Reveal('ap028')"],
       {"defausse": ["01089"], "pose_sous": [["ap010", "01002"]], "degats_identite": 1},
       choisir_option="Predator_Warlord_gets_+1_ATK_for_this_attack", passer_sur_option="Defense"),

    # ============================================================ ap029 Predation
    _c("ap029 Predation : la Reine soignee de 3 et Tenace ; 3 degats a un ennemi sans le trait XENOMORPH (le Warlord)",
       "« Heal 3 damage from the active villain and give them a tough status card. Deal 3 damage to an enemy whose trait does not match »",
       ["Puzzle.Damage('ap001a', 5)"], ["Puzzle.Reveal('ap029')"],
       {"degats": [["ap001a", 2], ["ap002a", 3]], "statuts": [["ap001a", "Tough"]]}),
    _c("ap029 Boost : 2 menaces sur CHAQUE manigance (complot + Hive + Skulls)",
       "« [star] Boost: Place 2 threat on each scheme »",
       [HEROS, "Puzzle.EmptyHand()"], ["Puzzle.Boost('ap029')"],
       {"menace": [["ap005b", 2], ["ap009", 4], ["ap010", 4]]},
       passer_sur_option="Defense"),

    # ============================================================ ap030 Trophy Taken
    _c("ap030 Trophy Taken : le mechant actif attaque le personnage ami le plus bas (Black Cat) ; vaincu, il est RETIRE de la partie (pas sous Skulls)",
       "« attacks the friendly character with the fewest remaining hit points. If this attack defeats an ally, remove that ally from the game » ; "
       "insert : priorite sur Skulls for the Taking",
       ["Puzzle.SetActiveVillain('ap002a')", "Puzzle.PutIntoPlay('01002', under_control=True)"], ["Puzzle.Reveal('ap030')"],
       {"retires": ["01002"], "taille_pose_sous": [["ap010", 0]]},
       choisir_option="Place_2_threat_on_the_main_scheme", passer_sur_option="Defense"),

    # ============================================================ ap031 Lethal Ambush
    _c("ap031 Lethal Ambush : le 1er sbire des 7 cartes defaussees entre en jeu engage ; puis le mechant ET ce sbire attaquent (1 + 2 = 3 degats)",
       "« Put the first minion discarded this way into play engaged with you. Then, the villain and each minion engaged with you attacks you »",
       [HEROS, "Puzzle.EmptyHand()"] + deck_avec("ap018", "01098"), ["Puzzle.Reveal('ap031')"],
       {"en_jeu": ["ap018"], "degats_identite": 3},
       passer_sur_option="Defense"),

    # ============================================================ ap032 Swarm Breaker / ap033 Alien Onslaught
    _c("ap032 Swarm Breaker vaincue : 2[per_hero] degats a chaque ennemi",
       "« When Defeated: Deal 2[per_hero] damage to each enemy »",
       ["Puzzle.Reveal('ap032')"], ["Puzzle.SetThreat('ap032', 0)"],
       {"degats": [["ap001a", 2], ["ap002a", 2]]}),
    _c("ap033 Alien Onslaught : chaque joueur defausse 2[per_hero] cartes ; l'Alien Scout atteint est distribue ET compte 1 jeton d'acceleration",
       "« Place 1 acceleration token here for each [[XENOMORPH]] minion discarded this way » ; arbitrage 4 du 25/10/2026",
       ["Puzzle.CreatePlayerDeck('01090', '01089', '01088', 'ap102')"], ["Puzzle.Reveal('ap033')"],
       {"jetons": [["ap033", "acceleration_token", 1]], "scouts_distribues": 1}),
    _c("ap033 apres que le joueur contrecarre cette manigance : il defausse les 2[per_hero] cartes du dessus de son deck",
       "« Forced Response: After you thwart this scheme, discard the top 2[per_hero] cards of your deck »",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.Reveal('ap033')", "Puzzle.EmptyPlayerDiscardPile()",
        "Puzzle.CreatePlayerDeck('01090', '01089', '01088', '01087')"], ["Puzzle.Thwart('01001a')"],
       {"defausse_joueur": 2}, cibles=["ap033"]),
]
