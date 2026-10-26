# Cas test_capacites des cartes de CAMPAGNE et d'aspect de HELLFIRE HUNT (Dipsome, prefixe `hf`, hf001-hf099, pack hellfire_hunt) :
# noms prefixes « [hf] » puis le card_id (substituer_pack.py filtre dessus).
#
# Rappels de montage :
#  - le deck `spider_man` demarre en ALTER EGO (01001b) ; `Puzzle.ChangeToFace('01001b', '01001a')` le passe en HEROS ;
#  - Rhino 01094 est le vilain, 01097b son complot principal ; 01101 Hydra Mercenary (3 PV, Guard) et 01110 Hydra Bomber des sbires ;
#  - ressources : 01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR ; `main_exclusive` DEFAUSSE la main de depart ;
#  - le deck de rencontre est vide + 8 fillers 01098 : aucune carte de boost parasite, aucun surge.
SC = "rhino"
HEROS = "Puzzle.ChangeToFace('01001b', '01001a')"
VILAIN = "01094"
COMPLOT = "01097b"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01098', '01098', '01098', '01098', '01098', '01098', '01098', '01098')"]


def en_jeu(*ids):
    return [f"Puzzle.PutIntoPlay('{i}', under_control=True)" for i in ids]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    mise = SANS_BOOST + list(mise)
    cas = {"nom": "[hfc] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "hf_etat"), "attendu": attendu}
    cas.setdefault("regles", ["v16_all", "v18_all"])
    cas.update(cle)
    return cas


CAS = [
    # ============================================================ hf013 Armor
    _c("hf013 Armor : apres avoir defendu contre une attaque ennemie, 1 degat a elle -> carte Tough (2 + 1 = 3 degats)",
       "« Response: After Armor defends against an enemy attack, deal 1 damage to her -> give her a tough status card » : Rhino (ATK 2) attaque, Armor defend",
       [HEROS, *en_jeu("hf013")], [f"Puzzle.Attack('{VILAIN}', defender='hf013')"],
       {"statuts": [["hf013", "Tough"]], "degats": [["hf013", 3]]}, accepter_choix=True),
    _c("hf013 Armor : CONTRE-CAS, Armor ne defend pas -> aucun statut Tough",
       "la Response n'existe qu'apres une DEFENSE d'Armor", [HEROS, *en_jeu("hf013")], [f"Puzzle.Attack('{VILAIN}')"],
       {"statuts_absents": [["hf013", "Tough"]], "degats": [["hf013", 0]]}, accepter_choix=True),
    _c("hf013 Armor : valeurs imprimees PV 5, ATK 1, THW 1, RECRUITED MUTANT",
       "nombres texte <-> code (scan)", [HEROS, *en_jeu("hf013")], [],
       {"pv_max": [["hf013", 5]], "traits_de": [["hf013", "RECRUITED"], ["hf013", "MUTANT"]]}),
    # ============================================================ hf015 Dazzler
    _c("hf015 Dazzler : en entrant en jeu, desoriente jusqu'a 2 sbires (et pas le vilain)",
       "« Response: After Dazzler enters play, confuse up to 2 minions » : deux sbires en jeu, Dazzler arrive",
       [HEROS, *en_jeu("01101", "01110")], en_jeu("hf015"),
       {"statuts": [["01101", "Confused"], ["01110", "Confused"]], "statuts_absents": [[VILAIN, "Confused"]]}, accepter_choix=True),
    _c("hf015 Dazzler : TROIS sbires en jeu -> deux seulement sont desorientes (jusqu'a 2)",
       "la borne haute « up to 2 » : un troisieme sbire n'est pas desoriente",
       [HEROS, *en_jeu("01101", "01110", "01100")], en_jeu("hf015"),
       {"statuts": [["01101", "Confused"], ["01110", "Confused"]], "statuts_absents": [["01100", "Confused"]]}, accepter_choix=True),
    # ============================================================ hf016 ForgetMeNot
    _c("hf016 ForgetMeNot : a la fin du round il est defausse",
       "« Forced Response: At the end of the round, if ForgetMeNot is still in play, discard him »",
       [HEROS, *en_jeu("hf016")], ["Puzzle.SendAfterRoundEnd()"], {"hors_jeu": ["hf016"], "defausse": ["hf016"]}),
    _c("hf016 ForgetMeNot : TEMOIN, sans fin de round il reste en jeu",
       "contre-cas : la defausse n'a lieu qu'en fin de round", [HEROS, *en_jeu("hf016")], [], {"en_jeu": ["hf016"]}),
    # ============================================================ hf017 Marrow
    _c("hf017 Marrow : apres avoir attaque un ennemi, depense une ressource [physical] -> l'ennemi est etourdi",
       "« Response: After Marrow attacks an enemy, spend a [physical] resource -> stun that enemy » : Rhino attaque par Marrow, Strength (RR) payee",
       [HEROS, *en_jeu("hf017")], ["Puzzle.Attack('hf017')"], {"statuts": [[VILAIN, "Stunned"]]},
       main_exclusive=["01090"], payer_avec=["01090"], cibles=[VILAIN], accepter_choix=True),
    _c("hf017 Marrow : CONTRE-CAS, aucune ressource a depenser -> pas d'etourdissement",
       "le cout [physical] n'est pas payable : la Response n'est pas offerte", [HEROS, *en_jeu("hf017"), "Puzzle.EmptyHand()"], ["Puzzle.Attack('hf017')"],
       {"statuts_absents": [[VILAIN, "Stunned"]]}, cibles=[VILAIN], accepter_choix=True),
    # ============================================================ hf018 Glob Herman
    _c("hf018 Glob Herman : valeurs imprimees PV 2, Toughness (carte Tough a l'entree en jeu)",
       "« Toughness. » est lu directement dans `desc` : la carte arrive avec un statut Tough", [HEROS, *en_jeu("hf018")], [],
       {"pv_max": [["hf018", 2]], "statuts": [["hf018", "Tough"]]}),
    # ============================================================ hf020 Oya
    _c("hf020 Oya : en entrant en jeu, 4 degats a un ennemi (premiere branche)",
       "« choose one: deal 4 damage to an enemy, or stun an enemy »", [HEROS], en_jeu("hf020"),
       {"degats": [[VILAIN, 4]]}, cibles=[VILAIN], preferer_option="Deal 4 damage", accepter_choix=True),
    _c("hf020 Oya : seconde branche, l'ennemi est etourdi (et ne prend pas de degats)",
       "l'autre branche du choix", [HEROS], en_jeu("hf020"),
       {"statuts": [[VILAIN, "Stunned"]], "degats": [[VILAIN, 0]]}, cibles=[VILAIN], preferer_option="Stun an enemy", accepter_choix=True),
    # ============================================================ hf021 Polaris
    _c("hf021 Polaris : Action, depense une ressource [energy] -> soigne 2 degats d'elle",
       "« Action: Spend a [energy] resource -> heal 2 damage from Polaris » : Polaris a 1 degat (PV 2), Energy (YY) payee",
       [HEROS, *en_jeu("hf021"), "Puzzle.Damage('hf021', 1)"], ["Puzzle.Action('hf021')"],
       {"degats": [["hf021", 0]]}, main_exclusive=["01088"], payer_avec=["01088"], accepter_choix=True),
    # ============================================================ hf022 Sage
    _c("hf022 Sage : apres une contrariete, la carte defaussee du deck de rencontre porte une etoile de boost -> un sbire est etourdi",
       "« After Sage thwarts, discard the top card of the encounter deck. Stun a minion if that card has a star icon in the boost area » : 01121 (boost avec etoile) au sommet",
       [HEROS, "Puzzle.EmptyHand()", *en_jeu("hf022", "01101"), f"Puzzle.SetThreat('{COMPLOT}', 3)", "Puzzle.MoveTo('01121', 'EncounterDeck')"], ["Puzzle.Thwart('hf022')"],
       {"statuts": [["01101", "Stunned"]]}, cibles=[COMPLOT, "01101"], accepter_choix=True),
    _c("hf022 Sage : CONTRE-CAS, la carte defaussee n'a pas d'etoile de boost -> aucun sbire etourdi",
       "01110 Hydra Bomber n'a pas d'etoile au boost", [HEROS, "Puzzle.EmptyHand()", *en_jeu("hf022", "01101"), f"Puzzle.SetThreat('{COMPLOT}', 3)", "Puzzle.MoveTo('01110', 'EncounterDeck')"],
       ["Puzzle.Thwart('hf022')"], {"statuts_absents": [["01101", "Stunned"]], "menace": [[COMPLOT, 2]]}, cibles=[COMPLOT, "01101"], accepter_choix=True),
    # ============================================================ hf023 Wiz-Kid
    _c("hf023 Wiz-Kid : +1 CTR par manigance annexe en jeu (1 -> 2 avec une manigance annexe)",
       "« Wiz-Kid gets +1 THW for each side scheme in play »", [HEROS, *en_jeu("hf023"), "Puzzle.PutIntoPlay('01108')"], [],
       {"attributs_carte": [["hf023", "thwart", 1]]}),
    # ============================================================ hf024 Wolfsbane
    _c("hf024 Wolfsbane : en entrant en jeu, +2 ATK jusqu'a la fin du round",
       "« Response: After Wolfsbane enters play, she gets +2 ATK until the end of the round »", [HEROS], en_jeu("hf024"),
       {"attributs_carte": [["hf024", "attack", 2]]}, accepter_choix=True),
    # ============================================================ hf028 Selene
    _c("hf028 Selene : apres avoir vaincu un sbire, elle se soigne 2 -> elle survit a ses degats consequents (PV 2, 1 degat + 1 consequent)",
       "« Response: After Selene attacks and defeats a minion, heal 2 damage from her » : Selene a 1 degat (PV 2) ; sans soin, le degat CONSEQUENT (ATK avec une etoile) la tuerait ; avec soin elle finit a 1 degat",
       [HEROS, *en_jeu("hf028", "01110"), "Puzzle.Damage('hf028', 1)", "Puzzle.Damage('01110', 1)"], ["Puzzle.Attack('hf028')"],
       {"degats": [["hf028", 1]], "hors_jeu": ["01110"]}, main_exclusive=["01090"], cibles=["01110"], accepter_choix=True),
    _c("hf028 Selene : CONTRE-CAS, elle attaque le vilain (pas un sbire) -> pas de soin, elle est vaincue par le degat consequent",
       "la Response ne part que si Selene VAINC un sbire", [HEROS, *en_jeu("hf028"), "Puzzle.Damage('hf028', 1)"], ["Puzzle.Attack('hf028')"],
       {"hors_jeu": ["hf028"]}, main_exclusive=["01090"], cibles=[VILAIN], accepter_choix=True),
    # ============================================================ hf019 Mirage
    _c("hf019 Mirage : valeurs imprimees PV 3, ATK 2, THW 1, RECRUITED MUTANT",
       "nombres texte <-> code (scan)", [HEROS, *en_jeu("hf019")], [],
       {"pv_max": [["hf019", 3]], "traits_de": [["hf019", "RECRUITED"]]}),
    # ============================================================ hf019 Mirage (suite)
    _c("hf019 Mirage : son attaque de base est A DISTANCE -> Whiplash (Retaliate 1) ne riposte pas (seul le degat consequent : 1)",
       "« Mirage's basic attack gains ranged » : ranged ignore la Riposte ; Mirage (ATK 2) attaque Whiplash 01172 (Retaliate 1)",
       [HEROS, *en_jeu("hf019", "01172")], ["Puzzle.Attack('hf019')"], {"degats": [["01172", 2], ["hf019", 1]]}, cibles=["01172"], accepter_choix=True),
    _c("hf019 Mirage : TEMOIN, un allie SANS distance (Mockingbird 01083) prend la Riposte de Whiplash (1 + 1 consequent = 2)",
       "contre-cas : sans `ranged`, la Riposte s'applique", [HEROS, *en_jeu("01083", "01172")], ["Puzzle.Attack('01083')"],
       {"degats": [["01172", 1], ["01083", 2]]}, cibles=["01172"], accepter_choix=True),
    # ============================================================ hf025 Emma Frost
    _c("hf025 Emma Frost : apres avoir defendu, le dessus du deck est defausse ; un EVENEMENT (Swinging Web Kick, cout 3) est joue GRATUITEMENT -> 8 degats au vilain",
       "« After Emma Frost defends against an attack, discard 1 card from your deck, you may play it if it is an event, ignoring its resource cost » (⚠ le Spider-Sense de Spider-Man pioche le DESSUS avant la defense : on empile donc deux cartes)",
       [HEROS, *en_jeu("hf025"), "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01090', '01090', '01005', '01084')"], [f"Puzzle.Attack('{VILAIN}', defender='hf025')"],
       {"degats": [[VILAIN, 8]]}, cibles=[VILAIN], accepter_choix=True),
    _c("hf025 Emma Frost : CONTRE-CAS, la carte defaussee n'est pas un evenement (allie 01083) -> rien n'est joue",
       "seul un EVENEMENT peut etre joue", [HEROS, *en_jeu("hf025"), "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01090', '01090', '01083', '01084')"], [f"Puzzle.Attack('{VILAIN}', defender='hf025')"],
       {"degats": [[VILAIN, 0]], "defausse": ["01083"]}, cibles=[VILAIN], accepter_choix=True),
    _c("hf025 Emma Frost : Armored 1 -> l'attaque de Rhino (ATK 2) ne lui inflige que 1 degat (2 - 1 prevenu)",
       "« Armored 1 » : previent 1 des degats d'UNE ATTAQUE (si016 / 01098)", [HEROS, *en_jeu("hf025"), "Puzzle.MoveTo('01083', 'PlayerDeck')"],
       [f"Puzzle.Attack('{VILAIN}', defender='hf025')"], {"degats": [["hf025", 1]], "pv_max": [["hf025", 3]]}, accepter_choix=True),
    # ============================================================ hf026 Charles Xavier
    _c("hf026 Charles Xavier : en entrant en jeu, 1re branche : pioche 2 cartes",
       "« choose one: draw 2 cards, stun an enemy, or ready your identity » : main a 1 carte -> 3", [HEROS], en_jeu("hf026"),
       {"taille_main": 3}, main_exclusive=["01090"], preferer_option="Draw 2 cards", accepter_choix=True),
    _c("hf026 Charles Xavier : 2e branche : un ennemi est etourdi (pas de pioche)",
       "l'autre branche du choix", [HEROS], en_jeu("hf026"), {"statuts": [[VILAIN, "Stunned"]], "taille_main": 1},
       main_exclusive=["01090"], cibles=[VILAIN], preferer_option="Stun an enemy", accepter_choix=True),
    _c("hf026 Charles Xavier : a la fin du round il est defausse",
       "« At the end of the round, if Charles Xavier is still in play, discard him »", [HEROS, *en_jeu("hf026")], ["Puzzle.SendAfterRoundEnd()"],
       {"hors_jeu": ["hf026"]}),
    # ============================================================ hf027 Sebastian Shaw
    _c("hf027 Sebastian Shaw : apres avoir subi 2 degats, 2 compteurs d'energie",
       "« Response: After Sebastian Shaw is damaged, place an equal amount of energy counter here »", [HEROS, *en_jeu("hf027")],
       ["Puzzle.Damage('hf027', 2)"], {"compteurs": [["hf027", "energy", 2]]}, accepter_choix=True),
    _c("hf027 Sebastian Shaw : en contrant avec 2 compteurs, +2 CTR (1 + 2 = 3 menaces retirees) et il ne lui reste que le compteur du degat CONSEQUENT (1) : les 2 d'avant ont ete retires",
       "« [star] Interrupt: When Sebastian Shaw thwarts, remove each energy counter from him -> for each counter discarded this way, he gets +1 THW for this thwart »",
       [HEROS, "Puzzle.EmptyHand()", *en_jeu("hf027"), f"Puzzle.SetThreat('{COMPLOT}', 5)", "Puzzle.Counter('hf027', 'energy', 2)"],
       ["Puzzle.Thwart('hf027')"], {"menace": [[COMPLOT, 2]], "compteurs": [["hf027", "energy", 1]]}, cibles=[COMPLOT], accepter_choix=True),
    _c("hf027 Sebastian Shaw : TEMOIN, sans compteur il contre sa valeur imprimee (1)",
       "contre-cas : pas de compteur, pas de bonus", [HEROS, "Puzzle.EmptyHand()", *en_jeu("hf027"), f"Puzzle.SetThreat('{COMPLOT}', 5)"],
       ["Puzzle.Thwart('hf027')"], {"menace": [[COMPLOT, 4]]}, cibles=[COMPLOT], accepter_choix=True),
    # ============================================================ hf014 Blink
    _c("hf014 Blink : vaincue, elle est melangee dans le deck Recruited Mutants",
       "« Forced Response: When Blink is defeated, shuffle her into Recruited Mutant deck » : PV 2, 2 degats", [HEROS, *en_jeu("hf014")],
       ["Puzzle.Damage('hf014', 2)"], {"hf_recrutes_deck": ["hf014"], "hors_jeu": ["hf014"]}, accepter_choix=True),
    _c("hf014 Blink : TEMOIN, sans etre vaincue elle ne va pas dans le deck Recruited Mutants",
       "contre-cas", [HEROS, *en_jeu("hf014")], ["Puzzle.Damage('hf014', 1)"], {"hf_recrutes_deck": [], "en_jeu": ["hf014"]}, accepter_choix=True),
    # ============================================================ hf029-hf040 : les 12 POTENTIAL ALLY (« When Defeated : Allie » depuis la zone mise de cote)
]

# (carte, allie recrute, nom lisible) : numero de manigance, allie du dossier hf013-hf028
POTENTIELS = [("hf029", "hf013", "Shattered Confidence", "Armor"), ("hf030", "hf014", "Portal Trouble", "Blink"),
              ("hf031", "hf015", "Battle of the Bands", "Dazzler"), ("hf032", "hf016", "Secret Identity", "ForgetMeNot"),
              ("hf033", "hf017", "Morlock Rescue Mission", "Marrow"), ("hf034", "hf018", "Xavier's School Under Siege", "Glob Herman"),
              ("hf035", "hf019", "Astral Plane Showdown", "Mirage"), ("hf036", "hf020", "Crisis of Faith", "Oya"),
              ("hf037", "hf021", "Break The Prison", "Polaris"), ("hf038", "hf022", "Covert Intelligence Operation", "Sage"),
              ("hf039", "hf023", "Tech Glitch", "Wiz-Kid"), ("hf040", "hf024", "Muir Island Crisis", "Wolfsbane")]
for _manigance, _allie, _titre, _nom in POTENTIELS:
    CAS.append(_c(
        f"{_manigance} {_titre} : defaite par le heros -> {_nom} sort de la zone mise de cote et entre en jeu SOUS SON CONTROLE",
        f"« When Defeated: The player who defeat this scheme searches {_nom} from the set-aside area, put it into play under the player's control » : "
        f"menace a 1, le heros (CTR 1) la defait ; l'allie attendait de cote (`AsideScenario`)",
        [HEROS, "Puzzle.EmptyHand()", f"Puzzle.PutIntoPlay('{_manigance}')", f"Puzzle.SetThreat('{_manigance}', 1)",
         f"Puzzle.MoveTo('{_allie}', 'AsideScenario')"],
        ["Puzzle.Thwart('01001a')"], {"en_jeu": [_allie], "hors_jeu": [_manigance]}, cibles=[_manigance], accepter_choix=True))

CAS += [
    _c("hf029 Shattered Confidence : CONTRE-CAS, l'allie n'est pas de cote -> rien n'entre en jeu (pas d'erreur)",
       "la recherche echoue en silence", [HEROS, "Puzzle.EmptyHand()", "Puzzle.PutIntoPlay('hf029')", "Puzzle.SetThreat('hf029', 1)"],
       ["Puzzle.Thwart('01001a')"], {"hors_jeu": ["hf029", "hf013"]}, cibles=["hf029"], accepter_choix=True),
    _c("hf030 Portal Trouble : au debut de la phase du vilain, chaque joueur defausse 1 carte de sa main AU HASARD (2 -> 1)",
       "« Forced Response: When the villain phase begins, each player discard 1 card from hand in random »",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.PutIntoPlay('hf030')", "Puzzle.Gain('01088', '01089')"], ["Puzzle.BeginVillainPhase()"],
       {"taille_main": 1}),
    _c("hf033 Morlock Rescue Mission : en etant revelee, 1 menace par allie en jeu (2 allies -> 3 + 2 = 5)",
       "« When Revealed: Place 1 threat here for each ally in play »", [HEROS, "Puzzle.EmptyHand()", *en_jeu("01083", "01084")], ["Puzzle.Reveal('hf033')"],
       {"menace": [["hf033", 5]]}),
    _c("hf034 Xavier's School Under Siege : en etant revelee, le premier joueur met en jeu un sbire du deck de rencontre, engage avec lui",
       "« When Revealed: The first player searches the encounter deck and discard pile for a minion and puts it into play engaged with them »",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01098', '01098', '01101')"], ["Puzzle.Reveal('hf034')"],
       {"en_jeu": ["01101"], "dans_deck_rencontre": []}, accepter_choix=True),
    _c("hf036 Crisis of Faith : la menace d'une AUTRE manigance annexe ne peut plus etre retiree en contrant",
       "« Threat cannot be removed from other side scheme in play from thwarting » : 01108 Crowd Control (menace 2) reste a 2 quand le heros la contre",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.PutIntoPlay('hf036')", "Puzzle.PutIntoPlay('01108')", "Puzzle.SetThreat('01108', 2)"],
       ["Puzzle.Thwart('01001a')"], {"menace": [["01108", 2]]}, cibles=["01108"], accepter_choix=True),
    _c("hf036 Crisis of Faith : TEMOIN, sans elle la meme contrariete retire 1 menace (2 -> 1)",
       "contre-cas : la restriction vient de la carte", [HEROS, "Puzzle.EmptyHand()", "Puzzle.PutIntoPlay('01108')", "Puzzle.SetThreat('01108', 2)"],
       ["Puzzle.Thwart('01001a')"], {"menace": [["01108", 1]]}, cibles=["01108"], accepter_choix=True),
    _c("hf037 Break The Prison : en boost, apres l'activation du vilain, elle est REVELEE (entre en jeu)",
       "« [star] Boost: After this activation, reveal this card » : Rhino attaque avec hf037 en boost", [HEROS, f"Puzzle.GiveFacedownBoost('{VILAIN}', 'hf037')"],
       [f"Puzzle.Attack('{VILAIN}')"], {"en_jeu": ["hf037"]}, accepter_choix=True),
    _c("hf038 Covert Intelligence Operation : chaque sbire gagne Incite 1",
       "« Each minion gains incite 1 »", [HEROS, *en_jeu("hf038", "01101")], [], {"hf_keyword": [["01101", "Incite", 1]]}),
    _c("hf040 Muir Island Crisis : apres la phase du vilain, 1 degat a chaque HEROS (forme heros) ; un joueur en alter ego n'en prend pas",
       "« Forced Response: After the villain phase ends, deal 1 damage to each hero in player order »", [HEROS, "Puzzle.PutIntoPlay('hf040')"],
       ["Puzzle.EndVillainPhase()"], {"degats_identite": 1}),
    _c("hf040 Muir Island Crisis : TEMOIN, en alter ego le joueur ne prend rien",
       "« each HERO »", ["Puzzle.PutIntoPlay('hf040')"], ["Puzzle.EndVillainPhase()"], {"degats_identite": 0}),
    # ============================================================ hf041-hf047 : manigances de campagne
    _c("hf041 Cerebro Insights : defaite -> cherche une POTENTIAL ALLY dans le deck de rencontre, la met en jeu puis la defait (l'allie sort de cote)",
       "« When Defeated: ... searches the encounter deck and discard pile for a POTENTIAL ALLY side scheme and put it into play. They choose a POTENTIAL ALLY side scheme in play, then defeat it »",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.PutIntoPlay('hf041')", "Puzzle.SetThreat('hf041', 1)", "Puzzle.EmptyEncounterDeck()",
        "Puzzle.CreateEncounterDeck('01098', 'hf029')", "Puzzle.MoveTo('hf013', 'AsideScenario')"], ["Puzzle.Thwart('01001a')"],
       {"en_jeu": ["hf013"], "hors_jeu": ["hf041", "hf029"]}, cibles=["hf041", "hf029"], accepter_choix=True),
    _c("hf042 Emma Frost's Redemption : defaite -> l'allie Emma Frost entre en jeu", "« searches the Emma Frost ally from the set-aside area »",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.PutIntoPlay('hf042')", "Puzzle.SetThreat('hf042', 1)", "Puzzle.MoveTo('hf025', 'AsideScenario')"],
       ["Puzzle.Thwart('01001a')"], {"en_jeu": ["hf025"], "hors_jeu": ["hf042"]}, cibles=["hf042"], accepter_choix=True),
    _c("hf043 Cryptic Threatening Message : defaite -> l'allie Charles Xavier entre en jeu", "« searches the Charles Xavier ally from the set-aside area »",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.PutIntoPlay('hf043')", "Puzzle.SetThreat('hf043', 1)", "Puzzle.MoveTo('hf026', 'AsideScenario')"],
       ["Puzzle.Thwart('01001a')"], {"en_jeu": ["hf026"], "hors_jeu": ["hf043"]}, cibles=["hf043"], accepter_choix=True),
    _c("hf044 Psychic Minefield : la derniere menace ne peut pas etre retiree (2 menaces, contre de 2 -> reste 1)",
       "« Threat cannot be removed from here while there is only 1 threat here »",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.PutIntoPlay('hf044')", "Puzzle.SetThreat('hf044', 2)", "Puzzle.Counter('01001a', 'counter', 0)"],
       ["Puzzle.Thwart('01001a')", "Puzzle.Thwart('01001a')"], {"menace": [["hf044", 1]]}, cibles=["hf044", "hf044"], accepter_choix=True),
    _c("hf045 Rally the Survivors : defaite -> prend une carte du deck Recruited Mutants (en jeu sous son controle) puis, s'il en reste, 5 menaces ici",
       "« takes a card from the Recruited Mutants deck and put it into play under their control. Then, if there still has card in the deck, place 5 threat here »",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.PutIntoPlay('hf045')", "Puzzle.SetThreat('hf045', 1)", "Puzzle.PutIntoRecruitedMutants('hf013', 'hf015')"],
       ["Puzzle.Thwart('01001a')"], {"hf_recrutes_taille": 1, "menace": [["hf045", 5]]}, cibles=["hf045"], accepter_choix=True),
    _c("hf046 Tactical Help : en boost, elle est revelee et recoit 2 menaces de plus (3 + 2 = 5)",
       "« [star] Boost: Reveal this card. Place 2 additional threat here »", [HEROS, "Puzzle.EmptyHand()", f"Puzzle.GiveFacedownBoost('{VILAIN}', 'hf046')"],
       [f"Puzzle.Attack('{VILAIN}')"], {"en_jeu": ["hf046"], "menace": [["hf046", 5]]}, accepter_choix=True),
    _c("hf046 Tactical Help : defaite -> Sebastian Shaw entre en jeu", "« searches Sebastian Shaw from the set-aside area »",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.PutIntoPlay('hf046')", "Puzzle.SetThreat('hf046', 1)", "Puzzle.MoveTo('hf027', 'AsideScenario')"],
       ["Puzzle.Thwart('01001a')"], {"en_jeu": ["hf027"], "hors_jeu": ["hf046"]}, cibles=["hf046"], accepter_choix=True),
    _c("hf047 Enemy Of Enemy : en boost, elle est revelee et le joueur est desoriente",
       "« [star] Boost: Reveal this card. You are confused »", [HEROS, f"Puzzle.GiveFacedownBoost('{VILAIN}', 'hf047')"],
       [f"Puzzle.Attack('{VILAIN}')"], {"en_jeu": ["hf047"], "statuts": [["01001a", "Confused"]]}, accepter_choix=True),
    _c("hf047 Enemy Of Enemy : defaite -> Selene entre en jeu", "« searches Selene from the set-aside area »",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.PutIntoPlay('hf047')", "Puzzle.SetThreat('hf047', 1)", "Puzzle.MoveTo('hf028', 'AsideScenario')"],
       ["Puzzle.Thwart('01001a')"], {"en_jeu": ["hf028"], "hors_jeu": ["hf047"]}, cibles=["hf047"], accepter_choix=True),
    # ============================================================ hf048 Xavier's Institute
    _c("hf048 Xavier's Institute : Action, depense 1 ressource -> pioche 1 carte du deck Recruited Mutants (Armor entre en main)",
       "« Action: Spend 1 resource of any type -> draw 1 card from the Recruited Mutants deck »",
       [HEROS, "Puzzle.PutIntoPlay('hf048')", "Puzzle.PutIntoRecruitedMutants('hf013')"], ["Puzzle.Action('hf048')"],
       {"en_main": ["hf013"], "hf_recrutes_deck": []}, main_exclusive=["01090"], payer_avec=["01090"], accepter_choix=True),
    _c("hf048 Xavier's Institute : un allie RECRUITED defausse va dans la defausse Recruited Mutants (pas dans celle du joueur)",
       "« Forced Response: After a RECRUITED ally is discarded, place it into the Recruited Mutants discard pile instead » : ForgetMeNot se defausse en fin de round",
       [HEROS, "Puzzle.PutIntoPlay('hf048')", *en_jeu("hf016")], ["Puzzle.SendAfterRoundEnd()"],
       {"hf_recrutes_defausse": ["hf016"], "hors_jeu": ["hf016"], "defausse": []}),
    # ============================================================ hf014 Blink (suite : depuis la defausse Recruited)
    _c("hf014 Blink : elle peut etre JOUEE depuis la defausse Recruited Mutants pendant son tour (cout 3 paye)",
       "« Any of the players may play Blink from Recruited Mutant discard pile during their own turn (paying its resource cost) »",
       [HEROS, "Puzzle.PutIntoPlay('hf048')", "Puzzle.PutIntoRecruitedMutants('hf014', discard=True)"], ["Puzzle.PlayFromRecruitedDiscard('hf014')"],
       {"en_jeu": ["hf014"], "hf_recrutes_defausse": []}, main_exclusive=["01088", "01090"], payer_avec=["01088", "01090"], accepter_choix=True),
    # ============================================================ hf001-hf009 : cartes d'aspect de Marvel Girl
    _c("hf001 Boom Boom : maximum 5 compteurs (5 + 1 -> reste 5) : detonation = 2 x 5 = 10 degats, pas 12",
       "« (to a maximum of 5) » : le pilote accepte la detonation, le degat mesure le nombre de compteurs",
       [HEROS, *en_jeu("hf001"), "Puzzle.Counter('hf001', 'boom', 5)"], ["Puzzle.BeginPlayerTurn()"],
       {"degats": [[VILAIN, 10]], "hors_jeu": ["hf001"]}, cibles=[VILAIN], accepter_choix=True),
    _c("hf001 Boom Boom : en la defaussant (3 compteurs apres le nouveau) -> 6 degats au vilain",
       "« you may discard Boom Boom to deal 2 damage to the villain for each boom counter » : 2 + 1 = 3 compteurs, 2 x 3 = 6",
       [HEROS, *en_jeu("hf001"), "Puzzle.Counter('hf001', 'boom', 2)"], ["Puzzle.BeginPlayerTurn()"],
       {"degats": [[VILAIN, 6]], "hors_jeu": ["hf001"]}, cibles=[VILAIN], accepter_choix=True),
    _c("hf002 Captain Britain (Brian) : au debut du tour, cherche un allie dans les 5 cartes du dessus du deck et l'ajoute a la main",
       "« Response: After your turn begins, search the top 5 cards of your deck for an ally card and add it to your hand »",
       [HEROS, *en_jeu("hf002"), "Puzzle.EmptyHand()", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01090', '01090', '01090', '01090', '01084', '01090', '01090')"],
       ["Puzzle.BeginPlayerTurn()"], {"en_main": ["01084"]}, accepter_choix=True),
    _c("hf002 Captain Britain (Brian) : CONTRE-CAS, l'allie est SOUS les 5 cartes du dessus (6e) -> pas trouve",
       "la recherche ne regarde que les 5 premieres", [HEROS, *en_jeu("hf002"), "Puzzle.EmptyHand()", "Puzzle.EmptyPlayerDeck()",
       "Puzzle.CreatePlayerDeck('01084', '01090', '01090', '01090', '01090', '01090', '01090')"],
       ["Puzzle.BeginPlayerTurn()"], {"absent_main": ["01084"]}, accepter_choix=True),
    _c("hf003 PAC-RAT II : au debut du tour, +1 compteur time", "« Response: After your turn begins, place 1 time counter »", [HEROS, *en_jeu("hf003")],
       ["Puzzle.BeginPlayerTurn()"], {"compteurs": [["hf003", "time", 1]]}),
    _c("hf003 PAC-RAT II : Action, 4 compteurs -> met en jeu UN allie X-FORCE de cout 4 (le second ne rentre pas), puis PAC-RAT est defaussee",
       "« Put up to two X-FORCE allies from your hand into play with total printed cost equal to or less than the number of time counters »",
       [HEROS, *en_jeu("hf003"), "Puzzle.Counter('hf003', 'time', 4)", "Puzzle.Gain('hf001')", "Puzzle.Gain('hf006')"], ["Puzzle.Action('hf003')"],
       {"en_jeu": ["hf001"], "hors_jeu": ["hf003", "hf006"], "en_main": ["hf006"]}, accepter_choix=True),
    _c("hf003 PAC-RAT II : Action, 8 compteurs -> met en jeu les DEUX allies X-FORCE (4 + 4)", "la borne « total printed cost <= compteurs »",
       [HEROS, *en_jeu("hf003"), "Puzzle.Counter('hf003', 'time', 8)", "Puzzle.Gain('hf001')", "Puzzle.Gain('hf006')"], ["Puzzle.Action('hf003')"],
       {"en_jeu": ["hf001", "hf006"], "hors_jeu": ["hf003"]}, accepter_choix=True),
    _c("hf004 Divided We Fall : 1re carte du round -> soigne 1 degat a 2 personnages ET leur donne Tough",
       "« Heal 1 damage from up to 2 friendly characters, If this is the first card you have played this round, give those characters a tough status card »",
       [HEROS, *en_jeu("01083"), "Puzzle.Damage('01001a', 2)", "Puzzle.Damage('01083', 1)", "Puzzle.Gain('hf004')"], [],
       {"degats": [["01083", 0]], "degats_identite": 1, "statuts": [["01083", "Tough"], ["01001a", "Tough"]]},
       main_exclusive=["hf004", "01090"], payer_avec=["01090"], jouer=["hf004"], cibles=["01001a", "01083"], accepter_choix=True),
    _c("hf005 First Command : redresse un allie et lui donne +1 CTR et +1 ATK pour la phase",
       "« Hero Action: Ready an ally. That ally gets +1 THW and +1 ATK this phase »", [HEROS, *en_jeu("01083"), "Puzzle.Exhaust('01083')"], [],
       {"pret": ["01083"], "attributs_carte": [["01083", "attack", 1], ["01083", "thwart", 1]]},
       main_exclusive=["hf005", "01090"], payer_avec=["01090"], jouer=["hf005"], cibles=["01083"], accepter_choix=True),
    _c("hf006 White Phoenix : gagne chaque TRAIT de l'identite (Spider-Man : AVENGER)", "« White Phoenix gains each TRAIT on your identity »",
       [HEROS, *en_jeu("hf006")], [], {"traits_de": [["hf006", "AVENGER"], ["hf006", "PSIONIC"]]}),
    _c("hf006 White Phoenix : quand elle quitte le jeu, cherche un EVENEMENT dans la defausse et l'ajoute a la main",
       "« Interrupt: When White Phoenix leaves play, search your discard pile for an event card and add it to your hand » : 01005 en defausse, hf006 (PV 3) vaincue",
       [HEROS, *en_jeu("hf006"), "Puzzle.EmptyHand()", "Puzzle.MoveTo('01005', 'DiscardPile')"], ["Puzzle.Damage('hf006', 3)"],
       {"hors_jeu": ["hf006"], "en_main": ["01005"]}, accepter_choix=True),
    _c("hf007 Jump-Start : au debut du tour, 1 degat au personnage porteur -> 1 compteur power",
       "« Response: After your turn begins, deal 1 damage to attached character -> place 1 power counter here »",
       [HEROS, "Puzzle.PutIntoPlay('hf007')", "Puzzle.Attach('hf007', '01001a')"], ["Puzzle.BeginPlayerTurn()"],
       {"compteurs": [["hf007", "power", 1]], "degats_identite": 1}, accepter_choix=True),
    _c("hf007 Jump-Start : avec 1 compteur, l'attaque de base du porteur fait +1 (2 + 1 = 3 degats) et le compteur est retire",
       "« Interrupt: When attached character makes a basic ... attack, remove 1 power counter from here -> +1 ATK for that action »",
       [HEROS, "Puzzle.PutIntoPlay('hf007')", "Puzzle.Attach('hf007', '01001a')", "Puzzle.Counter('hf007', 'power', 1)"], ["Puzzle.Attack('01001a')"],
       {"degats": [[VILAIN, 3]], "compteurs": [["hf007", "power", 0]]}, cibles=[VILAIN], accepter_choix=True),
    _c("hf007 Jump-Start : TEMOIN, sans compteur l'attaque de base fait 2",
       "contre-cas : le bonus coute un compteur", [HEROS, "Puzzle.PutIntoPlay('hf007')", "Puzzle.Attach('hf007', '01001a')"], ["Puzzle.Attack('01001a')"],
       {"degats": [[VILAIN, 2]]}, cibles=[VILAIN], accepter_choix=True),
    _c("hf008 Psionic Soulmates : Team-Up satisfait (Betsy Braddock = Captain Britain rm002 + Rachel Summers), apres avoir joue une carte PSIONIC (White Phoenix) : la remelange dans le deck, s'incline, pioche 1",
       "« Response: After you play a PSIONIC card, shuffle that card into your deck and exhaust this card -> draw 1 card »",
       ["Puzzle.ChangeToFace('rm001b', 'rm001a')", *en_jeu("hf008", "rm002"), "Puzzle.Gain('hf006')"], [],
       {"exhausted": ["hf008"], "hors_jeu": ["hf006"], "dans_deck_joueur": ["hf006"]}, heros="rachel_summers",
       main_exclusive=["hf006", "01088", "01089"], payer_avec=["01088", "01089"], jouer=["hf006"], accepter_choix=True),
    _c("hf008 Psionic Soulmates : CONTRE-CAS, Team-Up NON satisfait (Spider-Man, ni Betsy ni Rachel) -> aucune Response : White Phoenix reste en jeu",
       "Team-Up (Betsy Braddock and Rachel Summers)", [HEROS, *en_jeu("hf008"), "Puzzle.Gain('hf006')"], [],
       {"pret": ["hf008"], "en_jeu": ["hf006"]}, main_exclusive=["hf006", "01088", "01089"], payer_avec=["01088", "01089"], jouer=["hf006"], accepter_choix=True),
    _c("hf009 From The Ashes : paie a elle seule une carte de cout 2 (Haymaker) car elle compte double pour la PREMIERE carte du tour",
       "« This card doubles the number of resources it generates while paying for the first card you play in your turn »",
       [HEROS, "Puzzle.Gain('hf009', '01087')"], [], {"defausse": ["01087"]},
       main_exclusive=["hf009", "01087"], payer_avec=["hf009"], jouer=["01087"], cibles=[VILAIN], accepter_choix=True),
    # ============================================================ campaign.py : mise en place commune et releve du carnet
    _c("campagne scenario 1 : les 16 allies sont mis de cote, le deck Recruited Mutants est vide, 1 manigance POTENTIAL ALLY (1 joueur) est melangee au deck de rencontre, Cerebro Insights revele et Xavier's Institute en jeu",
       "livret p.5 et scenario 1 : « set aside the 16 Recruited allies ; shuffle 1 Potential Ally per player into the encounter deck ; reveal Cerebro Insights ; put Xavier's Institute into play »",
       [HEROS, "Puzzle.EmptyHand()"], ["Puzzle.HellfireCampagne(1)"],
       {"hf_recrutes_taille": 0, "hf_mis_de_cote": 16, "hf_pa_dans_rencontre": 1, "en_jeu": ["hf041", "hf048"]}),
    _c("campagne scenario 1 : un carnet qui note deux allies gagnes (Armor, Blink) -> ils forment le deck Recruited Mutants, les 14 autres restent de cote",
       "« Recruited Allies » du carnet -> deck Recruited Mutants", [HEROS, "Puzzle.EmptyHand()"],
       ["Puzzle.HellfireCampagne(1, {'Recruited Allies': 'hf013;hf014'})"],
       {"hf_recrutes_deck": ["hf013", "hf014"], "hf_mis_de_cote": 14}),
    _c("campagne scenario 2 : une seule manigance POTENTIAL ALLY n'est pas retiree (hf030) -> c'est elle que le joueur recoit dans le deck de rencontre",
       "« Removed Potential Allies » du carnet : les manigances vaincues quittent la campagne",
       [HEROS, "Puzzle.EmptyHand()"],
       ["Puzzle.HellfireCampagne(2, {'Removed Potential Allies': 'hf029;hf031;hf032;hf033;hf034;hf035;hf036;hf037;hf038;hf039;hf040'})"],
       {"hf_pa_ids_dans_rencontre": ["hf030"]}),
    _c("campagne scenario 3 : Emma Frost's Redemption non cochee -> elle est revelee",
       "livret scenario 3 : « if Emma Frost's Redemption is not checked, reveal it »", [HEROS, "Puzzle.EmptyHand()"], ["Puzzle.HellfireCampagne(3)"],
       {"en_jeu": ["hf042", "hf048"], "hors_jeu": ["hf043"]}),
    _c("campagne scenario 3 : Emma Frost's Redemption cochee -> Emma Frost rejoint le deck Recruited Mutants et Cryptic Threatening Message est revelee",
       "livret scenario 3 : « otherwise shuffle Emma Frost into the Recruited Mutants deck and reveal Cryptic Threatening Message »", [HEROS, "Puzzle.EmptyHand()"],
       ["Puzzle.HellfireCampagne(3, {\"Emma Frost's Redemption: Defeated\": '1'})"],
       {"en_jeu": ["hf043"], "hors_jeu": ["hf042"], "hf_recrutes_deck": ["hf025"]}),
    _c("campagne scenario 5 : Tactical Help et Enemy Of Enemy melanges dans le deck de rencontre, Rally the Survivors revelee, PAS de Xavier's Institute, Emma dans le deck Recruited",
       "livret scenario 5 : « shuffle Tactical Help and Enemy of Enemy into the encounter deck ; reveal Rally the Survivors ; remove Xavier's Institute ; Emma Frost's Redemption not checked -> shuffle Emma Frost into the Recruited Mutants deck »",
       [HEROS, "Puzzle.EmptyHand()"], ["Puzzle.HellfireCampagne(5)"],
       {"en_jeu": ["hf045"], "hors_jeu": ["hf048"], "hf_recrutes_deck": ["hf025"], "hf_ids_dans_rencontre": ["hf046", "hf047"]}),
    _c("campagne releve : a la victoire, les allies Recruited en jeu sont notes et la manigance POTENTIAL ALLY vaincue est retiree de la campagne",
       "carnet sortant : `Recruited Allies`, `Removed Potential Allies`",
       [HEROS, *en_jeu("hf013"), "Puzzle.PutIntoPlay('hf029')", "Puzzle.MoveTo('hf029', 'VictoryDisplay')"], ["Puzzle.HellfireReleve(1, True)"],
       {"hf_releve": {"Recruited Allies": "hf013", "Removed Potential Allies": "hf029"}}),
    _c("campagne releve : a la DEFAITE rien n'est note (on rejoue sans penalite)",
       "livret p.5 : « defeat : replay without penalty »", [HEROS, *en_jeu("hf013")], ["Puzzle.HellfireReleve(1, False)"], {"hf_releve": {}}),
]


VERIFICATIONS = r'''
def hf_etat(monde, aides):
    """Cles propres : `hf_recrutes_deck` / `hf_recrutes_defausse` (liste EXACTE des card_id du deck / de la defausse Recruited Mutants, dans
    n'importe quel ordre) ; le reste va a etat_attendu."""
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    soucis = []
    etat = getattr(monde, "hf_recruited", None)
    deck_ids = sorted(getattr(f.paper, "card_id", None) for f in etat[0].Get(True)) if etat else []
    defausse_ids = sorted(getattr(f.paper, "card_id", None) for f in etat[1].Get(True)) if etat else []
    if "hf_recrutes_deck" in attendu and deck_ids != sorted(attendu["hf_recrutes_deck"]):
        soucis.append(f"deck Recruited Mutants = {deck_ids} (attendu {sorted(attendu['hf_recrutes_deck'])})")
    if "hf_recrutes_defausse" in attendu and defausse_ids != sorted(attendu["hf_recrutes_defausse"]):
        soucis.append(f"defausse Recruited Mutants = {defausse_ids} (attendu {sorted(attendu['hf_recrutes_defausse'])})")
    if "hf_recrutes_taille" in attendu:
        n = len(deck_ids)
        if n != attendu["hf_recrutes_taille"]:
            soucis.append(f"deck Recruited Mutants = {n} carte(s) (attendu {attendu['hf_recrutes_taille']})")
    for card_id, mot, valeur in attendu.get("hf_keyword") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu (hf_keyword)")
        elif face.GetKeyword(mot) != valeur:
            soucis.append(f"{card_id} : {mot} = {face.GetKeyword(mot)} (attendu {valeur})")
    from game.operate.worlds import Worlds
    ids_rencontre = sorted(getattr(f.paper, "card_id", None) for f in Worlds.GetEncounterDeckCards(monde))
    potentiels = [i for i in ids_rencontre if i and i.startswith("hf") and 29 <= int(i[2:5]) <= 40]
    if "hf_mis_de_cote" in attendu:
        de_cote = [f for f in monde.aside_deck.Get(True) if getattr(f.paper, "card_id", None) in [f"hf{n:03d}" for n in range(13, 29)]]
        if len(de_cote) != attendu["hf_mis_de_cote"]:
            soucis.append(f"{len(de_cote)} allie(s) Recruited de cote (attendu {attendu['hf_mis_de_cote']})")
    if "hf_pa_dans_rencontre" in attendu and len(potentiels) != attendu["hf_pa_dans_rencontre"]:
        soucis.append(f"{len(potentiels)} manigance(s) POTENTIAL ALLY dans le deck de rencontre (attendu {attendu['hf_pa_dans_rencontre']}) : {potentiels}")
    if "hf_pa_ids_dans_rencontre" in attendu and potentiels != sorted(attendu["hf_pa_ids_dans_rencontre"]):
        soucis.append(f"POTENTIAL ALLY du deck de rencontre = {potentiels} (attendu {sorted(attendu['hf_pa_ids_dans_rencontre'])})")
    for card_id in attendu.get("hf_ids_dans_rencontre") or []:
        if card_id not in ids_rencontre:
            soucis.append(f"{card_id} n'est pas dans le deck de rencontre")
    if "hf_releve" in attendu:
        releve = getattr(monde, "hf_releve", None)
        if releve is None:
            soucis.append("aucun releve de campagne calcule")
        elif attendu["hf_releve"] == {}:
            if releve:
                soucis.append(f"un releve est ecrit alors que la partie est PERDUE : {releve}")
        else:
            for cle, valeur in attendu["hf_releve"].items():
                if releve.get(cle) != valeur:
                    soucis.append(f"releve[{cle!r}] = {releve.get(cle)!r} (attendu {valeur!r})")
    propres = ("hf_recrutes_deck", "hf_recrutes_defausse", "hf_recrutes_taille", "hf_keyword", "hf_mis_de_cote", "hf_pa_dans_rencontre",
               "hf_pa_ids_dans_rencontre", "hf_ids_dans_rencontre", "hf_releve")
    reste = {k: v for k, v in attendu.items() if k not in propres}
    copie = dict(aides); copie["cas"] = dict(cas); copie["cas"]["attendu"] = reste
    ok, message = etat_attendu(monde, copie)
    if not ok:
        soucis.append(message)
    if soucis:
        return False, " ; ".join(soucis)
    return True, message
'''
