# Cas test_capacites du pack d'aspect TMNT LEADERSHIP (Inkwire, prefixe `ul`, pack tmnt_aspect_leadership).
# Filtre : `[ul]`. Gabarits PROCESSUS-CARTE : .planning/tmnt/aspects-leadership-gabarits.md.
#
# Conventions (reprises de tools/cas/rampage.py) :
#  - Spider-Man (01001) demarre en ALTER EGO ; HEROS le met en forme heros (ATQ 2, CTR 1, DEF 3, 10 PV) ;
#  - `main_exclusive` : la main ne contient QUE la carte jouee et de quoi payer
#    (01090 Strength = RR, 01088 Energy = YY, 01089 Genius = BB, 01002 Black Cat = Y) ;
#  - Rhino 01094 (14 PV), complot 01097b, sbire 01101 Hydra Mercenary (3 PV), 01102 Sandman (ELITE) ;
#  - SANS_BOOST : deck rencontre de « I'm Tough » (01105, aucune icone de boost) pour les attaques de Rhino ;
#  - Reskins (ability_link) : chaque cas existe DEUX fois, sur la carte TMNT et en TEMOIN sur l'officielle
#    (meme montage, meme chiffre attendu) : `_paire`, le jeton « @@ » vaut l'id de la carte.
SC = "rhino"
HEROS = "Puzzle.ChangeForm('01001b')"
SANS_DECK = "Puzzle.EmptyPlayerDeck()"
DECK6 = "Puzzle.CreatePlayerDeck('01089', '01089', '01089', '01089', '01089', '01089')"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105')"]
NYC = "Puzzle.PutIntoPlay('tr008', under_control=True)"


def M(card):
    return f"Puzzle.PutIntoPlay('{card}', under_control=True)"


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[ul] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": list(mise), "declencher": list(declencher),
           "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.update(cle)
    return cas


def _sub(x, cid):
    if isinstance(x, str):
        return x.replace("@@", cid)
    if isinstance(x, list):
        return [_sub(y, cid) for y in x]
    if isinstance(x, dict):
        return {k: _sub(v, cid) for k, v in x.items()}
    return x


def _paire(reskin, officielle, nom, pourquoi, mise, declencher, attendu, **cle):
    """Le cas sur le reskin, puis le TEMOIN identique sur l'officielle."""
    a = _c(f"{reskin} {nom}", pourquoi, _sub(mise, reskin), _sub(declencher, reskin), _sub(attendu, reskin),
           **_sub(cle, reskin))
    b = _c(f"{reskin} TEMOIN {officielle} : {nom}", "meme montage sur l'officielle, meme chiffre attendu",
           _sub(mise, officielle), _sub(declencher, officielle), _sub(attendu, officielle), **_sub(cle, officielle))
    return [a, b]


CAS = []

# ===================================================================== reskins IDENTIQUES (ability_link)
CAS += _paire("ul002", "21018", "Band Together : 2 allies en jeu -> 2 [wild], Maria Hill (cout 2) payee avec elle seule",
              "« generates [wild] for each ally you control (max 3) » : sans la capacite, rien ne paie Maria Hill",
              [HEROS, M("01002"), M("01041")], [], {"en_jeu": ["01067"], "defausse": ["@@"]},
              main_exclusive=["@@", "01067"], jouer=["01067"])
CAS += _paire("ul004", "31029", "Clarity of Purpose : Ressource de heros (incline + 1 degat a l'attache) -> [wild]",
              "attachee a l'identite : 1 [wild] + Black Cat (Y) paient Maria Hill (2) ; l'identite subit 1 degat",
              [HEROS, M("@@"), "Puzzle.AttachReel('@@', '01001a')"], [],
              {"en_jeu": ["01067"], "degats_identite": 1, "exhausted": ["@@"]},
              main_exclusive=["01067", "01002"], jouer=["01067"])
CAS += _paire("ul009", "29017", "Go All Out : 1 + 2 + 3 = 6 degats a Rhino, heros incline",
              "« deal damage equal to the total of your hero's THW, ATK, and DEF » ; Requirement [energy] (01088 YY)",
              [HEROS], [], {"degats": [["01094", 6]], "exhausted": ["01001a"]},
              main_exclusive=["@@", "01088"], jouer=["@@"], cibles=["01094"])
CAS += _paire("ul011", "61037", "Innate Inspiration : chaque allie controle gagne +1 PV",
              "« Each ally you control gets +1 hit point » (amelioration posee dans la zone du joueur)",
              [HEROS, M("01067"), M("@@")], [], {"attributs_carte": [["01067", "health", 1]]})
CAS += _paire("ul012", "01074", "Inspired : l'allie attache gagne +1 CTR et +1 ATQ",
              "« Attach to an ally. Attached ally gets +1 THW and +1 ATK »",
              [HEROS, M("01067")], [], {"attributs_carte": [["01067", "attack", 1], ["01067", "thwart", 1]]},
              main_exclusive=["@@", "01090"], jouer=["@@"], cibles=["01067"])
CAS += _paire("ul013", "01071", "Make the Call : Maria Hill de la defausse mise en jeu (cout imprime paye)",
              "« Pay the printed cost of an ally in any player's discard pile -> put that ally into play »",
              [HEROS, "Puzzle.CreatePlayerDiscardPile('01067')"], [], {"en_jeu": ["01067"]},
              main_exclusive=["@@", "01089"], jouer=["@@"], cibles=["01067"])
