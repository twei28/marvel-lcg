# Cas test_capacites du set DARK PROTEGE (Shadowland, sl012a/b a sl027), prefixe de nom `[sla]`.
# Scenario REEL `shadows_in_the_night` : le vilain est tire au hasard par sl001a, la cle `graine` du harnais impose le tirage.
# Graines mesurees (22/10/2026, sonde sur les 40 premieres) : voir SEMENCES. Un cas qui nomme un vilain verifie AUSSI que c'est bien lui qui est en jeu (`vilain_id`).
HEROS = "spider_man"
SEMENCES = {"sl012": 4, "sl013": 12, "sl014": 5, "sl015": 9, "sl016": 1, "sl017": 8}
FORME_HEROS = "Puzzle.ChangeForm('01001b')"
FILLER = "'01105'"        # traitrise sans icone de boost : une carte de boost qui ne change rien
# deck de rencontre neutre : 5 cartes sans icone de boost (les activations du vilain y piochent leur boost)
RIEN = ["Puzzle.EmptyEncounterDeck()", f"Puzzle.CreateEncounterDeck({', '.join([FILLER] * 5)})"]


def _deck(*cartes):
    return ["Puzzle.EmptyEncounterDeck()", f"Puzzle.CreateEncounterDeck({', '.join(repr(c) for c in cartes)})"]


def _v(vilain, nom, pourquoi, mise, declencher, attendu, face_b=False, forme_heros=True, deck=None, **cle):
    """Cas sur le vilain `vilain` (« sl012 », « sl013 »...). `face_b` retourne le vilain (verso) avant le cas ; le vilain en jeu est verifie."""
    a, b = vilain + "a", vilain + "b"
    # ⚠ Le pilote DEFEND avec le heros quand il est pret (DEF 3) : pour mesurer des degats non defendus on l'epuise, sauf quand c'est lui qui attaque.
    epuise = forme_heros and not any("Puzzle.Attack('01001a')" in d or "Puzzle.Thwart('01001a')" in d for d in declencher) and not cle.pop("heros_pret", False)
    cle.pop("heros_pret", None)
    avant = [*(deck if deck is not None else RIEN), *([FORME_HEROS] if forme_heros else []), *([f"Puzzle.Flip('{a}')"] if face_b else []), *mise, *(["Puzzle.Exhaust('01001a')"] if epuise else [])]
    attendu = dict(attendu)
    attendu.setdefault("vilain_id", b if face_b else a)
    cas = {"nom": "[sla] " + nom, "pourquoi": pourquoi, "scenario": "shadows_in_the_night", "heros": HEROS, "graine": SEMENCES[vilain], "mise_en_place": avant,
           "declencher": declencher, "verifier": "sla_etat", "attendu": attendu, "main_exclusive": cle.pop("main_exclusive", ["01088"])}
    cas.update(cle)
    return cas


def _m(nom, pourquoi, mise, declencher, attendu, vilain="sl013", deck=None, forme_heros=True, **cle):
    """Cas sur une carte LIEE ou un sbire : le vilain de fond est sans importance (Daredevil, ATK 2 : sa seule capacite se declenche quand on l'ATTAQUE)."""
    return _v(vilain, nom, pourquoi, mise, declencher, attendu, deck=deck, forme_heros=forme_heros, **cle)


def _a(vilain, face_b=False):
    return vilain + ("b" if face_b else "a")


BW = "'01075'"             # Black Widow : allie, 3 de cout imprime, 2 PV
CAS = []

# ------------------------------------------------------------------------------------------------------------------------- tirage : chacun des six vilains
for _v_id, _g in SEMENCES.items():
    CAS.append(_v(_v_id, f"{_v_id}a tirage graine {_g} : le vilain en jeu est bien {_v_id}a (face A), ses cartes liees et elles seules dans le deck de rencontre", "sl001a : « Choose 1 random villain ... shuffle each card linked to that villain »",
                  [], [], {"setup_dark_protege": True, "en_jeu": ["sl003a", "sl004a"]}, deck=[], forme_heros=False))

