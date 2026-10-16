# Cas test_capacites du pack d'aspect TMNT JUSTICE (Inkwire, prefixe `uj`, pack `tmnt_aspect_justice`).
# Filtre : `[uj]`. Gabarits PROCESSUS-CARTE : .planning/tmnt/aspects-justice-gabarits.md.
#
# Deux familles :
#  - les RESKINS (scan IDENTIQUE a une officielle, `ability_link`, aucun script) : un cas sur la carte
#    TMNT et un TEMOIN identique sur l'officielle, meme chiffre attendu (RECETTES-MOTEUR §11) ;
#  - les cartes MODIFIEES ou NOUVELLES, scriptees dans src/cards/pack/tmnt_aspect_justice/.
#
# Conventions (reprises de tools/cas/rampage.py) :
#  - Spider-Man (01001) demarre en ALTER EGO ; HEROS le met en forme heros (01001a) ;
#  - `main_exclusive` : la main ne contient QUE la carte jouee et de quoi payer
#    (01088 Energy = [energy], 01089 Genius = [mental], 01090 Strength = [physical], 01087 = [wild]) ;
#  - Rhino 01094 (14 PV), sa manigance principale 01097b, ses manigances annexes 01107 / 01108 ;
#  - 01101 Hydra Mercenary (3 PV) est le sbire de mesure.
SC = "rhino"
HEROS = "Puzzle.ChangeForm('01001b')"
SANS_DECK = "Puzzle.EmptyPlayerDeck()"
DECK6 = "Puzzle.CreatePlayerDeck('01089', '01089', '01089', '01089', '01089', '01089')"


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    # La main de depart est VIDEE juste apres le changement de forme : sinon le pilote, qui accepte la premiere
    # option jouable, y joue des Interruptions pendant la mise en place (constate : `Puzzle.SetThreat` sur
    # 01097b ouvrait une fenetre ou une carte de la main de Spider-Man ramenait la menace a 0).
    mise = list(mise)
    rang = 1 if mise and mise[0].startswith("Puzzle.ChangeForm") else 0
    if cle.pop("garder_main", False) is False:
        mise.insert(rang, "Puzzle.EmptyHand()")
    cas = {"nom": "[uj] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": mise, "declencher": list(declencher),
           "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.update(cle)
    return cas


def _paire(tmnt, officielle, libelle, pourquoi, mise, declencher, attendu, **cle):
    """Un cas sur le reskin TMNT + le TEMOIN identique sur l'officielle (chaque card_id est remplace
    partout : mise en place, declencheurs, attendu, main, jouer, cibles)."""
    import json

    def sub(obj, de, vers):
        return json.loads(json.dumps(obj).replace(de, vers))

    cas_tmnt = _c(f"{tmnt} {libelle} (reskin de {officielle})", pourquoi, mise, declencher, attendu, **dict(cle))
    temoin = _c(f"{tmnt} TEMOIN {officielle} (officielle) : {libelle}",
                "le reskin doit rendre EXACTEMENT le meme chiffre que l'original",
                sub(mise, tmnt, officielle), sub(declencher, tmnt, officielle), sub(attendu, tmnt, officielle),
                **sub(dict(cle), tmnt, officielle))
    return [cas_tmnt, temoin]


CAS = []

# ================================================================== RESKINS (ability_link)
CAS += _paire(
    "uj001", "58016", "Battlefield Benevolence : soigne 2 degats de Rhino puis le desoriente",
    "« Heal 2 damage from an enemy → confuse that enemy » : Rhino a 3 degats -> 1, statut Confused",
    [HEROS, "Puzzle.Damage('01094', 3)"], [],
    {"degats": [["01094", 1]], "statuts": [["01094", "Confused"]], "defausse": ["uj001"]},
    main_exclusive=["uj001", "01090"], jouer=["uj001"], cibles=["01094"])
CAS += _paire(
    "uj003", "04049", "Clear the Area : retire 2 menaces et pioche 1 (derniere menace retiree)",
    "« Remove 2 threat ... If this removes the last threat on that scheme, draw 1 card » : 2 -> 0, main 0 -> 1",
    [HEROS, "Puzzle.SetThreat('01097b', 2)"], [],
    {"menace": [["01097b", 0]], "taille_main": 1, "defausse": ["uj003"]},
    main_exclusive=["uj003", "01089"], jouer=["uj003"], cibles=["01097b"])
CAS += _paire(
    "uj007", "47013", "Disguise : Action, incliner Disguise et l'identite -> 2 menaces retirees",
    "« Exhaust Disguise and your identity → remove 2 threat from a scheme » : 5 -> 3, les deux inclines",
    [HEROS, "Puzzle.PutIntoPlay('uj007', under_control=True)", "Puzzle.SetThreat('01097b', 5)"],
    ["Puzzle.Action('uj007')"],
    {"menace": [["01097b", 3]], "exhausted": ["uj007", "01001a"]},
    cibles=["01097b"])
CAS += _paire(
    "uj010", "41017", "Float Like a Butterfly : +1 degat a une attaque contre un ennemi desoriente",
    "« When a character you control attacks a confused enemy, increase the amount of damage ... by 1 » : "
    "Spider-Man ATK 2 -> 3 degats sur Rhino desoriente",
    [HEROS, "Puzzle.PutIntoPlay('uj010', under_control=True)", "Puzzle.Confuse('01094')"],
    ["Puzzle.Attack('01001a')"],
    {"degats": [["01094", 3]]}, cibles=["01094"], accepter_choix=True)
CAS += _paire(
    "uj011", "01060", "For Justice! paye en [mental] : 4 menaces retirees au lieu de 3",
    "« Remove 3 threat (4 threat instead if you paid for this card using a [mental] resource) » : 6 -> 2",
    [HEROS, "Puzzle.SetThreat('01097b', 6)"], [],
    {"menace": [["01097b", 2]]},
    main_exclusive=["uj011", "01089"], jouer=["uj011"], cibles=["01097b"])
CAS += _paire(
    "uj011", "01060", "For Justice! paye SANS [mental] : 3 menaces seulement",
    "contre-cas de la parenthese : paye en [physical], 6 -> 3",
    [HEROS, "Puzzle.SetThreat('01097b', 6)"], [],
    {"menace": [["01097b", 3]]},
    main_exclusive=["uj011", "01090"], jouer=["uj011"], cibles=["01097b"])
CAS += _paire(
    "uj013", "58021", "Heroic Conditioning : +3 PV au joueur, +1 THW au heros",
    "« You get +3 hit points and your hero gets +1 THW »",
    [HEROS, "Puzzle.PutIntoPlay('uj013', under_control=True)"], [],
    {"attributs": {"health": 3, "thwart": 1}})
CAS += _paire(
    "uj014", "01065", "Heroic Intuition : +1 THW au heros",
    "« Your hero gets +1 THW »",
    [HEROS, "Puzzle.PutIntoPlay('uj014', under_control=True)"], [],
    {"attributs": {"thwart": 1}})
CAS += _paire(
    "uj015", "61036", "Innate Perception : +1 THW au heros",
    "« Your hero gets +1 THW » (le mot-cle Starting est porte par le meme module : voir le gabarit)",
    [HEROS, "Puzzle.PutIntoPlay('uj015', under_control=True)"], [],
    {"attributs": {"thwart": 1}})
CAS += _paire(
    "uj017", "60023", "Know Your Enemy : retire 1 menace, puis 1 menace (deux choix)",
    "« Remove 1 threat from a scheme. Remove 1 threat from a scheme. » : 5 -> 3",
    [HEROS, "Puzzle.SetThreat('01097b', 5)"], [],
    {"menace": [["01097b", 3]], "defausse": ["uj017"]},
    main_exclusive=["uj017", "01089"], jouer=["uj017"], cibles=["01097b"])
CAS += _paire(
    "uj017", "60023", "Know Your Enemy : Discount 1 (MARTIAL ARTIST controle) -> jouable SANS ressource",
    "« [star] Discount 1 (Martial Artist) » : Daredevil 60039 (MARTIAL ARTIST) en jeu, la main ne contient que "
    "la carte (cout 1 -> 0) ; elle est jouee et resout",
    [HEROS, "Puzzle.PutIntoPlay('60039', under_control=True)", "Puzzle.SetThreat('01097b', 5)"], [],
    {"menace": [["01097b", 3]], "defausse": ["uj017"]},
    main_exclusive=["uj017"], jouer=["uj017"], cibles=["01097b"])
CAS += _paire(
    "uj022", "60027", "Move in Shadow : jouee, sa propre Reponse retire 1 menace",
    "« After you play a card (including this one), remove 1 threat from a scheme » : 5 -> 4",
    [HEROS, "Puzzle.SetThreat('01097b', 5)"], [],
    {"menace": [["01097b", 4]], "en_jeu": ["uj022"]},
    main_exclusive=["uj022", "01088"], jouer=["uj022"], cibles=["01097b"])
CAS += _paire(
    "uj023", "08011", "Night-Blade : entre en jeu -> va chercher une carte PREPARATION dans le deck",
    "« search your deck and discard pile for a Preparation card and add it to your hand » : 08018 Spycraft "
    "(PREPARATION) au fond d'un deck de Genius",
    [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01089', '01089', '08018', '01089')"], [],
    {"en_main": ["08018"], "en_jeu": ["uj023"]},
    main_exclusive=["uj023", "01089", "01088"], jouer=["uj023"], accepter_choix=True)
CAS += _paire(
    "uj024", "22015", "One Way or Another : revele une manigance annexe du deck rencontre -> pioche 3",
    "« Search the encounter deck for a side scheme. Reveal that side scheme → draw 3 cards » : 01107 en jeu, main 3",
    [HEROS, "Puzzle.CreateEncounterDeck('01104', '01107', '01104')"], [],
    {"en_jeu": ["01107"], "taille_main": 3, "defausse": ["uj024"]},
    main_exclusive=["uj024"], jouer=["uj024"], accepter_choix=True)
CAS += _paire(
    "uj025", "30019", "Overwatch : 1 menace contree sur la manigance principale -> 1 retiree d'une AUTRE manigance",
    "« When any amount of threat is removed from attached scheme by a thwart, discard this card → remove an equal "
    "amount of threat from a different scheme » : Spider-Man THW 1 sur 01097b, 01107 3 -> 2, Overwatch defaussee",
    [HEROS, "Puzzle.Reveal('01107')", "Puzzle.SetThreat('01107', 3)", "Puzzle.SetThreat('01097b', 5)",
     "Puzzle.PutIntoPlay('uj025', under_control=True)", "Puzzle.Attach('uj025', '01097b')"],
    ["Puzzle.Thwart('01001a')"],
    {"menace": [["01097b", 4], ["01107", 2]], "hors_jeu": ["uj025"]},
    cibles=["01097b", "01107"], accepter_choix=True)
CAS += _paire(
    "uj029", "04047", "Skilled Investigator : manigance annexe vaincue -> incliner -> piocher 1",
    "« After a side scheme is defeated, exhaust Skilled Investigator → draw 1 card » : 01107 a 1 menace, contree",
    [HEROS, "Puzzle.PutIntoPlay('uj029', under_control=True)", "Puzzle.Reveal('01107')",
     "Puzzle.SetThreat('01107', 1)", "Puzzle.EmptyHand()"],
    ["Puzzle.Thwart('01001a')"],
    {"hors_jeu": ["01107"], "taille_main": 1, "exhausted": ["uj029"]},
    cibles=["01107"], accepter_choix=True)
CAS += _paire(
    "uj030", "08013", "Stealth Strike : 4 degats tuent le sbire -> 2 menaces retirees",
    "« Deal 4 damage to an enemy. If that enemy is defeated by this attack, remove 2 threat from a scheme »",
    [HEROS, "Puzzle.PutIntoPlay('01101')", "Puzzle.SetThreat('01097b', 5)"], [],
    {"hors_jeu": ["01101"], "menace": [["01097b", 3]]},
    main_exclusive=["uj030", "01089", "01089"], jouer=["uj030"], cibles=["01101", "01097b"])
CAS += _paire(
    "uj031", "60028", "Stealth Training : contrer et vaincre EXACTEMENT une manigance annexe -> etourdir Rhino",
    "« After you thwart and exactly defeat a side scheme, exhaust Stealth Training → stun an enemy » : 01107 a 1 "
    "menace, Spider-Man THW 1",
    [HEROS, "Puzzle.PutIntoPlay('uj031', under_control=True)", "Puzzle.Reveal('01107')",
     "Puzzle.SetThreat('01107', 1)"],
    ["Puzzle.Thwart('01001a')"],
    {"hors_jeu": ["01107"], "statuts": [["01094", "Stunned"]], "exhausted": ["uj031"]},
    cibles=["01107", "01094"], accepter_choix=True)
CAS += _paire(
    "uj032", "47015", "Three Steps Ahead : paye en [mental] + [physical] (2 types) -> 2 x 2 menaces",
    "« For each different resource type you used to pay for this card, choose a scheme and remove 2 threat » : "
    "deux types, deux manigances a 2 retraits",
    [HEROS, "Puzzle.Reveal('01107')", "Puzzle.SetThreat('01107', 3)", "Puzzle.SetThreat('01097b', 5)"], [],
    {"menace": [["01097b", 3], ["01107", 1]]},
    main_exclusive=["uj032", "01089", "01090"], jouer=["uj032"], cibles=["01097b", "01107"])
CAS += _paire(
    "uj035", "06031", "Under Surveillance : seuil de la manigance principale +4",
    "« Increase the target threat value of attached scheme by 4 »",
    [HEROS, "Puzzle.PutIntoPlay('uj035', under_control=True)", "Puzzle.Attach('uj035', '01097b')"], [],
    {"attributs_carte": [["01097b", "target_threat", 4]]})
CAS += _paire(
    "uj040", "21050", "Zone of Silence (identite MYSTIC) : defausse 4 du deck -> 4 menaces retirees",
    "« discard up to 4 cards from the top of your deck → remove 1 threat from that scheme for each card discarded » : "
    "le pilote choisit 4 ; ligne de base du deck : la partie de Doctor Strange en retire deja 1 des 6 (mesure : "
    "choix « 1 » -> 4 restantes), donc 6 - 1 - 4 = 1",
    ["Puzzle.ChangeForm('09001b')", SANS_DECK, DECK6, "Puzzle.SetThreat('01097b', 6)"], [],
    {"menace": [["01097b", 2]], "taille_deck_joueur": 1},
    heros="doctor_strange", main_exclusive=["uj040", "01089"], jouer=["uj040"], cibles=["01097b"],
    choisir_option="4")
CAS += _paire(
    "uj040", "21050", "Zone of Silence : Spider-Man (pas MYSTIC) ne peut PAS la jouer",
    "« Play only if your identity has the Mystic trait »",
    [HEROS, "Puzzle.Gain('uj040')"], [],
    {"carte": "uj040", "jouable": False, "en_jeu": 0},
    main=["01089", "01089"], verifier="max_par_joueur_jouable")


VERIFICATIONS = r'''
'''