CAS += _paire("ul015", "40023", "Mission Leader : manigance annexe dejouee -> incline, chaque joueur pioche 1",
              "Spider-Man contre Breakin' & Takin' (1 menace) : la Reponse de heros incline la carte, main 1 -> 2",
              [HEROS, M("@@"), "Puzzle.PutIntoPlay('01107')", "Puzzle.SetThreat('01107', 1)"],
              ["Puzzle.Thwart('01001a')"], {"hors_jeu": ["01107"], "exhausted": ["@@"], "taille_main": 2},
              main_exclusive=["01090"], cibles=["01107"], accepter_choix=True)
CAS += _paire("ul017", "03013", "Napoleon : a l'entree en jeu, 1 degat a CHAQUE ennemi (Rhino et le sbire)",
              "« deal 1 damage to each enemy »", [HEROS, "Puzzle.PutIntoPlay('01101')"], [],
              {"degats": [["01094", 1], ["01101", 1]]},
              main_exclusive=["@@", "01090"], jouer=["@@"], accepter_choix=True)
CAS += _paire("ul018", "49018", "Noble Sacrifice : Maria Hill (2 PV imprimes) defaussee -> 2 soignes + Tenace",
              "« heal damage from your hero equal to that ally's printed hit points and give your hero a tough »",
              [HEROS, "Puzzle.Damage('01001a', 4)", M("01067")], [],
              {"degats_identite": 2, "statuts": [["01001a", "Tough"]], "defausse": ["01067"]},
              main_exclusive=["@@", "01089"], jouer=["@@"])
CAS += _paire("ul019", "51037", "Old Hob : Reponse forcee apres son attaque -> 1 menace sur le complot principal",
              "« After Old Hob attacks, place 1 threat on the main scheme » (complot a 0)",
              [HEROS, M("@@"), "Puzzle.EmptyHand()", "Puzzle.SetThreat('01097b', 0)"], ["Puzzle.Attack('@@')"],
              {"menace": [["01097b", 1]], "degats": [["01094", 2]]}, main_exclusive=["01090"], cibles=["01094"])
CAS += _paire("ul020", "01067", "Rasputin : a l'entree en jeu chaque joueur pioche 1 (main 0 -> 1)",
              "« each player draws 1 card » (main vide apres paiement)", [HEROS], [], {"taille_main": 1},
              main_exclusive=["@@", "01089"], jouer=["@@"], accepter_choix=True)
CAS += _paire("ul021", "62012", "Red Shell : defend contre Rhino (ATQ 2), previent 2 = son ATQ -> 0 degat",
              "« prevent damage from that attack equal to Red Shell's ATK » ; sans boost",
              [HEROS, M("@@")] + SANS_BOOST, ["Puzzle.Attack('01094', defender='@@')"],
              {"degats": [["@@", 0]], "en_jeu": ["@@"]}, main_exclusive=["01090"], accepter_choix=True)
CAS += _paire("ul022", "62019", "Righteous Purpose : allie a exactement 1 PV restant -> +2 CTR +2 ATQ",
              "« Each character you control that has exactly 1 hit point remaining gets +2 THW and +2 ATK »",
              [HEROS, M("01067"), "Puzzle.Damage('01067', 1)", M("@@")], [],
              {"attributs_carte": [["01067", "attack", 2], ["01067", "thwart", 2]]})
CAS += _paire("ul026", "45016", "Side-by-Side : redresser l'acolyte -> le heros se redresse aussi",
              "« Ready your sidekick -> ready your hero » : Black Cat porte Sidekick (45015), les deux inclines",
              [HEROS, M("01002"), M("45015"), "Puzzle.AttachReel('45015', '01002')", "Puzzle.Exhaust('01002')",
               "Puzzle.Exhaust('01001a')"], [], {"pret": ["01001a", "01002"], "defausse": ["@@"]},
              main_exclusive=["@@", "01088"], jouer=["@@"], accepter_choix=True)
CAS += _paire("ul027", "45015", "Sidekick : sur Black Cat (allie d'identite), +2 PV",
              "« Attach to an identity-specific ally you control. Attached ally gets +2 hit points »",
              [HEROS, M("01002")], [], {"attributs_carte": [["01002", "health", 2]]},
              main_exclusive=["@@", "01090"], jouer=["@@"], cibles=["01002"])
CAS += _paire("ul032", "21055", "Summoning Spell : identite MYSTIC (Doctor Strange) -> defausse jusqu'a un allie, mis en jeu",
              "« Discard cards from the top of your deck until you discard an ally -> put that ally into play »",
              ["Puzzle.ChangeForm('09001b')", SANS_DECK,
               "Puzzle.CreatePlayerDeck('01089', '01089', '01067', '01089')"], [], {"en_jeu": ["01067"]},
              heros="doctor_strange", main_exclusive=["@@", "01089"], jouer=["@@"])
CAS += _paire("ul033", "62015", "Take a Stand : apres la defense du heros, chaque allie +1 CTR +1 ATQ",
              "« After your hero defends, each ally you control gets +1 THW and +1 ATK »",
              [HEROS, M("01002")] + SANS_BOOST, ["Puzzle.Attack('01094', defender='01001a')"],
              {"attributs_carte": [["01002", "attack", 1], ["01002", "thwart", 1]], "defausse": ["@@"]},
              main_exclusive=["@@", "01088"], accepter_choix=True)
CAS += _paire("ul034", "06032", "Teamwork : attaque de base du heros + ATQ de Maria Hill inclinee -> 3 degats",
              "« exhaust an ally you control -> add that ally's matching power to your hero power »",
              [HEROS, M("01067")], ["Puzzle.Attack('01001a')"],
              {"degats": [["01094", 3]], "exhausted": ["01067"], "defausse": ["@@"]},
              main_exclusive=["@@"], cibles=["01094"], accepter_choix=True)
