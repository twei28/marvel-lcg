# Cas test_capacites de l'aspect TMNT Protection (Inkwire, pack tmnt_aspect_protection, prefixe up).
# Filtre : `[up]`. Gabarits : .planning/tmnt/aspects-protection-gabarits.md.
#
# Conventions (reprises de tools/cas/rampage.py) :
#  - Spider-Man (01001) demarre en ALTER EGO ; HEROS le met en forme heros (10 PV, ATQ 2, CTR 1, DEF 3) ;
#  - Rhino 01094 (14 PV, ATQ 2) ; complot principal 01097b ; 01101 Hydra Mercenary (sbire, 3 PV) ;
#  - ressources : 01090 Strength = RR, 01088 Energy = YY, 01089 Genius = BB ;
#  - chaque reskin IDENTIQUE a son cas TEMOIN sur l'officielle, meme montage, meme chiffre attendu.
SC = "rhino"
HEROS = "Puzzle.ChangeForm('01001b')"
SANS_DECK = "Puzzle.EmptyPlayerDeck()"
DECK6 = "Puzzle.CreatePlayerDeck('01089', '01089', '01089', '01089', '01089', '01089')"
SBIRE = "Puzzle.PutIntoPlay('01101')"


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[up] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": list(mise), "declencher": list(declencher),
           "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.update(cle)
    return cas


def _paire(up, officielle, nom, pourquoi, mise, declencher, attendu, **cle):
    """Un cas sur le reskin `up` et son TEMOIN identique sur l'officielle (card_id remplace partout)."""
    def sub(x):
        if isinstance(x, str):
            return x.replace(up, officielle)
        if isinstance(x, list):
            return [sub(y) for y in x]
        if isinstance(x, dict):
            return {k: sub(v) for k, v in x.items()}
        return x
    return [
        _c(f"{up} {nom}", pourquoi, mise, declencher, attendu, **cle),
        _c(f"{up} TEMOIN {officielle} (officielle) : {nom}", "meme montage sur l'officielle, meme chiffre attendu",
           sub(mise), sub(declencher), sub(attendu), **{k: sub(v) for k, v in cle.items()}),
    ]


def _unique(up, bandeau_id, bandeau):
    """Q-R1 (16/10/2026) : l'unicite se juge aussi sur le titre du bandeau (`unique_also`)."""
    return [
        _c(f"{up} unicite : {bandeau} ({bandeau_id}) en jeu -> {up} n'est PAS jouable (bandeau « {bandeau} »)",
           "decision Q-R1 : le bandeau imprime sous le titre compte pour l'unicite (`unique_also`)",
           [HEROS, f"Puzzle.Gain('{up}')", f"Puzzle.PutIntoPlay('{bandeau_id}', under_control=True)"], [],
           {"carte": up, "jouable": False, "en_jeu": 0},
           main=["01088", "01089", "01090", "01088"], verifier="max_par_joueur_jouable"),
        _c(f"{up} unicite : TEMOIN, sans {bandeau} en jeu, {up} est jouable",
           "contre-cas : c'est bien la copie au titre du bandeau qui bloque",
           [HEROS, f"Puzzle.Gain('{up}')"], [],
           {"carte": up, "jouable": True, "en_jeu": 0},
           main=["01088", "01089", "01090", "01088"], verifier="max_par_joueur_jouable"),
    ]


CAS = []