# ------------------------------------------------------------------------------------------------------------------------- sl012 Archpriestess
for _b in (False, True):
    _id = _a("sl012", _b)
    _t = "sl012b" if _b else "sl012a"
    CAS += [
        _v("sl012", f"{_t} Archpriestess attaque : un sbire sans Tough en recoit UN, le deck de rencontre n'est pas defausse", "« give a minion a tough status card. If no tough status card was placed this way ... »",
           ["Puzzle.PutIntoPlay('01101')"], [f"Puzzle.Attack('{_id}')"], {"statuts": [["01101", "Tough"]], "cartes_donnees": [0], "deck_rencontre": 4, "defausse_rencontre_taille": 1}, face_b=_b),
        _v("sl012", f"{_t} : tous les sbires ont deja un Tough -> rien n'est pose, defausse de 3 cartes du deck rencontre, un SBIRE defausse est donne face cachee au joueur",
           "« If no tough status card was placed this way, discard the top 3 cards of the encounter deck, then deal 1 minion discarded this way to yourself as a facedown encounter card »",
           ["Puzzle.PutIntoPlay('01102')"], [f"Puzzle.Attack('{_id}')"], {"cartes_donnees": [1], "deck_rencontre": 1, "defausse_rencontre_n": [["01101", 3]]}, face_b=_b,
           deck=_deck(*["01101"] * 5)),
        _v("sl012", f"{_t} : aucun sbire en jeu -> meme branche (defausse 3, un sbire donne face cachee)", "« give a minion a tough status card » sans sbire = aucune carte posee",
           [], [f"Puzzle.Attack('{_id}')"], {"cartes_donnees": [1], "deck_rencontre": 1, "defausse_rencontre_n": [["01101", 3]]}, face_b=_b, deck=_deck(*["01101"] * 5)),
        _v("sl012", f"{_t} : les 3 cartes defaussees ne sont pas des sbires -> rien n'est donne au joueur", "« deal 1 MINION discarded this way » : une traitrise defaussee reste defaussee",
           [], [f"Puzzle.Attack('{_id}')"], {"cartes_donnees": [0], "deck_rencontre": 1, "defausse_rencontre_n": [["01105", 4]]}, face_b=_b),
    ]
CAS.append(_v("sl012", "sl012a TEMOIN : sans sbire ET sans Tough a donner (le sbire a deja Tough) la defausse n'a pas lieu quand un Tough est vraiment pose",
              "garde-fou : un sbire Hydra sans Tough recoit le Tough, le deck garde 4 cartes (5 - la carte de boost)", ["Puzzle.PutIntoPlay('01101')", "Puzzle.PutIntoPlay('01102')"],
              ["Puzzle.Attack('sl012a')"], {"cartes_donnees": [0], "deck_rencontre": 4}, deck=RIEN, cibles=["01101"]))

# ------------------------------------------------------------------------------------------------------------------------- sl013 Daredevil
for _b in (False, True):
    _id = _a("sl013", _b)
    CAS += [
        _v("sl013", f"{_id} Daredevil attaque par le heros : le joueur choisit de defausser 1 carte au hasard de sa main", "« After you ... attacks Daredevil, choose: Either discard 1 random card from your hand ... »",
           [], ["Puzzle.Attack('01001a')"], {"defausse": ["01088"], "degats_identite": 0, "taille_main": 0}, face_b=_b, cibles=[_id], choisir_option=["Discard_1_random_card_from_your_hand"]),
        _v("sl013", f"{_id} : ou bien Daredevil l'attaque (ATQ 2 + 1 de position = 3, aucune carte defaussee)", "« ... or Daredevil attacks you »",
           [], ["Puzzle.Attack('01001a')"], {"degats_identite": 3, "en_main": ["01088"]}, face_b=_b, cibles=[_id], choisir_option=["Daredevil_attacks_you"]),
    ]
CAS += [
    _v("sl013", "sl013a, TEMOIN D'EPUISEMENT : deux attaques du heros dans le meme round, la 2e ne declenche rien (3 degats au total et non 6)", "« (Limit once per round per player.) »",
       [], ["Puzzle.Attack('01001a')", "Puzzle.Attack('01001a')"], {"degats_identite": 3}, cibles=["sl013a"], choisir_option=["Daredevil_attacks_you"]),
    _v("sl013", "sl013a : la main est VIDE -> la branche « defausser » n'est pas offerte, Daredevil attaque", "un choix sans effet ne se choisit pas",
       ["Puzzle.EmptyHand()"], ["Puzzle.Attack('01001a')"], {"degats_identite": 3}, cibles=["sl013a"], main_exclusive=None),
    _v("sl013", "sl013a : l'attaque d'un ALLIE du joueur (Black Widow) declenche aussi la reponse", "« After you OR AN ALLY you control attacks Daredevil »",
       ["Puzzle.PutIntoPlay('01075', under_control=True)"], ["Puzzle.Attack('01075')"], {"degats_identite": 3}, cibles=["sl013a"], choisir_option=["Daredevil_attacks_you"]),
    _v("sl013", "sl013a, TEMOIN : sans attaque contre lui, Daredevil ne fait rien", "la reponse ne part que sur une attaque contre Daredevil",
       [], ["Puzzle.Damage('sl013a', 1)"], {"degats_identite": 0, "en_main": ["01088"]}),
]