CAS += _paire("ul037", "62013", "Turtle-At-Arms : Toughness, et +2 ATQ +2 CTR tant qu'il porte un Tenace",
              "« Toughness » (desc, recopie) + « gets +2 ATK and +2 THW while he has a tough status card »",
              [HEROS, M("@@")], [],
              {"statuts": [["@@", "Tough"]], "attributs_carte": [["@@", "attack", 2], ["@@", "thwart", 2]]})
CAS += _paire("ul044", "49019", "You Got This! : contre de base + CTR de Maria Hill defaussee (1 + 2 = 3), heros redresse",
              "« discard an ally you control -> add that ally's matching power ... Ready your hero »",
              [HEROS, M("01067"), "Puzzle.EmptyHand()", "Puzzle.SetThreat('01097b', 5)"], ["Puzzle.Thwart('01001a')"],
              {"menace": [["01097b", 2]], "pret": ["01001a"], "defausse": ["01067", "@@"]},
              main_exclusive=["@@", "01090"], cibles=["01097b"], accepter_choix=True)
CAS += _paire("ul046", "21013", "Zetian : jouee de la main, Rhino stade 1 -> pioche 1",
              "« draw X cards, where X is equal to the villain's stage number »", [HEROS], [],
              {"taille_main": 1, "en_jeu": ["@@"]},
              main_exclusive=["@@", "01090", "01002"], jouer=["@@"], accepter_choix=True)

# ----- donnees des reskins : bandeau « ✦ <titre d'origine> » (Q-R1 : unique_also), traits propres
for _r, _o, _t in [("ul017", "03013", "Squirrel Girl"), ("ul019", "51037", "White Wolf"),
                   ("ul020", "01067", "Maria Hill"), ("ul021", "62012", "Iron Fist"),
                   ("ul037", "62013", "Misty Knight"), ("ul046", "21013", "White Tiger")]:
    CAS.append(_c(f"{_r} : bandeau « ✦ {_t} » : pas jouable quand {_o} est en jeu (unique_also)",
                  "decision Q-R1 : l'unicite se juge sur le titre TMNT ET sur le titre du bandeau",
                  [HEROS, "Puzzle.Gain('%s')" % _r, M(_o)], [],
                  {"carte": _r, "jouable": False, "en_jeu": 0},
                  main=["01088", "01089", "01090"], verifier="max_par_joueur_jouable"))
CAS.append(_c("ul019 Old Hob : porte SES traits (CAT, MUTANIMAL : coquille « MUTANIMALS » corrigee), pas WAKANDA",
              "Paper.Load lit `traits` sur l'entree du reskin ; `ability_link` ne copie que les capacites",
              [HEROS, M("ul019")], [],
              {"carte": "ul019", "presents": ["CAT", "MUTANIMAL"], "absents": ["WAKANDA", "MUTANIMALS"], "nom": "Old Hob",
               "unique": True}, verifier="reskin_identite"))

# ----- ul019 Old Hob est MUTANIMAL (coquille « MUTANIMALS » CONFIRMEE le 17/10/2026) : les Training s'y attachent
CAS += [
    _c("ul019 Old Hob MUTANIMAL : Splinter Dojo Training (ul028) s'y attache -> +1 CTR +1 ATQ +1 PV",
       "« Attach to a NINJA or MUTANIMAL ally » : Old Hob (CAT, MUTANIMAL) est le seul allie en jeu",
       [HEROS, M("ul019")], [],
       {"attributs_carte": [["ul019", "thwart", 1], ["ul019", "attack", 1], ["ul019", "health", 1]]},
       main_exclusive=["ul028", "01090"], jouer=["ul028"], cibles=["ul019"]),
    _c("ul019 Old Hob MUTANIMAL : Attack Training (ua004) s'y attache -> +1 ATQ +2 PV",
       "« Attach to a NINJA or MUTANIMAL ally » (ua004) : meme trait",
       [HEROS, M("ul019")], [],
       {"attributs_carte": [["ul019", "attack", 1], ["ul019", "health", 2]]},
       main_exclusive=["ua004", "01090"], jouer=["ua004"], cibles=["ul019"]),
]

# ----- ul033 Take a Stand : trait TACTIC remis (oubli de l'auteur, confirme le 17/10/2026)
CAS.append(_c("ul033 Take a Stand : porte le trait TACTIC (comme 62015)",
              "Paper.Load lit `traits` sur l'entree du reskin ; oubli de l'auteur confirme le 17/10/2026",
              [HEROS, "Puzzle.Gain('ul033')"], [],
              {"carte": "ul033", "presents": ["TACTIC"], "nom": "Take a Stand"}, verifier="tmnt_donnees_carte"))