# ===================================================================== IDENTIQUES (ability_link)
CAS += _paire("up001", "09012", "Ace Duck : Reponse a l'entree en jeu, l'evenement des 5 du dessus va en main",
              "« search the top 5 cards of your deck for an event card and add it to your hand » : deck Genius x5 + "
              "Powerful Punch 32014 en 3e position",
              [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01089', '01089', '32014', '01089', '01089', '01089')"], [],
              {"en_jeu": ["up001"], "en_main": ["32014"]},
              main_exclusive=["up001", "01090", "01088"], jouer=["up001"], accepter_choix=True)
CAS += _unique("up001", "09012", "Brother Voodoo")

CAS += _paire("up002", "01081", "Armored Vest : +1 DEF au heros",
              "« Your hero gets +1 DEF »", [HEROS], [],
              {"en_jeu": ["up002"], "attributs": {"defense": 1}},
              main_exclusive=["up002", "01090"], jouer=["up002"])

CAS += _paire("up003", "60048", "Army of One : redresse le heros",
              "« Hero Action: Ready your hero » ; aucun allie : cout 1",
              [HEROS, "Puzzle.Exhaust('01001a')"], [],
              {"pret": ["01001a"], "defausse": ["up003"]},
              main_exclusive=["up003", "01090"], jouer=["up003"])
CAS += _paire("up003", "60048", "Army of One : 2 allies controles -> cout 3, injouable avec 2 ressources",
              "« [star] Increase the cost to play this card by 1 for each ally you control » : 1 + 2 = 3 > 2",
              [HEROS, "Puzzle.Exhaust('01001a')", "Puzzle.PutIntoPlay('01059', under_control=True)",
               "Puzzle.PutIntoPlay('09012', under_control=True)"], [],
              {"en_main": ["up003"], "exhausted": ["01001a"]},
              main_exclusive=["up003", "01090"], jouer=["up003"])

CAS += _paire("up005", "48014", "Change of Fortune : sbire vaincu par le heros en phase du vilain -> incline, pioche 2",
              "« After you defeat an enemy during the villain phase, exhaust this card -> draw 2 cards »",
              [HEROS, SANS_DECK, DECK6, "Puzzle.PutIntoPlay('up005', under_control=True)",
               "Puzzle.Damage(Puzzle.PutIntoPlay('01101'), 2)"],
              ["Puzzle.BeginVillainPhase()", "Puzzle.Attack('01001a')"],
              {"hors_jeu": ["01101"], "exhausted": ["up005"], "taille_main": 3},
              main_exclusive=["01090"], cibles=["01101"], accepter_choix=True)
CAS += _paire("up005", "48014", "Change of Fortune : meme defaite en phase des JOUEURS -> rien",
              "contre-cas « during the villain phase »",
              [HEROS, SANS_DECK, DECK6, "Puzzle.PutIntoPlay('up005', under_control=True)",
               "Puzzle.Damage(Puzzle.PutIntoPlay('01101'), 2)"],
              ["Puzzle.Attack('01001a')"],
              {"hors_jeu": ["01101"], "pret": ["up005"], "taille_main": 1},
              main_exclusive=["01090"], cibles=["01101"], accepter_choix=True)

CAS += _paire("up006", "48016", "\"Come Get Me, Bub!\" : sbire defausse du deck rencontre mis en jeu engage, soin 3 + Tenace",
              "« Discard cards from the encounter deck until you discard a minion. Put that minion into play engaged "
              "with you -> heal 3 damage from your identity and give your identity a tough status card »",
              [HEROS, "Puzzle.Damage('01001a', 4)", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101')"], [],
              {"en_jeu": ["01101"], "degats_identite": 1, "statuts": [["01001a", "Tough"]]},
              main_exclusive=["up006"], jouer=["up006"])

CAS += _paire("up008", "56046", "Defensive Conditioning : +1 DEF au heros",
              "« You get +3 hit points and your hero gets +1 DEF »", [HEROS], [],
              {"en_jeu": ["up008"], "attributs": {"defense": 1}},
              main_exclusive=["up008", "01090"], jouer=["up008"])

CAS += _paire("up010", "10031", "Electrostatic Armor : apres une defense, 1 degat a l'attaquant",
              "« After you defend against an attack, deal 1 damage to the attacking character »",
              [HEROS, "Puzzle.PutIntoPlay('up010', under_control=True)"], ["Puzzle.Attack('01094', defender='01001a')"],
              {"degats": [["01094", 1]], "degats_identite": 0},
              main_exclusive=["01090"], accepter_choix=True)

CAS += _paire("up011", "05017", "Energy Barrier : previent 1, 1 degat a un ennemi, 1 compteur retire",
              "« remove 1 reflection counter from here -> prevent 1 of that damage and deal 1 damage to an enemy »",
              [HEROS, "Puzzle.PutIntoPlay('up011', under_control=True)", "Puzzle.Exhaust('01001a')"], ["Puzzle.Attack('01094')"],
              {"degats_identite": 1, "degats": [["01094", 1]], "compteurs": [["up011", "reflection", 2]]},
              main_exclusive=["01090"], accepter_choix=True)

CAS += _paire("up012", "60049", "Get Their Attention : quand un ennemi attaque, 3 menaces retirees",
              "« When an enemy initiates an attack, remove 3 threat from a scheme »",
              [HEROS], ["Puzzle.SetThreat('01097b', 5)", "Puzzle.Attack('01094')"],
              {"menace": [["01097b", 2]], "defausse": ["up012"]},
              main_exclusive=["up012", "01089"], cibles=["01097b"])

CAS += _paire("up017", "56041", "Honor Blade : apres que vous engagez un sbire, Tenace",
              "« After you engage a minion, give Honor Blade a tough status card »",
              [HEROS, "Puzzle.PutIntoPlay('up017', under_control=True)"], ["Puzzle.Reveal('01101')"],
              {"statuts": [["up017", "Tough"]]},
              main_exclusive=["01090"], accepter_choix=True)
CAS += _unique("up017", "56041", "Patriot")

CAS += _paire("up018", "56047", "\"I Can Do This All Day\" : heros incline declare defenseur sans s'incliner (0 degat)",
              "lu comme l'officielle (Hero INTERRUPT, question ouverte sur « Hero Action ») : DEF 3 contre ATQ 2",
              [HEROS, "Puzzle.Exhaust('01001a')"], ["Puzzle.Attack('01094')"],
              {"degats_identite": 0, "defausse": ["up018"], "exhausted": ["01001a"]},
              main_exclusive=["up018", "01089"])

CAS += _paire("up019", "60050", "In Harm's Way : X = DEF 3 degats a Rhino et 3 menaces retirees",
              "« Deal X damage to an enemy and remove X threat from a scheme, where X is your DEF »",
              [HEROS], ["Puzzle.SetThreat('01097b', 5)"],
              {"degats": [["01094", 3]], "menace": [["01097b", 2]]},
              main_exclusive=["up019", "01090", "01088"], jouer=["up019"], cibles=["01094", "01097b"])

CAS += _paire("up020", "60038", "Innate Reflexes : +1 DEF au heros",
              "« Your hero gets +1 DEF »", [HEROS], [],
              {"en_jeu": ["up020"], "attributs": {"defense": 1}},
              main_exclusive=["up020", "01090"], jouer=["up020"])

CAS += _paire("up025", "32014", "Powerful Punch : quand Rhino attaque, 4 degats a Rhino",
              "« When an enemy initiates an attack, deal 4 damage to that enemy »",
              [HEROS], ["Puzzle.Attack('01094')"],
              {"degats": [["01094", 4]], "defausse": ["up025"]},
              main_exclusive=["up025", "01090"])

CAS += _paire("up029", "52019", "Ready for a Fight : Rhino allait manigancer -> forme heros, Rhino attaque a la place",
              "« When an enemy would scheme, discard Ready for a Fight -> change to hero form. That enemy attacks you instead »",
              ["Puzzle.PutIntoPlay('up029', under_control=True)", "Puzzle.SetThreat('01097b', 0)"], ["Puzzle.Scheme('01094')"],
              {"forme": "Hero", "defausse": ["up029"], "menace": [["01097b", 0]]},
              main_exclusive=["01090"], accepter_choix=True)

CAS += _paire("up032", "60053", "Ronin : sans allie, +1 DEF et riposte 1",
              "« While you do not control any allies, your hero gets +1 DEF and gains retaliate 1 »", [HEROS], [],
              {"en_jeu": ["up032"], "attributs": {"defense": 1, "retaliate": 1}},
              main_exclusive=["up032", "01089"], jouer=["up032"])

CAS += _paire("up034", "48012", "Seymour Gutz : 1 degat a Jessica Jones -> + ATQ 2 et CTR 1 imprimes jusqu'a la fin du round",
              "« Deal 1 damage to another friendly character -> ... adds that character's printed THW and ATK »",
              [HEROS, "Puzzle.PutIntoPlay('up034', under_control=True)", "Puzzle.PutIntoPlay('01059', under_control=True)"],
              ["Puzzle.Action('up034', 'Action')"],
              {"degats": [["01059", 1]], "attributs_carte": [["up034", "attack", 2], ["up034", "thwart", 1]]},
              main_exclusive=["01090"], cibles=["01059"])
CAS += _unique("up034", "48012", "Rogue")

CAS += _paire("up035", "21061", "Shield Spell : identite MYSTIC (Doctor Strange), attaque de Rhino entierement prevenue, 2 cartes du deck defaussees",
              "« discard that many cards from the top of your deck -> prevent all damage from this attack » ; la sonde "
              "sans la carte mesure 4 degats sur Doctor Strange dans ce montage : 6 - 4 = 2 cartes restent",
              ["Puzzle.ChangeForm('09001b')", "Puzzle.Exhaust('09001a')", SANS_DECK, DECK6], ["Puzzle.Attack('01094')"],
              {"degats_identite": 0, "taille_deck_joueur": 2, "defausse": ["up035"]},
              main_exclusive=["up035"], heros="doctor_strange")

CAS += _paire("up036", "60054", "Stand Alone : sans allie, l'attaque de Rhino redresse le heros",
              "« When an enemy attacks you, if you do not control any allies, exhaust Stand Alone -> ready your hero »",
              [HEROS, "Puzzle.PutIntoPlay('up036', under_control=True)", "Puzzle.Exhaust('01001a')"], ["Puzzle.Attack('01094')"],
              {"exhausted": ["up036"]},
              main_exclusive=["01090"], accepter_choix=True)

CAS += _paire("up037", "56048", "Taunt : Rhino attaque, puis 3 cartes piochees",
              "« The villain attacks you. ... Draw 3 cards » ; main finale 4 = 3 piochees + 1 de Spider-Sense "
              "(01001a : « When the villain initiates an attack against you, draw 1 card »)",
              [HEROS, SANS_DECK, DECK6], [],
              {"taille_main": 4, "defausse": ["up037"]},
              main_exclusive=["up037", "01090"], jouer=["up037"])

CAS += _paire("up038", "60052", "The Best Offense... : l'attaque de base utilise la DEF (3 + 1 = 4)",
              "« Your hero gets +1 DEF. Use your DEF in place of your THW and ATK »", [HEROS], [],
              {"degats": [["01094", 4]]},
              main_exclusive=["up038", "01089"], jouer=["up038"], cibles=["01094"],
              declencher_apres=["Puzzle.Attack('01001a')"])

CAS += _paire("up040", "09020", "Unflappable : defense sans degat -> incline, pioche 1",
              "« After you defend against an attack and take no damage, exhaust Unflappable -> draw 1 card » ; main "
              "1 + 1 (Spider-Sense) + 1 (Unflappable) = 3",
              [HEROS, SANS_DECK, DECK6, "Puzzle.PutIntoPlay('up040', under_control=True)"],
              ["Puzzle.Attack('01094', defender='01001a')"],
              {"exhausted": ["up040"], "taille_main": 3},
              main_exclusive=["01090"], accepter_choix=True)

CAS += _paire("up042", "27016", "What Doesn't Kill Me : soigne 2 et redresse le heros",
              "« Heal 2 damage from your hero -> ready your hero »",
              [HEROS, "Puzzle.Damage('01001a', 3)", "Puzzle.Exhaust('01001a')"], [],
              {"degats_identite": 1, "pret": ["01001a"]},
              main_exclusive=["up042", "01090"], jouer=["up042"])

CAS += _paire("up043", "54032", "Wonder Turtle : apres Defensive Stance (cout 2) resolue, soigne 2",
              "« After you resolve the ability of a Preparation card you control, heal damage from Wonder Turtle equal "
              "to that card's printed resource cost »",
              [HEROS, "Puzzle.Damage(Puzzle.PutIntoPlay('up043', under_control=True), 2)",
               "Puzzle.PutIntoPlay('08032', under_control=True)", "Puzzle.Exhaust('01001a')", "Puzzle.Exhaust('up043')"],
              ["Puzzle.Attack('01094')"],
              {"degats_identite": 0, "degats": [["up043", 0]]},
              main_exclusive=["01090"], accepter_choix=True)
CAS += _unique("up043", "54032", "White Widow")

# ===================================================================== MODIFIEES et compteur renomme (script propre)
CAS += [
    _c("up004 Autodefenestration : Rampage 2 paye (2 degats, 2 cartes) puis l'attaque de Rhino entierement prevenue",
       "« [star] Rampage 2 » + « Hero Interrupt (defense): When you would take any amount of damage from an attack, "
       "prevent all of that damage » : 2 degats du cout, 0 de l'attaque (ATQ 2, heros incline) ; deck 6 - 1 "
       "(Spider-Sense pioche 1 quand le vilain attaque) - 2 (Rampage) = 3",
       [HEROS, SANS_DECK, DECK6, "Puzzle.Exhaust('01001a')"], ["Puzzle.Attack('01094')"],
       {"degats_identite": 2, "taille_deck_joueur": 3, "defausse": ["up004"]},
       main_exclusive=["up004"]),
    _c("up004 Autodefenestration : identite Tenace -> cout Rampage NON paye, la carte reste en main",
       "fiche rampage.md : « take 2 damage » empeche par Tenace = cout impaye ; l'attaque consomme le Tenace : 0 degat, "
       "deck intact (6 - 1 Spider-Sense)",
       [HEROS, SANS_DECK, DECK6, "Puzzle.Exhaust('01001a')", "Puzzle.Tough('01001a')"], ["Puzzle.Attack('01094')"],
       {"degats_identite": 0, "en_main": ["up004"], "taille_deck_joueur": 5},
       main_exclusive=["up004"]),
    _c("up004 Autodefenestration : degats HORS attaque (Puzzle.Damage 3) -> non jouable, 3 degats",
       "contre-cas « from an attack »",
       [HEROS, SANS_DECK, DECK6], ["Puzzle.Damage('01001a', 3)"],
       {"degats_identite": 3, "en_main": ["up004"], "taille_deck_joueur": 6},
       main_exclusive=["up004"]),
    _c("up004 Autodefenestration : forme ALTER-EGO -> Hero Interrupt indisponible (2 degats de Rhino)",
       "« HERO Interrupt » (Backflip etait un Interrupt simple) : en civil la carte ne se joue pas",
       [SANS_DECK, DECK6, "Puzzle.Exhaust('01001b')"], ["Puzzle.Attack('01094')"],
       {"degats_identite": 2, "en_main": ["up004"]},
       main_exclusive=["up004"]),

    _c("up013 Groo the Wanderer : en jeu -> 1 carte rencontre face cachee distribuee au joueur",
       "« Forced Response: After Groo enters play under your control, deal yourself 1 facedown encounter card »",
       [HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101', '01101')"], [],
       {"carte": "up013", "distribuees": 1},
       main_exclusive=["up013", "01090"], jouer=["up013"], verifier="up_rencontre_distribuee"),
    _c("up013 Groo the Wanderer : AUCUN ranged -> la Riposte 1 de Badoon Sentry le touche (1 consecutif + 1 = 2)",
       "la ligne « attacks gain ranged » de 20016 n'est PAS imprimee sur Groo : 16120 Badoon Sentry (Retaliate 1) "
       "riposte ; Groo ATK 3* subit 1 degat consecutif + 1 de riposte",
       [HEROS, "Puzzle.PutIntoPlay('up013', under_control=True)", "Puzzle.PutIntoPlay('16120')"], ["Puzzle.Attack('up013')"],
       {"degats": [["up013", 2], ["16120", 3]]},
       main_exclusive=["01090"], cibles=["16120"]),
    _c("up013 TEMOIN 20016 Star-Lord : attaque ranged -> pas de riposte (1 consecutif seulement)",
       "temoin : la meme mesure voit bien le ranged de l'officielle",
       [HEROS, "Puzzle.PutIntoPlay('20016', under_control=True)", "Puzzle.PutIntoPlay('16120')"], ["Puzzle.Attack('20016')"],
       {"degats": [["20016", 1], ["16120", 2]]},
       main_exclusive=["01090"], cibles=["16120"]),

    _c("up014 Grotto : entre en jeu avec 2 compteurs brute ; son attaque sonne Rhino et lui inflige 1 + 2",
       "« enters play with 2 brute counters » ; « When Grotto attacks an enemy, remove 1 brute counter -> stun that "
       "enemy and deal 1 damage to it » : 1 (capacite) + 2 (ATQ) = 3, 1 compteur reste",
       [HEROS, "Puzzle.PutIntoPlay('up014', under_control=True)"], ["Puzzle.Attack('up014')"],
       {"degats": [["01094", 3]], "statuts": [["01094", "Stunned"]], "compteurs": [["up014", "brute", 1]]},
       main_exclusive=["01090"], cibles=["01094"], accepter_choix=True),
    _c("up014 TEMOIN 09014 Iron Fist : meme montage, compteurs mystic",
       "meme chiffre que l'officielle (3 degats, sonne, 1 compteur)",
       [HEROS, "Puzzle.PutIntoPlay('09014', under_control=True)"], ["Puzzle.Attack('09014')"],
       {"degats": [["01094", 3]], "statuts": [["01094", "Stunned"]], "compteurs": [["09014", "mystic", 1]]},
       main_exclusive=["01090"], cibles=["01094"], accepter_choix=True),
]
CAS += _unique("up014", "09014", "Iron Fist")

CAS += [
    _c("up021 Jotaro : Rhino frapperait le heros de 2 -> [physical] depense, 1 seul degat",
       "« When an enemy would deal any amount of damage, spend a [physical] resource -> reduce that amount by 1 »",
       [HEROS, SANS_DECK, DECK6, "Puzzle.PutIntoPlay('up021', under_control=True)", "Puzzle.Exhaust('01001a')",
        "Puzzle.Exhaust('up021')"],
       ["Puzzle.Attack('01094')"],
       {"degats_identite": 1, "defausse": ["01090"]},
       main_exclusive=["01090"], accepter_choix=True),
    _c("up021 Jotaro : sans ressource [physical] (Genius BB), pas de reduction : 2 degats",
       "contre-cas du cout « spend a [physical] resource »",
       [HEROS, SANS_DECK, DECK6, "Puzzle.PutIntoPlay('up021', under_control=True)", "Puzzle.Exhaust('01001a')",
        "Puzzle.Exhaust('up021')"],
       ["Puzzle.Attack('01094')"],
       {"degats_identite": 2, "en_main": ["01089"]},
       main_exclusive=["01089"], accepter_choix=True),
    _c("up021 Jotaro : TEMOIN D'EPUISEMENT, deux attaques dans le round -> une seule reduction (6 - 1 = 5)",
       "« (Limit once per round.) » : ligne de base mesuree SANS Jotaro = 6 (cas suivant) ; avec Jotaro et deux "
       "Strength en main, une seule reduction de 1 -> 5 (deux reductions donneraient 4)",
       [HEROS, SANS_DECK, DECK6, "Puzzle.PutIntoPlay('up021', under_control=True)", "Puzzle.Exhaust('01001a')",
        "Puzzle.Exhaust('up021')"],
       ["Puzzle.Attack('01094')", "Puzzle.Attack('01094')"],
       {"degats_identite": 5, "en_main": ["01090"]},
       main_exclusive=["01090", "01090"], accepter_choix=True),
    _c("up021 Jotaro : ligne de base SANS Jotaro, deux attaques de Rhino -> 6 degats",
       "ligne de base du temoin d'epuisement (meme montage, Jotaro absent) : 2 puis 4 dans ce harnais (la 2e attaque "
       "de Rhino frappe plus fort ; la cause est hors carte, on mesure l'ecart)",
       [HEROS, SANS_DECK, DECK6, "Puzzle.Exhaust('01001a')"],
       ["Puzzle.Attack('01094')", "Puzzle.Attack('01094')"],
       {"degats_identite": 6},
       main_exclusive=["01090", "01090"], accepter_choix=True),
    _c("up021 Jotaro : Tenacite (Toughness) -> entre en jeu avec une carte Tenace",
       "« Toughness » lu dans desc",
       [HEROS], [],
       {"en_jeu": ["up021"], "statuts": [["up021", "Tough"]]},
       main_exclusive=["up021", "01090", "01088"], jouer=["up021"]),

    _c("up022 Lindsey Baker : Action -> soigne 1 et defausse le Sonne du heros, 1 compteur healing retire",
       "« Exhaust Lindsey Baker and remove 1 healing counter from her -> heal 1 damage from a hero and discard 1 "
       "status card from it » ; Uses (3 healing counters)",
       [HEROS, "Puzzle.PutIntoPlay('up022', under_control=True)", "Puzzle.Damage('01001a', 2)", "Puzzle.Stun('01001a')"],
       ["Puzzle.Action('up022', 'Action')"],
       {"degats_identite": 1, "statuts_absents": [["01001a", "Stunned"]], "compteurs": [["up022", "healing", 2]],
        "exhausted": ["up022"]},
       main_exclusive=["01090"], cibles=["01001a"], accepter_choix=True),
    _c("up022 TEMOIN 09019 The Night Nurse : meme montage (compteurs medical)",
       "meme chiffre que l'officielle",
       [HEROS, "Puzzle.PutIntoPlay('09019', under_control=True)", "Puzzle.Damage('01001a', 2)", "Puzzle.Stun('01001a')"],
       ["Puzzle.Action('09019', 'Action')"],
       {"degats_identite": 1, "statuts_absents": [["01001a", "Stunned"]], "compteurs": [["09019", "medical", 2]],
        "exhausted": ["09019"]},
       main_exclusive=["01090"], cibles=["01001a"], accepter_choix=True),
]
CAS += _unique("up022", "09019", "The Night Nurse")

CAS += [
    _c("up027 Protection Training : s'attache a un allie NINJA (Honor Blade? non : Wonder Turtle) -> +3 PV",
       "« Attach to a NINJA or MUTANIMAL ally. Attached ally gets +3 hit points » : Wonder Turtle up043 (NINJA)",
       [HEROS, "Puzzle.PutIntoPlay('up043', under_control=True)"], [],
       {"attaches": [["up043", "up027"]], "attributs_carte": [["up043", "health", 3]]},
       main_exclusive=["up027", "01089"], jouer=["up027"], cibles=["up043"]),
    _c("up027 Protection Training : allie MUTANIMAL seul (Seymour Gutz up034) -> jouable, +3 PV",
       "deuxieme branche du OU : MUTANIMAL",
       [HEROS, "Puzzle.PutIntoPlay('up034', under_control=True)"], [],
       {"attaches": [["up034", "up027"]], "attributs_carte": [["up034", "health", 3]]},
       main_exclusive=["up027", "01089"], jouer=["up027"], cibles=["up034"]),
    _c("up027 Protection Training : seul allie X-MEN/autre (Jessica Jones 01059) -> injouable",
       "contre-cas : ni NINJA ni MUTANIMAL (c'est la difference avec 32013 « X-MEN ally »)",
       [HEROS, "Puzzle.PutIntoPlay('01059', under_control=True)"], [],
       {"en_main": ["up027"]},
       main_exclusive=["up027", "01089"], jouer=["up027"]),

    _c("up031 Road Rage : entre avec 3 compteurs fuel ; un sbire entre -> 2 degats, 2 compteurs restent",
       "« enters play with 3 fuel counters » + « After a minion enters play, remove 1 fuel counter -> deal 2 damage "
       "to that minion » : Hydra Mercenary 3 PV -> 2 degats",
       [HEROS, "Puzzle.PutIntoPlay('up031', under_control=True)"], ["Puzzle.Reveal('01101')"],
       {"degats": [["01101", 2]], "compteurs": [["up031", "fuel", 2]]},
       main_exclusive=["01090"], accepter_choix=True),
    _c("up031 TEMOIN 01066 Hawkeye : meme montage, 4 compteurs arrow -> 3",
       "le texte de la Reponse est celui de 01066 ; seul le nombre/nom des compteurs differe",
       [HEROS, "Puzzle.PutIntoPlay('01066', under_control=True)"], ["Puzzle.Reveal('01101')"],
       {"degats": [["01101", 2]], "compteurs": [["01066", "arrow", 3]]},
       main_exclusive=["01090"], accepter_choix=True),
]

# ===================================================================== NOUVELLES
CAS += [
    # ------------------------------------------------------------------ up007 Cyber Ninja
    _c("up007 Cyber Ninja : Reponse, une amelioration defaussee de la main -> pioche 1 et Camoufle",
       "« After Cyber Ninja enters play, discard an upgrade from your hand -> draw 1 card and cloak Cyber Ninja »",
       [HEROS, SANS_DECK, DECK6], [],
       {"en_jeu": ["up007"], "statuts": [["up007", "Cloaked"]], "defausse": ["01081"], "taille_main": 1},
       main_exclusive=["up007", "01089", "01081"], payer_avec=["01089"], jouer=["up007"], accepter_choix=True),
    _c("up007 Cyber Ninja : sans amelioration en main, cout impayable -> ni pioche ni Camoufle",
       "contre-cas du cout « discard an upgrade from your hand » (la main ne contient qu'un evenement)",
       [HEROS, SANS_DECK, DECK6], [],
       {"en_jeu": ["up007"], "statuts_absents": [["up007", "Cloaked"]], "en_main": ["01003"], "taille_main": 1},
       main_exclusive=["up007", "01089", "01003"], payer_avec=["01089"], jouer=["up007"], accepter_choix=True),

    # ------------------------------------------------------------------ up009 Demoralize
    _c("up009 Demoralize : Rhino attaque le heros (incline : 2 degats) puis est Desoriente",
       "« Choose an enemy. It attacks you. Confuse that enemy »",
       [HEROS, "Puzzle.Exhaust('01001a')"], [],
       {"degats_identite": 2, "statuts": [["01094", "Confused"]], "defausse": ["up009"]},
       main_exclusive=["up009"], jouer=["up009"], cibles=["01094"]),
    _c("up009 Demoralize : un SBIRE choisi (Hydra Mercenary) attaque puis est Desoriente ; Rhino intact",
       "« an enemy » : un sbire aussi ; « that enemy » = le meme",
       [HEROS, "Puzzle.Exhaust('01001a')", SBIRE], [],
       {"statuts": [["01101", "Confused"]], "statuts_absents": [["01094", "Confused"]], "defausse": ["up009"]},
       main_exclusive=["up009"], jouer=["up009"], cibles=["01101"]),

    # ------------------------------------------------------------------ up015 Helpful Bystander
    _c("up015 Helpful Bystander : Rhino attaque le joueur -> attaque le Bystander a la place, deferlement 1 sur l'identite",
       "« it attacks Helpful Bystander instead. This attack gains overkill » : ATQ 2 sur 1 PV -> vaincu, 1 d'exces a "
       "l'identite (overkill.md : allie vaincu -> identite du controleur)",
       [HEROS, "Puzzle.PutIntoPlay('up015', under_control=True)", "Puzzle.Exhaust('01001a')"], ["Puzzle.Attack('01094')"],
       {"hors_jeu": ["up015"], "degats_identite": 1},
       main_exclusive=["01090"]),
    _c("up015 Helpful Bystander : votre heros gagne +1 taille de main",
       "« Your hero gets +1 hand size »",
       [HEROS, "Puzzle.PutIntoPlay('up015', under_control=True)"], [],
       {"attributs": {"hand_size": 1}},
       main_exclusive=["01090"]),

    # ------------------------------------------------------------------ up016 Herman
    _c("up016 Herman : surpaye de 2 (4 ressources pour un cout de 2) -> 3 cartes Tenace",
       "Toughness (1) + « an additional tough status card on him (to a max of 2) for each resource you overpaid »",
       [HEROS], [],
       {"carte": "up016", "tenaces": 3}, verifier="up_tenaces",
       main_exclusive=["up016", "01090", "01088"], jouer=["up016"], surpayer=True, payer_tout=True,
       payer_avec=["01090", "01088"]),
    _c("up016 Herman : paye juste (cout 2) -> 1 seule Tenace (Toughness)",
       "contre-cas : aucun surpaiement",
       [HEROS], [],
       {"carte": "up016", "tenaces": 1}, verifier="up_tenaces",
       main_exclusive=["up016", "01090"], jouer=["up016"]),
    _c("up016 Herman : surpaye de 4 (6 ressources) -> plafond, 3 Tenace et pas 5",
       "TEMOIN de la limite « to a max of 2 » et du « up to 3 tough status cards »",
       [HEROS], [],
       {"carte": "up016", "tenaces": 3}, verifier="up_tenaces",
       main_exclusive=["up016", "01090", "01088", "01089"], jouer=["up016"], surpayer=True, payer_tout=True,
       payer_avec=["01090", "01088", "01089"]),

    # ------------------------------------------------------------------ up023 Lookout
    _c("up023 Lookout : un sbire vous engage -> Lookout defausse, heros Camoufle, 1 carte piochee",
       "« After a minion engages you, discard Lookout -> cloak your hero and draw 1 card »",
       [HEROS, SANS_DECK, DECK6, "Puzzle.PutIntoPlay('up023', under_control=True)"], ["Puzzle.Reveal('01101')"],
       {"defausse": ["up023"], "statuts": [["01001a", "Cloaked"]], "taille_main": 2},
       main_exclusive=["01090"], accepter_choix=True),
    _c("up023 Lookout : soutien NYC controle (Shell Cycle tr008) -> cout 1, jouable avec une seule ressource",
       "« Reduce the cost to play this card by 1 if you control a NYC support » ; 01081 ne genere qu'1 ressource",
       [HEROS, "Puzzle.PutIntoPlay('tr008', under_control=True)"], [],
       {"en_jeu": ["up023"]},
       main_exclusive=["up023", "01081"], jouer=["up023"]),
    _c("up023 Lookout : SANS soutien NYC -> cout 2, injouable avec une seule ressource",
       "contre-cas de la reduction",
       [HEROS], [],
       {"en_main": ["up023"]},
       main_exclusive=["up023", "01081"], jouer=["up023"]),

    # ------------------------------------------------------------------ up024 Nobody
    _c("up024 Nobody : Reponse -> option Tenace",
       "« place a tough or cloaked status card on them » : premiere option",
       [HEROS], [],
       {"statuts": [["up024", "Tough"]], "statuts_absents": [["up024", "Cloaked"]]},
       main_exclusive=["up024", "01090", "01088"], jouer=["up024"], accepter_choix=True,
       preferer_option="Place a tough"),
    _c("up024 Nobody : Reponse -> option Camoufle",
       "seconde option (une seule des deux)",
       [HEROS], [],
       {"statuts": [["up024", "Cloaked"]], "statuts_absents": [["up024", "Tough"]]},
       main_exclusive=["up024", "01090", "01088"], jouer=["up024"], accepter_choix=True,
       preferer_option="Place a cloaked"),

    # ------------------------------------------------------------------ up026 Primal Provisions
    _c("up026 Primal Provisions : Rampage 2 paye puis 2 cartes piochees",
       "« [star] Rampage 2 » + « Hero Action: Draw 2 cards » : deck 6 - 2 - 2 = 2, main 2, 2 degats",
       [HEROS, SANS_DECK, DECK6], [],
       {"degats_identite": 2, "taille_deck_joueur": 2, "taille_main": 2, "defausse": ["up026"]},
       main_exclusive=["up026"], jouer=["up026"]),
    _c("up026 Primal Provisions : TEMOIN D'EPUISEMENT « Max 1 per phase » : la 2e copie reste en main",
       "deux copies jouees dans la meme phase : un seul Rampage paye (2 degats), une copie en main",
       [HEROS, SANS_DECK, DECK6], [],
       {"degats_identite": 2, "en_main": ["up026"], "taille_deck_joueur": 2},
       main_exclusive=["up026", "up026"], jouer=["up026", "up026"]),

    # ------------------------------------------------------------------ up028 Rabid Infection
    _c("up028 Rabid Infection : sbire attaque par le heros -> attachee, vulnerable : Sonne = defausse",
       "« Attach to a minion that your hero attacked this turn. If attached to a non-ELITE minion, it gains "
       "vulnerable » ; puis Puzzle.Stun : un sbire vulnerable etourdi est defausse",
       [HEROS, SBIRE], ["Puzzle.Attack('01001a')"],
       {"hors_jeu": ["01101"]},
       main_exclusive=["up028"], jouer=["up028"], cibles=["01101"],
       declencher_apres=["Puzzle.Stun(Puzzle.FindFaceInPlay('01101'))"]),
    _c("up028 Rabid Infection : sbire NON attaque ce tour -> injouable",
       "contre-cas « that your hero attacked this turn »",
       [HEROS, SBIRE], [],
       {"en_main": ["up028"], "en_jeu": ["01101"]},
       main_exclusive=["up028"], jouer=["up028"]),
    _c("up028 Rabid Infection : sbire ELITE (Killmonger 01157) -> pas vulnerable, survit au Sonne",
       "« non-ELITE » : un sbire ELITE ne gagne rien",
       [HEROS, "Puzzle.PutIntoPlay('01157')"], ["Puzzle.Attack('01001a')"],
       {"en_jeu": ["01157"], "attaches": [["01157", "up028"]], "statuts": [["01157", "Stunned"]]},
       main_exclusive=["up028"], jouer=["up028"], cibles=["01157"],
       declencher_apres=["Puzzle.Stun('01157')"]),
    _c("up028 Rabid Infection : le sbire s'active (attaque) -> 1 degat a un ennemi (Rhino)",
       "« Interrupt: When attached minion activates, deal 1 damage to an enemy »",
       [HEROS, SBIRE], ["Puzzle.Attack('01001a')"],
       {"degats": [["01094", 1]]},
       main_exclusive=["up028"], jouer=["up028"], cibles=["01094", "01101"], accepter_choix=True,
       declencher_apres=["Puzzle.Attack('01101')"]),

    # ------------------------------------------------------------------ up033 Senkon
    _c("up033 Senkon : attache a Jessica Jones qui defend contre Rhino -> Rhino -1 ATQ (1 degat au lieu de 2)",
       "« When attached character defends against an enemy attack, exhaust Senkon -> that enemy gets –1 ATK »",
       [HEROS, "Puzzle.PutIntoPlay('01059', under_control=True)"], [],
       {"degats": [["01059", 1]], "exhausted": ["up033"], "attaches": [["01059", "up033"]]},
       main_exclusive=["up033", "01090"], jouer=["up033"], cibles=["01059"], accepter_choix=True,
       declencher_apres=["Puzzle.Attack('01094', defender='01059')"]),
    _c("up033 Senkon : attache a un ALLIE -> pas restricted",
       "« While attached to an identity, this card gains restricted » : sur un allie, 0",
       [HEROS, "Puzzle.PutIntoPlay('01059', under_control=True)"], [],
       {"carte": "up033", "restricted": 0}, verifier="up_restricted",
       main_exclusive=["up033", "01090"], jouer=["up033"], cibles=["01059"]),
    _c("up033 Senkon : attache a l'IDENTITE -> restricted",
       "branche « attached to an identity »",
       [HEROS], [],
       {"carte": "up033", "restricted": 1}, verifier="up_restricted",
       main_exclusive=["up033", "01090"], jouer=["up033"], cibles=["01001a"]),

    # ------------------------------------------------------------------ up039 Tonfa
    _c("up039 Tonfa : attaque non defendue de Rhino -> option riposte 1 : Rhino subit 1",
       "« give your hero either +1 DEF or retaliate 1 for this attack » : option riposte",
       [HEROS, "Puzzle.PutIntoPlay('up039', under_control=True)", "Puzzle.Exhaust('01001a')"], ["Puzzle.Attack('01094')"],
       {"degats": [["01094", 1]], "degats_identite": 2, "exhausted": ["up039"]},
       main_exclusive=["01090"], accepter_choix=True, preferer_option="retaliate"),
    _c("up039 Tonfa : Titania (ATQ 6) attaque, le heros defend (DEF 3) -> option +1 DEF : 2 degats au lieu de 3",
       "option +1 DEF ; ligne de base : cas suivant (3 degats sans Tonfa)",
       [HEROS, "Puzzle.PutIntoPlay('up039', under_control=True)", "Puzzle.PutIntoPlay('01162')"],
       ["Puzzle.Attack('01162', defender='01001a')"],
       {"degats_identite": 2, "exhausted": ["up039"]},
       main_exclusive=["01090"], accepter_choix=True, preferer_option="+1 DEF"),
    _c("up039 Tonfa : ligne de base SANS Tonfa, Titania contre DEF 3 -> 3 degats",
       "ligne de base du cas precedent",
       [HEROS, "Puzzle.PutIntoPlay('01162')"], ["Puzzle.Attack('01162', defender='01001a')"],
       {"degats_identite": 3},
       main_exclusive=["01090"], accepter_choix=True),

    # ------------------------------------------------------------------ up041 Usagi Yojimbo
    _c("up041 Usagi Yojimbo : defend sans s'incliner (reste pret), Tenace consomme, Riposte 2 sur Rhino",
       "« does not exhaust to defend » + Toughness + Retaliate 2 ; defense par la VRAIE question du moteur (le raccourci "
       "`Puzzle.Attack(defender=...)` incline le defenseur lui-meme et court-circuite le cout)",
       [HEROS, "Puzzle.PutIntoPlay('up041', under_control=True)", "Puzzle.Exhaust('01001a')"], ["Puzzle.Attack('01094')"],
       {"pret": ["up041"], "statuts_absents": [["up041", "Tough"]], "degats": [["01094", 2], ["up041", 0]],
        "degats_identite": 0},
       main_exclusive=["01090"]),
    _c("up041 Usagi Yojimbo : INCLINE, il peut quand meme defendre (RR v1.8, « Defending »)",
       "« A card ability that allows an ally to be declared as a defender without exhausting can be used on an "
       "exhausted ally »",
       [HEROS, "Puzzle.PutIntoPlay('up041', under_control=True)", "Puzzle.Exhaust('up041')", "Puzzle.Exhaust('01001a')"],
       ["Puzzle.Attack('01094')"],
       {"statuts_absents": [["up041", "Tough"]], "degats_identite": 0, "degats": [["01094", 2]]},
       main_exclusive=["01090"]),
    _c("up041 Usagi Yojimbo : la capacite ne deborde PAS sur un autre allie (Jessica Jones defend et s'incline)",
       "« USAGI does not exhaust » : Jessica Jones, en jeu avec Usagi, s'incline toujours pour defendre (le cout "
       "d'inclinaison est propre a chaque face) ; Usagi incline pour ne pas etre choisi",
       [HEROS, "Puzzle.PutIntoPlay('up041', under_control=True)", "Puzzle.Exhaust('up041')",
        "Puzzle.PutIntoPlay('01059', under_control=True)", "Puzzle.Exhaust('01001a')"], ["Puzzle.Attack('01094')"],
       {"exhausted": ["01059"], "degats": [["01059", 2]]},
       main_exclusive=["01090"], preferer_option="Defense", cibles=["01059"]),
    _c("up041 TEMOIN moteur 53011 Draw Their Fire : Falcon defend sans s'incliner (correctif cost_func.Exhaust)",
       "carte officielle de la meme mecanique (`not_need_to_exhaust`) : apres le debut de la phase du vilain, "
       "Falcon defend et reste pret",
       ["Puzzle.ChangeForm('53001b')", "Puzzle.PutIntoPlay('53011', under_control=True)"],
       ["Puzzle.BeginVillainPhase()", "Puzzle.Attack('01094')"],
       {"pret": ["53001a"], "defausse": ["53011"]},
       main_exclusive=["01090"], heros="falcon", accepter_choix=True),
    _c("up041 TEMOIN : un allie ordinaire (Jessica Jones) s'incline pour defendre",
       "temoin de la mesure « pret » : sans la capacite, le defenseur est incline",
       [HEROS, "Puzzle.PutIntoPlay('01059', under_control=True)", "Puzzle.Exhaust('01001a')"], ["Puzzle.Attack('01094')"],
       {"exhausted": ["01059"]},
       main_exclusive=["01090"]),
]


VERIFICATIONS = r'''
def up_rencontre_distribuee(monde, aides):
    """Nombre de cartes rencontre distribuees face cachee au joueur 1 (en attente de revelation)
    + la carte `carte` est en jeu. `attendu` = {carte, distribuees}."""
    attendu = aides["cas"]["attendu"]
    if aides["par_id"](monde, attendu["carte"]) is None:
        return False, f"{attendu['carte']} n'est pas en jeu"
    n = len(monde.players[0].dealt_encounter_cards.Get())
    if n != attendu["distribuees"]:
        return False, f"{n} carte(s) rencontre distribuee(s) (attendu {attendu['distribuees']})"
    return True, f"{n} carte(s) rencontre distribuee(s), face cachee"


def up_tenaces(monde, aides):
    """Nombre de cartes Tough sur `carte` (en jeu). `attendu` = {carte, tenaces}."""
    attendu = aides["cas"]["attendu"]
    face = aides["par_id"](monde, attendu["carte"])
    if face is None:
        return False, f"{attendu['carte']} n'est pas en jeu"
    n = face.CastTo(aides["CanStatus"]).tough
    if n != attendu["tenaces"]:
        return False, f"{n} carte(s) Tenace (attendu {attendu['tenaces']})"
    return True, f"{n} carte(s) Tenace"


def up_restricted(monde, aides):
    """Valeur courante du mot-cle restricted de `carte`. `attendu` = {carte, restricted}."""
    attendu = aides["cas"]["attendu"]
    face = aides["par_id"](monde, attendu["carte"])
    if face is None:
        return False, f"{attendu['carte']} n'est pas en jeu"
    n = face.restricted
    if n != attendu["restricted"]:
        return False, f"restricted = {n} (attendu {attendu['restricted']})"
    return True, f"restricted = {n}"
'''