# ------------------------------------------------------------------------------------------------------------------------- sl014 Elektra
for _b in (False, True):
    _id = _a("sl014", _b)
    _t3 = ["'01075'"] * 3
    CAS += [
        _v("sl014", f"{_id} Elektra attaque : la carte du dessus de son deck (cout imprime IMPAIR : Black Widow, 3) est defaussee et Elektra gagne +1 ATK (2 + 1 de position + 1 = 4 degats)", "« If that card's printed cost is an odd number, Elektra gets +1 ATK for this attack »",
           ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01075', '01075', '01075')"], [f"Puzzle.Attack('{_id}')"], {"degats_identite": 4, "defausse": ["01075"]}, face_b=_b),
        _v("sl014", f"{_id} : cout PAIR (Falcon, 4) -> pas de +1 ATK, l'attaque gagne PIERCING : elle defausse le Tough du heros et inflige ses 3 degats (2 + 1 de position)", "« otherwise, this attack gains overkill and piercing »",
           ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('03011', '03011', '03011')", "Puzzle.Tough('01001a')"], [f"Puzzle.Attack('{_id}')"], {"degats_identite": 3, "statuts_absents": [["01001a", "Tough"]], "defausse": ["03011"]}, face_b=_b),
        _v("sl014", f"{_id} : cout PAIR -> OVERKILL : Black Widow (2 PV) defend, l'exces (2 + 1 de position + 1 de boost - 2 PV = 2) passe au heros", "« this attack gains overkill »",
           ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('03011', '03011', '03011')", "Puzzle.PutIntoPlay('01075', under_control=True)"], [f"Puzzle.Attack('{_id}', defender='01075')"],
           {"degats_identite": 2, "hors_jeu": ["01075"]}, face_b=_b, deck=_deck("01101", "01101", "01101", "01101", "01101")),
    ]
CAS += [
    _v("sl014", "sl014a : une carte SANS cout imprime (Energy) n'est pas impaire -> piercing (le Tough du heros saute)", "« printed cost » : une ressource n'a pas de cout",
       ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01088', '01088', '01088')", "Puzzle.Tough('01001a')"], ["Puzzle.Attack('sl014a')"], {"degats_identite": 3, "statuts_absents": [["01001a", "Tough"]]}),
    _v("sl014", "sl014a, TEMOIN : cout IMPAIR -> pas de piercing : le Tough du heros absorbe l'attaque (+1 ATK ne change rien, 0 degat, Tough defausse)", "le piercing ne vient que de la branche « otherwise »",
       ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01075', '01075', '01075')", "Puzzle.Tough('01001a')"], ["Puzzle.Attack('sl014a')"], {"degats_identite": 0, "statuts_absents": [["01001a", "Tough"]]}),
]

# ------------------------------------------------------------------------------------------------------------------------- sl015 Gorgon
for _b in (False, True):
    _id = _a("sl015", _b)
    CAS += [
        _v("sl015", f"{_id} Gorgon attaque, branche 1 : le joueur depense une ressource physique (Strength), pas d'etourdissement ni de degats indirects (3 degats d'attaque)", "« Spend a [physical] resource »",
           [], [f"Puzzle.Attack('{_id}')"], {"degats_identite": 3, "defausse": ["01090"], "statuts_absents": [["01001a", "Stunned"]]}, face_b=_b, preferer_option=["Spend_a_[physical]_resource"], payer_avec=["01090"], main_exclusive=["01090"]),
        _v("sl015", f"{_id} branche 2 : l'identite est etourdie", "« Stun your identity »",
           [], [f"Puzzle.Attack('{_id}')"], {"statuts": [["01001a", "Stunned"]], "en_main": ["01088"]}, face_b=_b, preferer_option=["Stun_your_identity"]),
        _v("sl015", f"{_id} branche 3 : 2 degats indirects en plus de l'attaque (3 + 2 = 5)", "« Take 2 indirect damage »",
           [], [f"Puzzle.Attack('{_id}')"], {"degats_identite": 5, "statuts_absents": [["01001a", "Stunned"]]}, face_b=_b, preferer_option=["Take_2_indirect_damage"]),
    ]
CAS += [
    _v("sl015", "sl015a : aucune ressource physique en main (Genius = mentale) -> la branche payante n'est PAS offerte, le pilote retombe sur « Stun your identity »", "le moteur reduirait un choix payant impayable au plus gros morceau payable : on ne l'offre que si payable",
       [], ["Puzzle.Attack('sl015a')"], {"statuts": [["01001a", "Stunned"]], "en_main": ["01089"]}, preferer_option=["Spend_a_[physical]_resource"], main_exclusive=["01089"]),
]

# ------------------------------------------------------------------------------------------------------------------------- sl016 Lady Bullseye
for _b in (False, True):
    _id = _a("sl016", _b)
    _atq = 2 if _b else 1
    CAS += [
        _v("sl016", f"{_id} Lady Bullseye attaque SANS defenseur : 1 degat indirect en plus de l'attaque ({_atq} + 1 de position + 1), pas de menace sur le complot", "« if that attack was undefended, take 1 indirect damage »",
           [], [f"Puzzle.Attack('{_id}')"], {"degats_identite": _atq + 2, "menace": [["sl001b", 2]]}, face_b=_b),
        _v("sl016", f"{_id} : attaque DEFENDUE par un allie (Black Widow) : 1 menace sur le complot principal, aucun degat indirect (le heros ne subit rien)", "« otherwise, place 1 threat on the main scheme »",
           ["Puzzle.PutIntoPlay('01075', under_control=True)"], [f"Puzzle.Attack('{_id}', defender='01075')"], {"degats_identite": 0, "menace": [["sl001b", 3]]}, face_b=_b),
    ]

# ------------------------------------------------------------------------------------------------------------------------- sl017 White Tiger
CAS += [
    _v("sl017", "sl017a White Tiger attaque : elle ATTAQUE DE NOUVEAU avec +1 ATK (1 puis 0 + 1 + 1 = 2 : 3 degats au total)", "« After White Tiger attacks you, she attacks you again with +1 ATK »",
       [], ["Puzzle.Attack('sl017a')"], {"degats_identite": 3}),
    _v("sl017", "sl017a, TEMOIN D'EPUISEMENT : deux attaques dans le meme round, la seconde ne declenche pas de 2e attaque (4 degats au total : 1 + 2, puis 1 ; et non 6)", "« (Limit once per round per player.) »",
       [], ["Puzzle.Attack('sl017a')", "Puzzle.Attack('sl017a')"], {"degats_identite": 4}),
    _v("sl017", "sl017b White Tiger (verso) : elle attaque de nouveau SANS bonus (2 + 2 = 4 degats)", "« she attacks you again » (sans « with +1 ATK » au verso)",
       [], ["Puzzle.Attack('sl017b')"], {"degats_identite": 4}, face_b=True),
    _v("sl017", "sl017b, TEMOIN D'EPUISEMENT : deux attaques dans le meme round, une seule attaque supplementaire (6 degats : 2+2 puis 2)", "limite partagee par round",
       [], ["Puzzle.Attack('sl017b')", "Puzzle.Attack('sl017b')"], {"degats_identite": 6}, face_b=True),
]

# ------------------------------------------------------------------------------------------------------------------------- sl018 Art of the Kill
CAS += [
    _m("sl018 Art of the Kill revelee : s'attache a l'identite du joueur", "« Attach to your identity »", [], ["Puzzle.Reveal('sl018')"], {"hotes": [["sl018", "01001a"]]}),
    _m("sl018 : un ennemi (Hydra Mercenary, ATQ 1) qui attaque le porteur gagne +1 ATK : 3 degats (1 + 1 de position + 1)", "« When an enemy attacks you, it gets +1 ATK for that attack »",
       ["Puzzle.Reveal('sl018')", "Puzzle.PutIntoPlay('01101')"], ["Puzzle.Attack('01101')"], {"degats_identite": 3}),
    _m("sl018 TEMOIN : sans la carte, la meme attaque inflige 2 degats (1 + 1 de position)", "la carte seule ajoute le +1", ["Puzzle.PutIntoPlay('01101')"], ["Puzzle.Attack('01101')"], {"degats_identite": 2}),
    _m("sl018 : si l'attaque VAINC un personnage (Black Widow, 2 PV, defend contre ATQ 1 + 1) : 1 menace sur le complot principal", "« If that attack defeats a character, place 1 threat on the main scheme »",
       ["Puzzle.Reveal('sl018')", "Puzzle.PutIntoPlay('01101')", "Puzzle.PutIntoPlay('01075', under_control=True)"], ["Puzzle.Attack('01101', defender='01075')"], {"menace": [["sl001b", 3]], "hors_jeu": ["01075"]}),
    _m("sl018, TEMOIN : l'allie survit (3 degats sur 5 PV : U.S. Agent) -> aucune menace posee", "la menace n'est posee que si un personnage est vaincu",
       ["Puzzle.Reveal('sl018')", "Puzzle.PutIntoPlay('01101')", "Puzzle.PutIntoPlay('04014', under_control=True)"], ["Puzzle.Attack('01101', defender='04014')"], {"menace": [["sl001b", 2]], "en_jeu": ["04014"]}),
    _m("sl018 Alter-Ego Action : depenser [energy][mental][physical] (Energy + Genius + Strength) -> la carte est defaussee", "« Spend [energy] [mental] [physical] resources -> discard this card »",
       ["Puzzle.Reveal('sl018')", "Puzzle.EmptyHand()", "Puzzle.CreateHandCards('01088', '01089', '01090', '01088', '01089', '01090')"], ["Puzzle.Action('sl018', 'AlterEgoAction')"], {"hors_jeu": ["sl018"]}, forme_heros=False, payer_avec=["01088", "01089", "01090"], deck=RIEN, main_exclusive=None, surpayer=True),
]

# ------------------------------------------------------------------------------------------------------------------------- sl019 Krahllak's Blessing
CAS += [
    _v("sl012", "sl019 Krahllak's Blessing revelee : s'attache au VILAIN", "« Attach to the villain »", [], ["Puzzle.Reveal('sl019')"], {"hotes": [["sl019", "sl012a"]]}),
    _v("sl012", "sl019 : le heros attaque le vilain (2 + 1 de position = 3 degats) : reduits de 3 -> 0 degat, le vilain ATTAQUE le heros (ATQ 1 + 1 de position = 2), la carte est defaussee", "« reduce that amount by 3. Attached villain attacks that character. Discard this card »",
       ["Puzzle.Reveal('sl019')"], ["Puzzle.Attack('01001a')"], {"degats": [["sl012a", 0]], "degats_identite": 2, "hors_jeu": ["sl019"]}, cibles=["sl012a"], deck=_deck(*["01105"] * 9)),
    _v("sl012", "sl019 : un ALLIE (U.S. Agent) attaque le vilain : 0 degat (1 de Riposte de l'allie : le vilain lui a inflige 1), le vilain attaque l'ALLIE (2 degats + 1 que le moteur inflige deja a un allie qui attaque le vilain, mesure sans la carte : 3), le heros n'est pas touche", "« attacks THAT character »",
       ["Puzzle.PutIntoPlay('04014', under_control=True)", "Puzzle.Reveal('sl019')"], ["Puzzle.Attack('04014')"], {"degats": [["sl012a", 1], ["04014", 3]], "degats_identite": 0, "hors_jeu": ["sl019"]}, cibles=["sl012a"], deck=_deck(*["01105"] * 9)),
    _v("sl012", "sl019 TEMOIN : sans la carte le vilain subit les 3 degats et n'attaque pas", "la carte seule reduit et contre-attaque",
       [], ["Puzzle.Attack('01001a')"], {"degats": [["sl012a", 3]], "degats_identite": 0}, cibles=["sl012a"]),
    _v("sl012", "sl019 : une attaque de 5 degats (heros + 3 de bonus) n'en inflige que 2 : la reduction est de 3 exactement, pas totale", "« reduce that amount by 3 »",
       ["Puzzle.Reveal('sl019')", "Puzzle.PutIntoPlay('01101')"], ["Puzzle.Attack('01001a')"], {"degats": [["sl012a", 0]]}, cibles=["sl012a"], deck=_deck(*["01105"] * 9)),
]

# ------------------------------------------------------------------------------------------------------------------------- sl020 Archpriestess (sbire)
CAS += [
    _m("sl020 Archpriestess (sbire) revelee, un autre sbire engage (Hydra Mercenary, ATQ 1) : il attaque le joueur (1 + 1 de position = 2 degats), RIEN n'est defausse", "« Each other minion engaged with you attacks you. If no attack was made this way, discard the top 3 cards ... »",
       ["Puzzle.PutIntoPlay('01101')"], ["Puzzle.Reveal('sl020')"], {"degats_identite": 2, "deck_rencontre": 5}, deck=RIEN),
    _m("sl020 : DEUX autres sbires engages : les deux attaquent (2 + 3 = 5 degats)", "« EACH other minion »",
       ["Puzzle.PutIntoPlay('01101')", "Puzzle.PutIntoPlay('01103')"], ["Puzzle.Reveal('sl020')"], {"degats_identite": 5, "deck_rencontre": 5}, deck=RIEN),
    _m("sl020 : aucun autre sbire engage -> aucune attaque : defausse des 3 premieres cartes du deck rencontre", "« If no attack was made this way, discard the top 3 cards of the encounter deck »",
       [], ["Puzzle.Reveal('sl020')"], {"degats_identite": 0, "deck_rencontre": 2}, deck=RIEN),
    _m("sl020 : le seul autre sbire est ETOURDI (il ne peut pas attaquer) -> aucune attaque n'est faite : defausse de 3 cartes", "le sbire etourdi retire son statut au lieu d'attaquer",
       ["Puzzle.PutIntoPlay('01101')", "Puzzle.Stun('01101')"], ["Puzzle.Reveal('sl020')"], {"degats_identite": 0, "deck_rencontre": 2}, deck=RIEN),
]

# ------------------------------------------------------------------------------------------------------------------------- sl021 Gorgon (sbire)
CAS += [
    _m("sl021 Gorgon (sbire) engage : le heros l'attaque et lui inflige des degats -> le heros est ETOURDI", "« After a character attacks and damages Gorgon, stun that character »",
       ["Puzzle.PutIntoPlay('sl021')"], ["Puzzle.Attack('01001a')"], {"degats": [["sl021", 3]], "statuts": [["01001a", "Stunned"]]}, cibles=["sl021"]),
    _m("sl021 : un ALLIE qui l'attaque (Black Widow) est etourdi, pas le heros", "« that character » = l'attaquant",
       ["Puzzle.PutIntoPlay('sl021')", "Puzzle.PutIntoPlay('01075', under_control=True)"], ["Puzzle.Attack('01075')"], {"statuts": [["01075", "Stunned"]], "statuts_absents": [["01001a", "Stunned"]]}, cibles=["sl021"]),
    _m("sl021 TEMOIN : une attaque ABSORBEE (Gorgon a un Tough) n'inflige aucun degat : personne n'est etourdi", "« attacks AND DAMAGES »",
       ["Puzzle.PutIntoPlay('sl021')", "Puzzle.Tough('sl021')"], ["Puzzle.Attack('01001a')"], {"degats": [["sl021", 0]], "statuts_absents": [["01001a", "Stunned"]]}, cibles=["sl021"]),
]

# ------------------------------------------------------------------------------------------------------------------------- sl022 Lady Bullseye (sbire)
CAS += [
    _m("sl022 Lady Bullseye (sbire) attaque le joueur qui controle un allie : elle attaque L'ALLIE (Falcon, 1 + 1 = 2 degats), le heros n'est pas touche", "« she attacks the ally with the highest printed cost you control »",
       ["Puzzle.PutIntoPlay('sl022')", "Puzzle.PutIntoPlay('03011', under_control=True)"], ["Puzzle.Attack('sl022')"], {"degats": [["03011", 2]], "degats_identite": 0}, deck=RIEN),
    _m("sl022 : deux allies -> l'allie au cout imprime le PLUS ELEVE (Falcon, 4, contre Black Widow, 3)", "« highest printed cost »",
       ["Puzzle.PutIntoPlay('sl022')", "Puzzle.PutIntoPlay('01075', under_control=True)", "Puzzle.PutIntoPlay('03011', under_control=True)", "Puzzle.Exhaust('01075')", "Puzzle.Exhaust('03011')"], ["Puzzle.Attack('sl022')"],
       {"degats": [["03011", 2], ["01075", 0]], "degats_identite": 0}, deck=RIEN),
    _m("sl022 : aucun allie -> l'attaque reste sur l'identite (2 degats)", "« if able »",
       ["Puzzle.PutIntoPlay('sl022')"], ["Puzzle.Attack('sl022')"], {"degats_identite": 2}, deck=RIEN),
    _m("sl022 : l'attaque gagne RANGED : U.S. Agent (Riposte 1) ne la riposte pas, Lady Bullseye ne subit aucun degat", "« this attack gains ranged » (ranged ignore Retaliate)",
       ["Puzzle.PutIntoPlay('sl022')", "Puzzle.PutIntoPlay('04014', under_control=True)"], ["Puzzle.Attack('sl022')"], {"degats": [["04014", 2], ["sl022", 0]]}, deck=RIEN),
]

# ------------------------------------------------------------------------------------------------------------------------- sl023 White Tiger (sbire)
CAS += [
    _m("sl023 White Tiger (sbire) revelee : 2 degats indirects au joueur", "« When Revealed: Take 2 indirect damage »", [], ["Puzzle.Reveal('sl023')"], {"degats_identite": 2}),
]

# ------------------------------------------------------------------------------------------------------------------------- sl024 Rite of Offering
CAS += [
    _m("sl024 Rite of Offering vaincue : le joueur qui l'a vaincue retire UN allie qu'il controle DE LA PARTIE (Black Widow, ni defaussee ni en jeu)", "« removes an ally they control from the game »",
       ["Puzzle.PutIntoPlay('sl024')", "Puzzle.SetThreat('sl024', 1)", "Puzzle.PutIntoPlay('01075', under_control=True)"], ["Puzzle.Thwart('01001a')"], {"hors_jeu": ["sl024", "01075"], "degats_identite": 0}, cibles=["sl024"]),
    _m("sl024 : AUCUN allie -> le joueur subit 3 degats", "« If no ally was removed this way, that player takes 3 damage »",
       ["Puzzle.PutIntoPlay('sl024')", "Puzzle.SetThreat('sl024', 1)"], ["Puzzle.Thwart('01001a')"], {"hors_jeu": ["sl024"], "degats_identite": 3}, cibles=["sl024"]),
    _m("sl024, TEMOIN : tant qu'elle n'est pas vaincue (menace 3), rien ne se passe", "la reponse ne part que a la defaite",
       ["Puzzle.PutIntoPlay('sl024')", "Puzzle.SetThreat('sl024', 3)", "Puzzle.PutIntoPlay('01075', under_control=True)"], ["Puzzle.Thwart('01001a')"], {"en_jeu": ["sl024", "01075"], "degats_identite": 0}, cibles=["sl024"]),
]

# ------------------------------------------------------------------------------------------------------------------------- sl025 Shadowy Plot
CAS += [
    _m("sl025 Shadowy Plot vaincue : le joueur regarde les 3 cartes du dessus du deck rencontre, en REVELE une (un sbire : il entre en jeu) et defausse les 2 autres", "« looks at the top 3 cards of the encounter deck, reveals 1 of them, and discards the rest »",
       ["Puzzle.PutIntoPlay('sl025')", "Puzzle.SetThreat('sl025', 1)"], ["Puzzle.Thwart('01001a')"], {"en_jeu": ["01101"], "defausse_rencontre_n": [["01101", 2]], "deck_rencontre": 2}, cibles=["sl025"], deck=_deck(*["01101"] * 5)),
    _m("sl025 : la carte revelee est choisie PARMI les 3 (une traitrise sans effet pour Spider-Man et deux sbires : le pilote prend la premiere, les deux autres vont en defausse)", "« reveals 1 of them »",
       ["Puzzle.PutIntoPlay('sl025')", "Puzzle.SetThreat('sl025', 1)"], ["Puzzle.Thwart('01001a')"], {"defausse_rencontre_taille": 3, "deck_rencontre": 1}, cibles=["sl025"], deck=_deck("01101", "01101", "01101", "01105")),
]

# ------------------------------------------------------------------------------------------------------------------------- sl026 Darkness Within
CAS += [
    _m("sl026 Darkness Within revelee en ALTER-EGO : le joueur passe en forme HEROS, le vilain (Daredevil, ATQ 2) l'attaque : 2 degats", "« Change to hero form. The villain attacks you »",
       [], ["Puzzle.Reveal('sl026')"], {"forme": "Hero", "exhausted": ["01001a"]}, forme_heros=False),
    _m("sl026 revelee en forme HEROS : le joueur reste heros, le vilain l'attaque", "« Change to hero form » sans effet si deja heros",
       [], ["Puzzle.Reveal('sl026')"], {"forme": "Hero", "degats_identite": 3}),
    _m("sl026 en BOOST d'une attaque du vilain : l'attaque gagne OVERKILL (Black Widow, 2 PV, defend ATQ 2 + 1 icone de boost : 2 degats d'exces au heros : 2 + 1 de position + 1 - 2)", "« [star] Boost: If this activation is an attack, it gains overkill »",
       ["Puzzle.PutIntoPlay('01075', under_control=True)", "Puzzle._DeclareDefender('01075')"], ["Puzzle.Boost('sl026')"], {"degats_identite": 2, "hors_jeu": ["01075"]}),
]

# ------------------------------------------------------------------------------------------------------------------------- sl027 Embraced by Darkness
CAS += [
    _m("sl027 Embraced by Darkness revelee : le vilain MANIGANCE (SCH 1 -> 1 menace, <= 2) donc defausse des 3 premieres cartes du deck rencontre", "« The villain schemes. If 2 or less threat was placed on the main scheme this way, discard the top 3 cards »",
       [], ["Puzzle.Reveal('sl027')"], {"menace": [["sl001b", 3]], "deck_rencontre": 1}, deck=RIEN),
    _m("sl027 : la manigance pose PLUS de 2 menaces (SCH 1 + 2 icones de boost = 3) -> rien n'est defausse", "« 2 OR LESS »",
       [], ["Puzzle.Reveal('sl027')"], {"menace": [["sl001b", 5]], "deck_rencontre": 4}, deck=_deck(*["01107"] * 5)),
    _m("sl027 en BOOST d'une ATTAQUE : 2 menaces sur le complot principal", "« [star] Boost: If this activation is an attack, place 2 threat on the main scheme »",
       [], ["Puzzle.Boost('sl027')"], {"menace": [["sl001b", 4]]}),
]

import os as _os
if _os.environ.get("SLA_SONDE"):
    import copy as _copy
    _cas = [c for c in CAS if c["nom"].startswith("[sla] " + _os.environ["SLA_SONDE"])]
    CAS = []
    for _c in _cas:
        _c = _copy.deepcopy(_c); _c["nom"] = "[slaS] " + _c["nom"][6:]; _c["verifier"] = "sla_sonde"; CAS.append(_c)

VERIFICATIONS = r'''
def sla_sonde(monde, aides):
    lignes = []
    for obj in monde.object_manager.card_dict.values():
        f = getattr(obj, "face", None)
        if f is not None and f.IsInPlay():
            try:
                lignes.append(f"{f.paper.card_id}:{f.max_health - f.health}/{f.max_health}")
            except Exception:
                lignes.append(f"{f.paper.card_id}")
    main = [str(f.paper.card_id) for f in monde.players[0].hand_cards.GetAll()]
    disc = [str(f.paper.card_id) for f in monde.players[0].discard_pile.Get()]
    return False, "EN JEU " + " ".join(lignes) + " MAIN " + " ".join(main) + " DEFAUSSE " + " ".join(disc)

def sla_etat(monde, aides):
    """sl_etat (shadowland.py) + `vilain_id` (la FACE du vilain en jeu), `deck_rencontre` (taille du deck de rencontre du vilain), `defausse_rencontre_taille`, `defausse_rencontre_n` [[card_id, n]]."""
    from game.operate.worlds import Worlds as _W
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    soucis = []
    propres = ("vilain_id", "deck_rencontre", "defausse_rencontre_taille", "defausse_rencontre_n")
    if "vilain_id" in attendu:
        ids = [str(v.paper.card_id) for v in _W.GetAllVillains(monde)]
        if ids != [attendu["vilain_id"]]:
            soucis.append(f"vilain en jeu {ids} (attendu {attendu['vilain_id']})")
    if "deck_rencontre" in attendu:
        n = len(list(_W.GetEncounterDeckCards(monde)))
        if n != attendu["deck_rencontre"]:
            soucis.append(f"deck de rencontre = {n} carte(s) (attendu {attendu['deck_rencontre']})")
    if "defausse_rencontre_taille" in attendu or "defausse_rencontre_n" in attendu:
        cartes = [str(getattr(f.paper, "card_id", None)) for f in _W.GetEncounterDiscardPileCards(monde)]
        if "defausse_rencontre_taille" in attendu and len(cartes) != attendu["defausse_rencontre_taille"]:
            soucis.append(f"defausse de rencontre = {len(cartes)} carte(s) {cartes} (attendu {attendu['defausse_rencontre_taille']})")
        for card_id, n in attendu.get("defausse_rencontre_n") or []:
            if cartes.count(card_id) != n:
                soucis.append(f"{card_id} x{cartes.count(card_id)} dans la defausse de rencontre {cartes} (attendu {n})")
    reste = {k: v for k, v in attendu.items() if k not in propres}
    cas["attendu"] = reste
    try:
        ok, msg = sl_etat(monde, aides)
    finally:
        cas["attendu"] = attendu
    if not ok:
        soucis.append(msg)
    return (False, " ; ".join(soucis)) if soucis else (True, "etat conforme")
'''