# ===================================================================== cartes MODIFIEES / NOUVELLES
CAS += [
    # ---- ul001 Alopex
    _c("ul001 Alopex : Reponse a l'entree en jeu -> elle est camouflee (Cloaked)",
       "« Response: After Alopex enters play, cloak her »", [HEROS], [], {"statuts": [["ul001", "Cloaked"]]},
       main_exclusive=["ul001", "01090", "01002"], jouer=["ul001"], accepter_choix=True),
    _c("ul001 Alopex : Retaliate 1 (desc) -> Rhino qui l'attaque subit 1 degat",
       "mot-cle lu par le moteur (fiche retaliate.md) ; donnees, reste vert sans module (attendu)",
       [HEROS, M("ul001")] + SANS_BOOST, ["Puzzle.Attack('01094', defender='ul001')"],
       {"degats": [["01094", 1]]}, main_exclusive=["01090"]),
    # ---- ul005 Dask
    _c("ul005 Dask : 2 traitrises dans les 3 cartes du dessus -> 2 degats a Rhino",
       "« For each treachery looked at this way, deal 1 damage to an enemy » ; 01105 et 01104 sont des "
       "traitrises, 01101 un sbire",
       [HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01104', '01101')"], [],
       {"degats": [["01094", 2]], "dans_deck_rencontre": ["01105", "01104", "01101"]},
       main_exclusive=["ul005", "01090", "01002"], jouer=["ul005"], cibles=["01094"], accepter_choix=True),
    _c("ul005 Dask : aucune traitrise regardee -> aucun degat (contre-cas)",
       "trois sbires sur le dessus : le compte vaut 0", [HEROS, "Puzzle.EmptyEncounterDeck()",
                                                         "Puzzle.CreateEncounterDeck('01101', '01110', '01101')"], [],
       {"degats": [["01094", 0]]},
       main_exclusive=["ul005", "01090", "01002"], jouer=["ul005"], cibles=["01094"], accepter_choix=True),
    # ---- ul006 Defensive Formation
    _c("ul006 Defensive Formation : incline + 1 jeton blocage -> Tenace a un allie TURTLE (Red Shell)",
       "« give a TURTLE ally a tough status card » ; 3 jetons -> 2",
       [HEROS, M("ul006"), M("ul021")], ["Puzzle.Action('ul006')"],
       {"statuts": [["ul021", "Tough"]], "compteurs": [["ul006", "block", 2]], "exhausted": ["ul006"]},
       cibles=["ul021"], accepter_choix=True),
    _c("ul006 Defensive Formation : seul un allie NON TURTLE (Maria Hill) -> aucune cible, pas de Tenace",
       "contre-cas du trait : [[DEFENDER]] devenu [[TURTLE]]", [HEROS, M("ul006"), M("01067")], [],
       {"statuts_absents": [["01067", "Tough"]], "compteurs": [["ul006", "block", 3]]},
       declencher_tolerant=["Puzzle.Action('ul006')"], accepter_choix=True),
    # ---- ul007 Down the Drain
    _c("ul007 Down the Drain : Rampage 2 + allie defausse -> 2 degats, 2 menaces retirees, 2 cartes piochees",
       "« take 2 damage and discard 2 cards » (cout) ; « Discard an ally you control -> deal 2 damage to an enemy, "
       "remove 2 threat from a scheme, and draw 2 cards » : deck 6 -> 2 defaussees -> 2 piochees -> 2",
       [HEROS, SANS_DECK, DECK6, M("01041"), "Puzzle.EmptyHand()", "Puzzle.SetThreat('01097b', 5)"], [],
       {"degats_identite": 2, "degats": [["01094", 2]], "menace": [["01097b", 3]], "defausse": ["01041", "ul007"],
        "taille_main": 2, "taille_deck_joueur": 2},
       main_exclusive=["ul007", "01002"], jouer=["ul007"], cibles=["01094", "01097b", "01041"]),
    _c("ul007 Down the Drain : sans allie a defausser, la carte n'est pas jouable (aucun degat de Rampage)",
       "« Discard an ally you control » est un COUT : impayable -> rien n'est paye", [HEROS, SANS_DECK, DECK6], [],
       {"degats_identite": 0, "en_main": ["ul007"], "taille_deck_joueur": 6},
       main_exclusive=["ul007", "01002"], jouer=["ul007"], cibles=["01094", "01097b"]),
    # ---- ul008 Gennosuke
    _c("ul008 Gennosuke : apres son attaque, main vide -> il se defausse",
       "« choose to either discard 1 card from your hand, or discard Gennosuke » : seule la 2e option possible",
       [HEROS, M("ul008"), "Puzzle.EmptyHand()"], ["Puzzle.Attack('ul008')"],
       {"hors_jeu": ["ul008"], "degats": [["01094", 2]]}, cibles=["01094"]),
    _c("ul008 Gennosuke : apres son contre, defausse 1 carte de la main et reste en jeu",
       "option 1 choisie : la carte de la main part, Gennosuke reste ; contre 2 (5 -> 3)",
       [HEROS, M("ul008"), "Puzzle.EmptyHand()", "Puzzle.SetThreat('01097b', 5)"], ["Puzzle.Thwart('ul008')"],
       {"en_jeu": ["ul008"], "defausse": ["01090"], "menace": [["01097b", 3]]},
       main_exclusive=["01090"], cibles=["01097b", "01090"], preferer_option="Discard 1 card"),
    # ---- ul010 Heroes in a Half Shell
    _c("ul010 Heroes in a Half Shell : un allie TURTLE gagne +1 PV, pas Maria Hill",
       "« Each of your TURTLE allies get +1 hit point »", [HEROS, M("ul010"), M("ul021"), M("01067")], [],
       {"attributs_carte": [["ul021", "health", 1], ["01067", "health", 0]]}),
    _c("ul010 Heroes in a Half Shell : identite Leonardo (TURTLE) seule -> Red Shell (3) coute 2",
       "« If each of your characters has the TURTLE trait, each of your TURTLE allies cost 1 fewer » : "
       "01090 (RR) suffit",
       ["Puzzle.ChangeForm('tl001b')", M("ul010")], [], {"en_jeu": ["ul021"]}, heros="leonardo",
       main_exclusive=["ul021", "01090"], jouer=["ul021"], accepter_choix=True),
    _c("ul010 Heroes in a Half Shell : un personnage NON TURTLE (Maria Hill) -> pas de reduction, Red Shell reste en main",
       "contre-cas de « If EACH of your characters »", ["Puzzle.ChangeForm('tl001b')", M("ul010"), M("01067")], [],
       {"en_main": ["ul021"]}, heros="leonardo", main_exclusive=["ul021", "01090"], jouer=["ul021"]),
    # ---- ul014 Midnight Veil
    _c("ul014 Midnight Veil : sans soutien NYC, 3 personnages controles -> 2 seulement camoufles",
       "« Cloak up to 2 characters you control » : plafond 2", [HEROS, M("01067"), M("01002")], [],
       {"cloaked": 2}, main_exclusive=["ul014", "01088", "01089"], jouer=["ul014"], accepter_choix=True,
       verifier="ul_compte"),
    _c("ul014 Midnight Veil : avec un soutien NYC (Shell Cycle) -> 3 camoufles",
       "« (3 characters instead if you control a NYC support) »", [HEROS, M("01067"), M("01002"), NYC], [],
       {"cloaked": 3}, main_exclusive=["ul014", "01088", "01089"], jouer=["ul014"], accepter_choix=True,
       verifier="ul_compte"),
    # ---- ul016 Naginata
    _c("ul016 Naginata : Maria Hill attaque, Naginata inclinee -> +2 a ce pouvoir (1 + 2 = 3)",
       "« When attached character uses a basic power, exhaust Naginata -> they get +2 »",
       [HEROS, M("01067"), M("ul016"), "Puzzle.AttachReel('ul016', '01067')"], ["Puzzle.Attack('01067')"],
       {"degats": [["01094", 3]], "exhausted": ["ul016"]}, main_exclusive=["01090"], cibles=["01094"],
       accepter_choix=True),
    _c("ul016 Naginata : Maria Hill contre -> 2 + 2 = 4 menaces retirees",
       "le meme +2 sur le pouvoir CTR", [HEROS, M("01067"), M("ul016"), "Puzzle.AttachReel('ul016', '01067')",
                                         "Puzzle.EmptyHand()", "Puzzle.SetThreat('01097b', 5)"], ["Puzzle.Thwart('01067')"],
       {"menace": [["01097b", 1]], "exhausted": ["ul016"]}, main_exclusive=["01090"], cibles=["01097b"],
       accepter_choix=True),
    _c("ul016 Naginata : TEMOIN D'INCLINAISON, deja inclinee -> pas de bonus (1 degat)",
       "« exhaust Naginata » est le cout : inclinee, elle ne part pas",
       [HEROS, M("01067"), M("ul016"), "Puzzle.AttachReel('ul016', '01067')", "Puzzle.Exhaust('ul016')"],
       ["Puzzle.Attack('01067')"], {"degats": [["01094", 1]]}, main_exclusive=["01090"], cibles=["01094"],
       accepter_choix=True),
    # ---- ul023 Rubble Rouser
    _c("ul023 Rubble Rouser : un allie vaincu -> Rampage 3 paye, un allie du deck mis en jeu INCLINE",
       "« After an ally is defeated, search your deck for an ally and put it into play, exhausted »",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01089', '01089', '01089', '01066', '01068', '01075', "
                          "'01089', '01089', '01089')", M("01002")], ["Puzzle.Damage('01002', 2)"],
       {"degats_identite": 3, "allies_inclines": 1, "allies": 1, "defausse": ["ul023"]},
       main_exclusive=["ul023", "01090"], accepter_choix=True, verifier="ul_compte"),
    # ---- ul024 Sense of Dread
    _c("ul024 Sense of Dread : attachee au sbire que le heros a attaque -> il gagne vulnerable",
       "« Attach to a minion that your hero attacked this turn. If attached to a non-ELITE minion, it gains "
       "vulnerable »", [HEROS, "Puzzle.PutIntoPlay('01101')"], ["Puzzle.Attack('01001a')"],
       {"vulnerable": [["01101", True]], "pose_sur": [["ul024", "01101"]]},
       main_exclusive=["ul024", "01089"], cibles=["01101"], jouer_apres=["ul024"], verifier="ul_compte"),
    _c("ul024 Sense of Dread : sbire ELITE (Sandman) attaque -> attachee mais PAS vulnerable",
       "« non-ELITE » : contre-cas", [HEROS, "Puzzle.PutIntoPlay('01102')"], ["Puzzle.Attack('01001a')"],
       {"vulnerable": [["01102", False]], "pose_sur": [["ul024", "01102"]]},
       main_exclusive=["ul024", "01089"], cibles=["01102"], jouer_apres=["ul024"], verifier="ul_compte"),
    _c("ul024 Sense of Dread : sbire NON attaque ce tour -> pas jouable",
       "« that your hero attacked this turn »", [HEROS, "Puzzle.PutIntoPlay('01101')", "Puzzle.Gain('ul024')"], [],
       {"carte": "ul024", "jouable": False, "en_jeu": 0}, main=["01089"], verifier="max_par_joueur_jouable"),
    _c("ul024 Sense of Dread : le sbire attache quitte le jeu -> Interruption, pioche 1",
       "« When attached minion leaves play, draw 1 card » : main 0 -> 1",
       [HEROS, "Puzzle.PutIntoPlay('01101')", M("ul024"), "Puzzle.AttachReel('ul024', '01101')",
        "Puzzle.EmptyHand()"],
       ["Puzzle.Discard(Puzzle.FindFaceInPlay('01101'))"], {"taille_main": 1, "hors_jeu": ["01101"]}, accepter_choix=True),
    _c("ul024 Sense of Dread : le sbire attache est VAINCU (attaque du heros) -> pioche 1",
       "« leaves play » couvre aussi la defaite : 2 degats sur 1 PV restant",
       [HEROS, "Puzzle.PutIntoPlay('01101')", "Puzzle.Damage(Puzzle.FindFaceInPlay('01101'), 2)", M("ul024"),
        "Puzzle.AttachReel('ul024', '01101')", "Puzzle.EmptyHand()"],
       ["Puzzle.Attack('01001a')"], {"taille_main": 1, "hors_jeu": ["01101"]}, cibles=["01101"],
       accepter_choix=True),
    # ---- ul025 Shogun
    _c("ul025 Shogun : defausse un allie de la main -> Tenace sur un allie (lui-meme)",
       "« discard an ally from your hand -> give an ally a tough status card »", [HEROS], [],
       {"statuts": [["ul025", "Tough"]], "defausse": ["01067"]},
       main_exclusive=["ul025", "01090", "01067"], payer_avec=["01090"], jouer=["ul025"], cibles=["ul025", "01067"],
       accepter_choix=True),
    _c("ul025 Shogun : sans allie en main, pas de Tenace (cout impayable)",
       "contre-cas du cout", [HEROS], [], {"statuts_absents": [["ul025", "Tough"]], "en_jeu": ["ul025"]},
       main_exclusive=["ul025", "01090"], jouer=["ul025"], accepter_choix=True),
    # ---- ul028 Splinter Dojo Training
    _c("ul028 Splinter Dojo Training : sur un allie NINJA -> +1 CTR +1 ATQ +1 PV",
       "« Attach to a NINJA or MUTANIMAL ally » ; Red Shell est NINJA", [HEROS, M("ul021")], [],
       {"attributs_carte": [["ul021", "thwart", 1], ["ul021", "attack", 1], ["ul021", "health", 1]]},
       main_exclusive=["ul028", "01090"], jouer=["ul028"], cibles=["ul021"]),
    _c("ul028 Splinter Dojo Training : seul allie NI NINJA NI MUTANIMAL (Maria Hill) -> pas jouable",
       "contre-cas du trait", [HEROS, M("01067"), "Puzzle.Gain('ul028')"], [],
       {"carte": "ul028", "jouable": False, "en_jeu": 0}, main=["01090"], verifier="max_par_joueur_jouable"),
    # ---- ul029 Splinter
    _c("ul029 Splinter : regarde 5, en prend 1, le reste dessous (deck 6 -> 5, main 0 -> 1)",
       "« look at the top 5 cards of your deck. Add 1 of those cards to your hand »",
       [HEROS, SANS_DECK, DECK6], [], {"taille_main": 1, "taille_deck_joueur": 5},
       main_exclusive=["ul029", "01090"], jouer=["ul029"], accepter_choix=True),
    # ---- ul030 Street Vendor
    _c("ul030 Street Vendor : se defausse -> soigne 3 au total (2 sur le heros, 1 sur Maria Hill)",
       "« Discard Street Vendor -> heal a total of 3 damage from among characters you control »",
       [HEROS, M("ul030"), "Puzzle.Damage('01001a', 2)", M("01067"), "Puzzle.Damage('01067', 1)"],
       ["Puzzle.Action('ul030')"], {"degats_identite": 0, "degats": [["01067", 0]], "defausse": ["ul030"]},
       accepter_choix=True),
    _c("ul030 Street Vendor : avec un soutien NYC, coute 1 (Black Cat suffit)",
       "« Reduce the cost to play this card by 1 if you control a NYC support »", [HEROS, NYC], [],
       {"en_jeu": ["ul030"]}, main_exclusive=["ul030", "01002"], jouer=["ul030"]),
    _c("ul030 Street Vendor : sans soutien NYC, Black Cat ne suffit pas (contre-cas)",
       "cout 2 plein", [HEROS], [], {"en_main": ["ul030"]}, main_exclusive=["ul030", "01002"], jouer=["ul030"]),
    # ---- ul031 Suit Up : LECTURE LITTERALE (17/10/2026) « an upgrade that can be attached to AN ally »
    _c("ul031 Suit Up : Black Cat et Sidekick (attachable a CET allie) ajoutes a la main",
       "montage du cas 45017 : l'upgrade est attachable a l'allie trouve, donc aussi (a fortiori) a UN allie",
       [], ["Puzzle.CreatePlayerDeck('01002', '45015', '01089')"],
       {"en_main": ["01002", "45015"], "taille_main": 2},
       main_exclusive=["ul031", "01088"], jouer=["ul031"], accepter_choix=True),
    _c("ul031 Suit Up : amelioration attachable a UN AUTRE allie que celui trouve (Sidekick -> Black Cat en jeu) -> ajoutee",
       "lecture litterale : deck = Maria Hill (allie trouve) + Sidekick (« identity-specific ally you control », "
       "attachable a Black Cat EN JEU mais pas a Maria Hill). Sous la lecture de l'officielle (« THAT ally ») "
       "Sidekick serait ecarte",
       [M("01002"), SANS_DECK, "Puzzle.CreatePlayerDeck('01067', '45015', '01089')"], [],
       {"en_main": ["01067", "45015"], "taille_main": 2},
       main_exclusive=["ul031", "01088"], jouer=["ul031"], accepter_choix=True),
    _c("ul031 Suit Up : aucune amelioration attachable a un allie (Armored Vest, « players ») -> l'allie seul est ajoute",
       "lecture litterale : Armored Vest 01081 ne se pose pas sur un allie ; la recherche d'amelioration ne propose "
       "rien et l'allie trouve vient quand meme",
       [SANS_DECK, "Puzzle.CreatePlayerDeck('01067', '01081', '01089')"], [],
       {"en_main": ["01067"], "absent_main": ["01081"], "taille_main": 1},
       main_exclusive=["ul031", "01088"], jouer=["ul031"], accepter_choix=True),
    # ---- ul035 Turtle Power
    _c("ul035 Turtle Power : identite TURTLE, un allie TURTLE du dessus mis en jeu, puis en main a la fin de la phase",
       "« Search the top 5 cards of your deck for a TURTLE ally and put it into play ... add it to your hand »",
       ["Puzzle.ChangeForm('tl001b')", SANS_DECK, "Puzzle.CreatePlayerDeck('01089', 'ul021', '01089')"], [],
       {"en_main": ["ul021"]}, heros="leonardo", main_exclusive=["ul035", "01088"], jouer=["ul035"],
       accepter_choix=True, declencher_final=["Puzzle.EndPlayerPhase()"]),
    _c("ul035 Turtle Power : identite NON TURTLE (Spider-Man) -> pas jouable",
       "« Play only if your identity has the TURTLE trait »", [HEROS, "Puzzle.Gain('ul035')"], [],
       {"carte": "ul035", "jouable": False, "en_jeu": 0}, main=["01088"], verifier="max_par_joueur_jouable"),
    # ---- ul036 Turtle Titan
    _c("ul036 Turtle Titan : apres son contre, se soigne de 2 (2 + 1 consecutif - 2 = 1)",
       "« After Turtle Titan thwarts a scheme, heal 2 damage from him »",
       [HEROS, M("ul036"), "Puzzle.Damage('ul036', 2)", "Puzzle.EmptyHand()", "Puzzle.SetThreat('01097b', 5)"], ["Puzzle.Thwart('ul036')"],
       {"degats": [["ul036", 1]], "menace": [["01097b", 4]]}, main_exclusive=["01090"], cibles=["01097b"],
       accepter_choix=True),
    # ---- ul038 Unified Strike (Hero Interrupt, titre corrige : coquilles confirmees le 17/10/2026)
    _c("ul038 Unified Strike : Maria Hill attaque + ATQ du heros (1 + 2 = 3), sans degat consecutif",
       "Interruption de heros, comme 58020 (la coquille « Hero Response: When » est corrigee)",
       [HEROS, M("01067")], ["Puzzle.Attack('01067')"],
       {"degats": [["01094", 3], ["01067", 0]], "exhausted": ["01001a"]},
       main_exclusive=["ul038"], cibles=["01094"], accepter_choix=True),
    _c("ul038 Unified Strike : le titre est « Unified Strike » (et non « Stike »), trait TACTIC",
       "coquille de titre confirmee le 17/10/2026 ; donnee de la carte (reste vert sans le script)",
       [HEROS, "Puzzle.Gain('ul038')"], [],
       {"carte": "ul038", "presents": ["TACTIC"], "nom": "Unified Strike"}, verifier="tmnt_donnees_carte"),
    # ---- ul039 Venus
    _c("ul039 Venus : a l'entree en jeu, attache face cachee une carte de la defausse qui partage un trait",
       "« choose a card in your discard pile that shares a TRAIT with Venus » : Red Shell (NINJA TURTLE) oui",
       [HEROS, "Puzzle.CreatePlayerDiscardPile('ul021')"], [], {"pose_sous": [["ul039", "ul021"]]},
       main_exclusive=["ul039", "01090", "01002"], jouer=["ul039"], cibles=["ul021"], accepter_choix=True),
    _c("ul039 Venus : une carte SANS trait commun (Maria Hill) n'est pas proposee",
       "contre-cas du filtre", [HEROS, "Puzzle.CreatePlayerDiscardPile('01067')"], [],
       {"taille_pose_sous": [["ul039", 0]], "defausse": ["01067"]},
       main_exclusive=["ul039", "01090", "01002"], jouer=["ul039"], cibles=["01067"], accepter_choix=True),
    _c("ul039 Venus : la carte attachee (un ALLIE, Turtle-At-Arms) est jouable comme depuis la main",
       "« You may play the CARD attached to Venus as if it were in your hand » : pas seulement un evenement",
       [HEROS, M("ul039"), "Puzzle.PlaceUnder('ul037', 'ul039')"], [], {"carte": "ul037", "jouable": True},
       main_exclusive=["01090", "01002"], verifier="ul_jouable_hors_main"),
    _c("ul039 Venus : TEMOIN, la meme carte posee sous un autre allie (Maria Hill) n'est PAS jouable",
       "c'est bien Venus qui rend la carte jouable", [HEROS, M("01067"), "Puzzle.PlaceUnder('ul037', '01067')"], [],
       {"carte": "ul037", "jouable": False}, main_exclusive=["01090", "01002"], verifier="ul_jouable_hors_main"),
    # ---- ul040 Weasel In + ul041-043
    _c("ul040 Weasel In : jouee (cout 0) -> manigance a 2 menaces, les 3 belettes liees mises de cote",
       "Linked (fiche linked.md) : ul041-043 fabriquees de cote avec la manigance ; « 2 [per_player] »",
       [HEROS], [], {"en_jeu": ["ul040"], "menace": [["ul040", 2]], "mis_de_cote_scenario": ["ul041", "ul042", "ul043"]},
       main_exclusive=["ul040"], jouer=["ul040"]),
    _c("ul040 Weasel In : dejouee -> les belettes mises de cote sont melangees dans le deck rencontre",
       "« When Defeated: Shuffle the set-aside WEASEL allies into the encounter deck »",
       [HEROS, M("ul040"), "Puzzle.SetThreat('ul040', 1)"], ["Puzzle.Thwart('01001a')"],
       {"dans_deck_rencontre": ["ul041", "ul042", "ul043"], "hors_jeu": ["ul040"]},
       cibles=["ul040"], accepter_choix=True),
    _c("ul041 Mushroom : revelee -> soigne 2 a un personnage ami et entre en jeu sous votre controle",
       "« Heal 2 damage from a friendly character and put Mushroom into play under your control »",
       [HEROS, "Puzzle.Damage('01001a', 3)"] + SANS_BOOST, ["Puzzle.Reveal('ul041')"],
       {"en_jeu": ["ul041"], "degats_identite": 1}, cibles=["01001a"], accepter_choix=True),
    _c("ul042 Zanna : revelee -> retire 2 menaces d'une manigance et entre en jeu",
       "« Remove 2 threat from a scheme and put Zanna into play »",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.SetThreat('01097b', 5)"] + SANS_BOOST, ["Puzzle.Reveal('ul042')"],
       {"en_jeu": ["ul042"], "menace": [["01097b", 3]]}, cibles=["01097b"], accepter_choix=True),
    _c("ul043 Zink : revelee -> 2 degats a un ennemi et entre en jeu",
       "« Deal 2 damage to an enemy and put Zink into play »", [HEROS] + SANS_BOOST, ["Puzzle.Reveal('ul043')"],
       {"en_jeu": ["ul043"], "degats": [["01094", 2]]}, cibles=["01094"], accepter_choix=True),
    _c("ul043 Zink : hors limite d'allies (3 allies deja en jeu -> 4 en jeu, aucun defausse)",
       "« Zink does not count against your ally limit » (`ThisNotCountAllyLimit`, modele 39071)",
       [HEROS, M("01002"), M("01067"), M("01041")] + SANS_BOOST, ["Puzzle.Reveal('ul043')"],
       {"en_jeu": ["ul043", "01002", "01067", "01041"]}, cibles=["01094"], accepter_choix=True),
    # ---- ul045 Zato-Ino
    _c("ul045 Zato-Ino : attaque et blesse Rhino -> Rhino Dazed",
       "« After Zato-Ino attacks and damages an enemy, daze that enemy »", [HEROS, M("ul045")],
       ["Puzzle.Attack('ul045')"], {"statuts": [["01094", "Dazed"]], "degats": [["01094", 1]]},
       main_exclusive=["01090"], cibles=["01094"], accepter_choix=True),
    _c("ul045 Zato-Ino : Rhino Tenace (aucun degat) -> pas de Dazed (contre-cas « and damages »)",
       "l'attaque est absorbee par le Tenace", [HEROS, M("ul045"), "Puzzle.Tough('01094')"],
       ["Puzzle.Attack('ul045')"], {"statuts_absents": [["01094", "Dazed"]], "degats": [["01094", 0]]},
       main_exclusive=["01090"], cibles=["01094"], accepter_choix=True),
]


VERIFICATIONS = r'''
def ul_jouable_hors_main(monde, aides):
    """La carte `attendu.carte` (posee hors de la main) est-elle OFFERTE au jeu par le moteur ? Meme filtre que
    `jouer_carte_glissee` du harnais (WhenPlayerLikeInTurn + FilterAvailableEffects), sans exiger l'identite
    comme hote."""
    from game.message import Message
    from game.effect.rule import GameRule
    from game.event.manager import EventManager
    attendu = aides["cas"]["attendu"]
    joueur = monde.players[0]
    face = None
    for objet in monde.object_manager.card_dict.values():
        f = getattr(objet, "face", None)
        if f is not None and getattr(f.paper, "card_id", None) == attendu["carte"]:
            face = f
    if face is None:
        return False, f"{attendu['carte']} introuvable"
    effets = face.effect.Find(func_name="Play", when=Message.WhenPlayerInTurn)
    message = Message.WhenPlayerLikeInTurn(joueur, GameRule(joueur.GetIdentity()))
    message.Send()
    jouable = bool(EventManager.FilterAvailableEffects(message, effets, joueur, monde, None))
    if jouable != attendu["jouable"]:
        return False, f"jouable={jouable} (attendu {attendu['jouable']}), zone {face.card.area}"
    return True, f"jouable={jouable}"

def ul_compte(monde, aides):
    """Comptes du pack ul : `cloaked` (personnages du joueur 1 camoufles), `allies` / `allies_inclines`
    (allies controles), `vulnerable` [[id, bool]], `pose_sur` [[upgrade, hote]], plus les cles d'etat_attendu."""
    attendu = dict(aides["cas"].get("attendu") or {})
    joueur = monde.players[0]
    soucis = []
    persos = [f for f in joueur.GetControlCharacters() if f is not None]
    if "cloaked" in attendu:
        n = sum(1 for f in persos if f.IsCloaked())
        if n != attendu.pop("cloaked"):
            soucis.append(f"{n} personnage(s) camoufle(s)")
    allies = [f for f in persos if type(f).__name__ == "Ally" or f.paper.type == "Ally"]
    if "allies" in attendu:
        if len(allies) != attendu.pop("allies"):
            soucis.append(f"{len(allies)} allie(s) controle(s) : {[a.paper.card_id for a in allies]}")
    if "allies_inclines" in attendu:
        n = sum(1 for a in allies if a.IsExhaust())
        if n != attendu.pop("allies_inclines"):
            soucis.append(f"{n} allie(s) incline(s)")
    for cid, voulu in attendu.pop("vulnerable", []):
        f = aides["par_id"](monde, cid)
        v = f is not None and f.IsVulnerable()
        if v != voulu:
            soucis.append(f"{cid} vulnerable={v}")
    for up, hote in attendu.pop("pose_sur", []):
        u = aides["par_id"](monde, up)
        h = aides["par_id"](monde, hote)
        if u is None or h is None or getattr(u, "bind_face", None) is not h:
            soucis.append(f"{up} n'est pas attachee a {hote}")
    if soucis:
        return False, " ; ".join(soucis)
    if attendu:
        aides["cas"] = dict(aides["cas"], attendu=attendu)
        return etat_attendu(monde, aides)
    return True, "comptes conformes"
'''
