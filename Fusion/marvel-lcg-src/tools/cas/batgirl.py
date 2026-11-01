# Cas test_capacites du heros BATGIRL (ES, « Sealed 11.26.2025 », prefixe `bg`) : noms prefixes « [bg] » puis le card_id
# (substituer_pack.py filtre dessus). Un cas par capacite, sujet = le card_id dans le nom.
#
# Rappels de montage :
#  - le deck batgirl demarre en ALTER EGO (bg001b Barbara Gordon) ; `Puzzle.ChangeToFace('bg001b', 'bg001a')` le passe en forme HEROS
#    SANS declencher de Reponse ; `Puzzle.ChangeToFace('bg001a', 'bg001b')` revient en alter ego ;
#  - Rhino 01094 est le vilain, 01097b son complot principal, 01101 Hydra Mercenary (3 PV, Guard), 01103 Shocker (3 PV), 01121 Weapons
#    Runner (2 PV, ATQ 1), 01182 Hydra Soldier (4 PV, Guard) ; 01098 sert de boost neutre ; 01190 Shadow of the Past (traitrise, boost 2) ;
#  - ressources : 01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR (cartes Basic) ; 01020 Hellcat (RES G) = UNE [wild] ;
#  - `main_exclusive` donne la main EXACTE apres la mise en place.
SC = "rhino"
HEROS = "Puzzle.ChangeToFace('bg001b', 'bg001a')"
HEROS_BF = "Puzzle.ChangeToFace('bg001b', 'bg001c')"
CIVIL = "Puzzle.ChangeToFace('bg001a', 'bg001b')"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01098', '01098', '01098', '01098', '01098', '01098', '01098', '01098')"]
COMPLOT = "01097b"
VILAIN = "01094"
PIOCHE = ["Puzzle.EmptyPlayerDeck()",
          "Puzzle.CreatePlayerDeck('01057', '01057', '01057', '01057', '01057', '01057', '01057', '01057')"]


def en_jeu(*ids):
    return [f"Puzzle.PutIntoPlay('{i}', under_control=True)" for i in ids]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    # La main EXACTE se pose par la mise en place (pas par `main_exclusive`, qui DEFAUSSE l'ancienne main et fausse les comptes
    # de defausse) : EmptyHand, defausse videe, puis les cartes voulues.
    main = cle.pop("main_exclusive", [])
    mise = SANS_BOOST + PIOCHE + ["Puzzle.EmptyHand()", "Puzzle.EmptyPlayerDiscardPile()"] + list(mise)
    if main:
        mise += ["Puzzle.CreateHandCards(" + ", ".join(repr(c) for c in main) + ")"]
    cas = {"nom": "[bg] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "batgirl"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "bg_etat"), "attendu": attendu}
    cas.setdefault("regles", ["v16_all", "v18_all"])
    cas.update(cle)
    return cas


CAS = [
    # ============================================================ bg001a / bg001c / bg001b : valeurs imprimees
    _c("bg001a Batgirl (Birds of Prey) : valeurs imprimees PV 10, THW 2, ATK 1, DEF 2, main 5, trait BIRD OF PREY",
       "nombres texte <-> code (scan) : HAND SIZE 5 / HIT POINTS 10 ; THW 2 ATK 1 DEF 2", [HEROS], [],
       {"pv_max": [["bg001a", 10]], "traits": ["BIRD OF PREY"],
        "bg_stats": {"attack": 1, "thwart": 2, "defense": 2, "hand_size": 5}}, main_exclusive=["01090"]),
    _c("bg001b Barbara Gordon : valeurs imprimees PV 10, REC 3, main 6, trait GENIUS",
       "nombres texte <-> code (scan) : HAND SIZE 6 / HIT POINTS 10 / REC 3", [], [],
       {"pv_max": [["bg001b", 10]], "traits": ["GENIUS"], "bg_stats": {"recover": 3, "hand_size": 6}}, main_exclusive=["01090"]),
    # ============================================================ bg001a The Oracle
    _c("bg001a The Oracle : Applying Pressure payee en [energy], [physical] change en [energy] -> les 2 degats partent",
       "« change a resource icon in the text of that card » : le texte devient « using only [energy] resources »",
       [HEROS, "Puzzle.SetThreat('01097b', 6)", "Puzzle.PutIntoPlay('01182')"], [], {"degats": [["01182", 2]], "menace": [[COMPLOT, 2]]},
       main_exclusive=["bg004", "01088"], jouer=["bg004"], payer_avec=["01088"], cibles=[COMPLOT, "01182"],
       preferer_option="Change [physical] to [energy]"),
    _c("bg001a The Oracle : TEMOIN, sans changement d'icone, Applying Pressure payee en [energy] n'inflige PAS les 2 degats",
       "icone [physical] inchangee : payee en energie, la branche des degats ne part pas",
       [HEROS, "Puzzle.PutIntoPlay('01182')", "Puzzle.SetThreat('01097b', 5)"], [], {"degats": [["01182", 0]], "menace": [[COMPLOT, 1]]},
       main_exclusive=["bg004", "01088"], jouer=["bg004"], payer_avec=["01088"], cibles=[COMPLOT, "01182"],
       ),
    # ============================================================ bg001b Eidetic Memory
    _c("bg001b Eidetic Memory : la carte [physical] la plus ANCIENNE de la defausse remonte sur le deck",
       "« put the BOTTOMMOST card with a printed resource of that type from your discard pile on top of your deck »",
       ["Puzzle.CreatePlayerDiscardPile('01024', '01090', '01088')"], ["Puzzle.Action('bg001b')"],
       {"dans_deck_joueur": ["01024"]}, main_exclusive=["01057"], preferer_option="[physical]"),
    _c("bg001b Eidetic Memory : TEMOIN, rien n'a ete vaincu ce round -> pas de carte piochee",
       "le « draw 1 card » exige un exploit ce round", ["Puzzle.CreatePlayerDiscardPile('01024', '01090')"],
       ["Puzzle.Action('bg001b')"], {"dans_deck_joueur": ["01024"], "taille_main": 1}, main_exclusive=["01057"],
       preferer_option="[physical]"),
    _c("bg001b Eidetic Memory : un ennemi vaincu ce round -> une carte piochee en plus",
       "« If you defeated an enemy ... this round, draw 1 card »",
       ["Puzzle.CreatePlayerDiscardPile('01024', '01090')", HEROS, "Puzzle.PutIntoPlay('01121')", "Puzzle.Damage('01121', 1)"],
       ["Puzzle.Attack('bg001a')", CIVIL, "Puzzle.Action('bg001b')"],
       {"en_main": ["01024"], "hors_jeu": ["01121"], "taille_main": 2}, main_exclusive=["01057"],
       cibles=["01121"], preferer_option="[physical]"),
    _c("bg001b Eidetic Memory : limite UNE fois par round (temoin d'epuisement : la 2e Action ne deplace rien)",
       "« Limit once per round » : deux Actions dans le meme round, la seconde ne change pas la defausse (1 carte deplacee seulement)",
       ["Puzzle.CreatePlayerDiscardPile('01024', '01090', '01088')"], ["Puzzle.Action('bg001b')", "Puzzle.Action('bg001b')"],
       {"dans_deck_joueur": ["01024"], "defausse_joueur": 2, "taille_deck_joueur": 9}, main_exclusive=["01057"],
       preferer_option="[physical]"),
    # ============================================================ bg002 Black Canary
    _c("bg002 Black Canary : payee avec des ressources [mental] -> autant d'ennemis sonnes",
       "« stun 1 enemy for each [mental] resource used to pay for her cost » (cout 3 : deux Genius BB BB = 4 ressources [mental])",
       [HEROS] + en_jeu("01121", "01103", "01101", "01182"), [], {"statuts": [["01121", "Stunned"]]},
       main_exclusive=["bg002", "01089", "01089"], jouer=["bg002"], payer_avec=["01089", "01089"], cibles=["01121", "01103", "01101", "01182"]),
    _c("bg002 Black Canary : TEMOIN, payee sans [mental] (Energy YY + Strength RR) -> aucun ennemi sonne",
       "aucune ressource [mental] : aucune carte d'etat Sonne", [HEROS] + en_jeu("01121"), [],
       {"statuts_absents": [["01121", "Stunned"]], "en_jeu": ["bg002"]},
       main_exclusive=["bg002", "01088", "01090"], jouer=["bg002"], payer_avec=["01088", "01090"], cibles=["01121"]),
    # ============================================================ bg003 Nightwing
    _c("bg003 Nightwing : apres une attaque de base, la PROCHAINE ressource generee devient [wild] : le joueur la declare [mental] -> Batarangs 2 + 2 ([physical]) et un Desoriente",
       "« the next resource you generate is considered a [wild] resource » : Strength RR -> G + R ; RR Wild Resource : le wild compte pour le type declare (mental) : 2 degats + 1 ligne [physical] = 4 sur Rhino, et la ligne [mental] desoriente",
       [HEROS, "Puzzle.SetThreat('01097b', 6)", "Puzzle.PutIntoPlay('bg003', under_control=True)"],
       ["Puzzle.Action('bg003', 'BasicPower', 1)"], {"degats": [[VILAIN, 4]], "menace": [[COMPLOT, 4]], "statuts": [[VILAIN, "Confused"]]},
       main_exclusive=["bg005", "01090"], jouer=["bg005"], payer_avec=["01090"], cibles=[VILAIN, VILAIN, VILAIN], preferer_option="B"),
    _c("bg003 Nightwing : TEMOIN, sans attaque de Nightwing, Batarangs payee en Strength RR : 2 + 2 + 2 = 6 sur Rhino",
       "sans Reponse, deux ressources [physical] imprimees : deux lignes", [HEROS, "Puzzle.PutIntoPlay('bg003', under_control=True)"], [],
       {"degats": [[VILAIN, 6]]}, main_exclusive=["bg005", "01090"], jouer=["bg005"], payer_avec=["01090"], cibles=[VILAIN, VILAIN, VILAIN]),
    # ============================================================ bg004 Applying Pressure
    _c("bg004 Applying Pressure : payee en [physical] -> 4 menace retirees ET 2 degats",
       "« remove 4 threat ... If you paid using only [physical] resources, deal 2 damage to an enemy »",
       [HEROS, "Puzzle.SetThreat('01097b', 6)", "Puzzle.PutIntoPlay('01182')"], [], {"menace": [[COMPLOT, 2]], "degats": [["01182", 2]]},
       main_exclusive=["bg004", "01090"], jouer=["bg004"], payer_avec=["01090"], cibles=[COMPLOT, "01182"]),
    _c("bg004 Applying Pressure : TEMOIN, payee en [energy] -> 4 menace retirees, AUCUN degat",
       "la branche des degats exige « only [physical] »", [HEROS, "Puzzle.SetThreat('01097b', 6)", "Puzzle.PutIntoPlay('01182')"], [],
       {"menace": [[COMPLOT, 2]], "degats": [["01182", 0]]},
       main_exclusive=["bg004", "01088"], jouer=["bg004"], payer_avec=["01088"], cibles=[COMPLOT, "01182"]),
    _c("bg004 Applying Pressure : l'ennemi VAINCU par l'attaque -> 1 carte piochee",
       "« If this attack defeats an enemy, draw 1 card » (Weapons Runner 2 PV)",
       [HEROS, "Puzzle.SetThreat('01097b', 6)", "Puzzle.PutIntoPlay('01121')"], [], {"hors_jeu": ["01121"], "taille_main": 1},
       main_exclusive=["bg004", "01090"], jouer=["bg004"], payer_avec=["01090"], cibles=[COMPLOT, "01121"]),
    # ============================================================ bg005 Batarangs
    _c("bg005 Batarangs : payee Strength RR -> 2 degats + 2 lignes [physical] = 6 sur Rhino",
       "« Deal 2 damage ... for each [physical] resource: deal 2 damage »", [HEROS], [], {"degats": [[VILAIN, 6]]},
       main_exclusive=["bg005", "01090"], jouer=["bg005"], payer_avec=["01090"], cibles=[VILAIN, VILAIN, VILAIN]),
    _c("bg005 Batarangs : payee Energy YY -> 2 degats et 2 ennemis sonnes",
       "« [energy] - Stun an enemy » une fois par ressource", [HEROS] + en_jeu("01121", "01103"), [],
       {"degats": [[VILAIN, 2]], "statuts": [[VILAIN, "Stunned"]]},
       main_exclusive=["bg005", "01088"], jouer=["bg005"], payer_avec=["01088"], cibles=[VILAIN, "01121", "01103"]),
    _c("bg005 Batarangs : payee Genius BB -> 2 degats et 2 ennemis desorientes",
       "« [mental] - Confuse an enemy » une fois par ressource", [HEROS] + en_jeu("01121", "01103"), [],
       {"degats": [[VILAIN, 2]], "statuts": [[VILAIN, "Confused"]]},
       main_exclusive=["bg005", "01089"], jouer=["bg005"], payer_avec=["01089"], cibles=[VILAIN, "01121", "01103"]),
    # RR « Wild Resource » (26/10/2026) : un wild depense pour Batarangs compte pour la ligne du type que le joueur DECLARE.
    _c("bg005 Batarangs : payee avec DEUX WILD (Hellcat x2) declares [mental] + [energy] -> 2 degats, un cran Sonne ET un cran Desoriente (une ligne chacune)",
       "RR Wild Resource : « they may specify which resource type it is being used as » ; une ligne [energy] + une ligne [mental]",
       [HEROS] + en_jeu("01121", "01103"), [],
       {"degats": [[VILAIN, 2]], "statuts": [[VILAIN, "Stunned"], [VILAIN, "Confused"]]},
       main_exclusive=["bg005", "01020", "01020"], jouer=["bg005"], payer_avec=["01020", "01020"], cibles=[VILAIN, VILAIN, VILAIN],
       preferer_option="BY"),
    _c("bg005 Batarangs : payee avec DEUX WILD (Hellcat x2) declares [physical] x2 -> 2 degats + 2 lignes [physical] = 6 sur Rhino",
       "RR Wild Resource : le joueur declare le type, ici physique deux fois",
       [HEROS], [], {"degats": [[VILAIN, 6]]},
       main_exclusive=["bg005", "01020", "01020"], jouer=["bg005"], payer_avec=["01020", "01020"], cibles=[VILAIN, VILAIN, VILAIN],
       preferer_option="RR"),
    # ============================================================ bg006 Master Plan
    _c("bg006 Master Plan : option 1, +2 THW sur le heros (THW 2 -> 4) jusqu'a la fin du round",
       "« That character gets +2 to a basic power for its next use » (ecart documente : dure jusqu'a la fin du round). ⚠ Le `declencher` du harnais "
       "part AVANT `jouer` : on lit donc la stat de l'identite apres la carte",
       [HEROS], [], {"bg_stats": {"thwart": 4}},
       main_exclusive=["bg006"], jouer=["bg006"], cibles=[VILAIN], preferer_option="+2 THW"),
    _c("bg006 Master Plan : option 1, TEMOIN, sans la carte le THW du heros reste a 2", "stat imprimee", [HEROS], [],
       {"bg_stats": {"thwart": 2}}, main_exclusive=["01090"]),
    _c("bg006 Master Plan : option 2, les ressources generees sont [wild] jusqu'a la fin du round -> Batarangs en Strength RR : le joueur declare [energy] x2 -> 2 degats + 2 lignes [energy] (Sonne), aucune ligne [physical]",
       "« those resources are considered [wild] resources instead. Draw a card. » ; RR Wild Resource : chaque wild compte pour le type declare (ici energie, deux fois) : 2 degats seulement (aucune ligne [physical]) et Rhino sonne",
       [HEROS], [], {"degats": [[VILAIN, 2]], "statuts": [[VILAIN, "Stunned"]]},
       main_exclusive=["bg006", "bg005", "01090"], jouer=["bg006", "bg005"], payer_avec=["01090"], cibles=[VILAIN],
       preferer_option=["Until the end of the round", "YY"]),
    _c("bg006 Master Plan : option 2 pioche une carte",
       "« Draw a card »", [HEROS], [], {"taille_main": 1}, main_exclusive=["bg006"], jouer=["bg006"], cibles=[VILAIN],
       preferer_option="Until the end of the round"),
    # ============================================================ bg007 Calculated Counter
    _c("bg007 Calculated Counter : la carte revelee est annulee et defaussee ; payee en [energy], X = 2 boosts -> 2 degats a un ennemi",
       "« cancel the effects of that card and discard it ... deal X damage to an enemy » (Shadow of the Past : 2 icones de boost)",
       [HEROS, "Puzzle.PutIntoPlay('01182')"], ["Puzzle.Reveal('01190')"], {"degats": [["01182", 2]], "defausse_rencontre": ["01190"]},
       main_exclusive=["bg007", "01088"], jouer=["bg007"], payer_avec=["01088"], cibles=["01182"],
       preferer_option="Deal 2 damage"),
    _c("bg007 Calculated Counter : TEMOIN, payee en [physical] -> carte annulee mais AUCUN degat",
       "la branche X exige « only [energy] »", [HEROS, "Puzzle.PutIntoPlay('01182')"], ["Puzzle.Reveal('01190')"],
       {"degats": [["01182", 0]], "defausse_rencontre": ["01190"]},
       main_exclusive=["bg007", "01090"], jouer=["bg007"], payer_avec=["01090"], cibles=["01182"]),
    # ============================================================ bg008 The Clocktower
    _c("bg008 The Clocktower : Action d'alter ego, s'incline -> 1 carte piochee et 1 menace retiree",
       "« Alter-Ego Action: Exhaust this card -> draw 1 card and remove 1 threat from a scheme »",
       ["Puzzle.SetThreat('01097b', 3)"] + en_jeu("bg008"), ["Puzzle.Action('bg008')"],
       {"exhausted": ["bg008"], "menace": [[COMPLOT, 2]], "taille_main": 1}, main_exclusive=[], cibles=[COMPLOT]),
    _c("bg008 The Clocktower : Interruption de heros, une carte payee uniquement en [mental] -> s'incline, 2 menaces retirees",
       "« When you pay for a card using only [mental] resources, exhaust this card -> remove up to 2 threat »",
       [HEROS, "Puzzle.SetThreat('01097b', 5)"] + en_jeu("bg008"), [], {"exhausted": ["bg008"], "menace": [[COMPLOT, 3]]},
       main_exclusive=["bg009", "01089"], jouer=["bg009"], payer_avec=["01089"], cibles=[COMPLOT]),
    _c("bg008 The Clocktower : TEMOIN, payee en [physical] -> reste prete, menace inchangee",
       "la fenetre exige « only [mental] »", [HEROS, "Puzzle.SetThreat('01097b', 5)"] + en_jeu("bg008"), [],
       {"pret": ["bg008"], "menace": [[COMPLOT, 5]]},
       main_exclusive=["bg009", "01090"], jouer=["bg009"], payer_avec=["01090"], cibles=[COMPLOT]),
    # ============================================================ bg009 James Gordon
    _c("bg009 James Gordon : une carte payee uniquement en [physical] -> 2 degats a un ennemi",
       "« using only [physical] resources, exhaust James Gordon -> deal 2 damage to an enemy » (Armored Suit cout 2 payee RR)",
       [HEROS, "Puzzle.PutIntoPlay('01182')"] + en_jeu("bg009"), [], {"exhausted": ["bg009"], "degats": [["01182", 2]]},
       main_exclusive=["bg010", "01090"], jouer=["bg010"], payer_avec=["01090"], cibles=["01182"]),
    _c("bg009 James Gordon : une carte payee uniquement en [energy] -> 1 carte piochee",
       "« using only [energy] resources, exhaust James Gordon -> draw a card » (Grapple Line cout 1 payee YY)",
       [HEROS] + en_jeu("bg009"), [], {"exhausted": ["bg009"], "taille_main": 1},
       main_exclusive=["bg011", "01088"], jouer=["bg011"], payer_avec=["01088"], cibles=[]),
    # ============================================================ bg010 Armored Suit
    _c("bg010 Armored Suit : +3 PV maximum",
       "« You get +3 hit points »", [HEROS] + en_jeu("bg010"), [], {"pv_max": [["bg001a", 13]]}, main_exclusive=["01090"]),
    _c("bg010 Armored Suit : Interruption de heros, s'incline -> 1 des degats d'une attaque est empeche",
       "« When you would take any amount of damage, exhaust Armored Suit -> prevent 1 of that damage » (Rhino ATQ 2 -> 1 degat)",
       [HEROS] + en_jeu("bg010"), ["Puzzle.Damage('bg001a', 2)"], {"degats_identite": 1, "exhausted": ["bg010"]}, main_exclusive=["01090"],
       accepter_choix=True),
    # ============================================================ bg011 Grapple Line
    _c("bg011 Grapple Line : payee avec une ressource [physical] -> un compteur recon",
       "« If you paid for this card using a [physical] resource, place a recon counter »", [HEROS], [],
       {"compteurs": [["bg011", "recon", 1]]}, main_exclusive=["bg011", "01090"], jouer=["bg011"], payer_avec=["01090"]),
    _c("bg011 Grapple Line : TEMOIN, payee en [energy] -> aucun compteur",
       "pas de [physical] payee : pas de recon", [HEROS], [], {"compteurs": [["bg011", "recon", 0]]},
       main_exclusive=["bg011", "01088"], jouer=["bg011"], payer_avec=["01088"]),
    _c("bg011 Grapple Line : Action avec un compteur recon -> redresse un personnage, pioche, se defausse",
       "« Discard Grapple Line -> ready a friendly character. If there is a recon counter, draw a card »",
       [HEROS, "Puzzle.Exhaust('bg001a')"] + en_jeu("bg011") + ["Puzzle.Counter('bg011', 'recon', 1)"], ["Puzzle.Action('bg011')"],
       {"pret": ["bg001a"], "hors_jeu": ["bg011"], "taille_main": 1}, main_exclusive=[], cibles=["bg001a"]),
    _c("bg011 Grapple Line : TEMOIN, sans compteur recon -> redresse mais ne pioche pas",
       "le « draw a card » exige le compteur", [HEROS, "Puzzle.Exhaust('bg001a')"] + en_jeu("bg011"), ["Puzzle.Action('bg011')"],
       {"pret": ["bg001a"], "hors_jeu": ["bg011"], "taille_main": 0}, main_exclusive=[], cibles=["bg001a"]),
    # ============================================================ bg012 Utility Belt
    _c("bg012 Utility Belt : prete, en fin de phase la pioche donne 6 cartes",
       "« if this card is ready, Batgirl gets +1 hand size » (mesure par une vraie pioche)",
       [HEROS] + en_jeu("bg012"), ["Puzzle.EmptyHand()", "Puzzle.PlayersEndPhaseDraw()", "Puzzle.EndPlayerPhase()"], {"taille_main": 6}),
    _c("bg012 Utility Belt : TEMOIN, inclinee, la pioche de fin de phase donne 5 cartes",
       "« if this card is ready » : inclinee, plus de +1", [HEROS] + en_jeu("bg012") + ["Puzzle.Exhaust('bg012')"],
       ["Puzzle.EmptyHand()", "Puzzle.PlayersEndPhaseDraw()", "Puzzle.EndPlayerPhase()"], {"taille_main": 5}),
    _c("bg012 Utility Belt : Hero Action, la ceinture s'incline -> l'evenement suivant coute 1 de moins (Applying Pressure cout 2 payee par UNE ressource)",
       "« Hero Action: When you would play an event, exhaust this card -> reduce the cost of that event by 1 » : une ACTION facultative "
       "(RR « Action ») : on l'active, puis on joue l'evenement avec une seule ressource",
       [HEROS, "Puzzle.SetThreat('01097b', 5)"] + en_jeu("bg012"), ["Puzzle.Action('bg012', 'HeroAction')"],
       {"exhausted": ["bg012"], "menace": [[COMPLOT, 1]]},
       main_exclusive=["bg004", "01020"], jouer=["bg004"], payer_avec=["01020"], cibles=[COMPLOT]),
    _c("bg012 Utility Belt : REFUS, l'action n'est pas activee -> l'evenement est paye plein (2 ressources) et la ceinture reste PRETE",
       "RR « Action » : une action est facultative ; le joueur garde la ceinture prete pour le +1 de taille de main de sa 2e capacite",
       [HEROS, "Puzzle.SetThreat('01097b', 5)"] + en_jeu("bg012"), [],
       {"pret": ["bg012"], "menace": [[COMPLOT, 1]]},
       main_exclusive=["bg004", "01088", "01088"], jouer=["bg004"], payer_avec=["01088", "01088"], cibles=[COMPLOT]),
    _c("bg012 Utility Belt : « Hero » Action, en forme d'ALTER EGO l'action n'est pas offerte (la ceinture reste prete)",
       "RR « Triggered Abilities » : un « Hero » ne peut etre utilise qu'en forme heros",
       [CIVIL] + en_jeu("bg012"), [], {"pret": ["bg012"]},
       declencher_tolerant=["Puzzle.Action('bg012', 'HeroAction')"]),
    _c("bg012 Utility Belt : TEMOIN, sans Utility Belt la meme carte coute 2 et n'est pas payable avec UNE ressource",
       "cout plein", [HEROS, "Puzzle.SetThreat('01097b', 5)"], [], {"menace": [[COMPLOT, 5]]},
       main_exclusive=["bg004", "01020"], jouer=["bg004"], payer_avec=["01020"], cibles=[COMPLOT]),
    _c("bg012 Utility Belt : ORDRE, l'Action jouee APRES l'evenement ne le reduit pas (cout plein 2, une seule ressource : l'evenement n'est pas joue)",
       "mesure de l'ordre reel (26/10/2026) : `declencher` tourne AVANT `jouer` (cas precedent : reduction), `declencher_apres` APRES : l'Action de la "
       "ceinture arme le PROCHAIN evenement, elle ne rembourse pas celui qui vient d'etre joue",
       [HEROS, "Puzzle.SetThreat('01097b', 5)"] + en_jeu("bg012"), [],
       {"exhausted": ["bg012"], "menace": [[COMPLOT, 5]]},
       main_exclusive=["bg004", "01020"], jouer=["bg004"], payer_avec=["01020"], cibles=[COMPLOT],
       declencher_apres=["Puzzle.Action('bg012', 'HeroAction')"]),
    # ============================================================ cas ajoutes le 26/10/2026 (consigne du coordinateur)
    _c("bg001a The Oracle : limite UNE fois par round (temoin d'epuisement) : Applying Pressure change, Batarangs NON (4 degats, pas 8)",
       "« Limit once per round » : la 1re carte jouee voit son icone changee ; la 2e, meme proposition, n'est plus offerte (sans limite : 2 + 2 + 4 = 8)",
       [HEROS, "Puzzle.SetThreat('01097b', 6)"], [], {"degats": [[VILAIN, 4]], "menace": [[COMPLOT, 2]]},
       main_exclusive=["bg004", "bg005", "01088", "01088"], jouer=["bg004", "bg005"], payer_avec=["01088", "01088"],
       cibles=[COMPLOT, VILAIN], preferer_option="Change [physical] to [energy]"),
    _c("bg015 Black Mask : SCH 0 -> le joueur engage recoit une carte rencontre face cachee quand il manigance",
       "« If his SCH is 0, the engaged player is dealt a facedown encounter card when Black Mask schemes »",
       [HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01190')", "Puzzle.EmptyHand()", "Puzzle.CreateHandCards('01090')",
        "Puzzle.PutIntoPlay('bg015')"], ["Puzzle.Scheme('bg015')"], {"carte_du_surge": "01190"}),
    _c("bg015 Black Mask : TEMOIN, SCH 1 (une carte [mental] en main) -> aucune carte rencontre donnee",
       "la carte face cachee n'est donnee qu'a SCH 0",
       [HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01190')", "Puzzle.EmptyHand()", "Puzzle.CreateHandCards('01089')",
        "Puzzle.PutIntoPlay('bg015')"], ["Puzzle.Scheme('bg015')"], {"dans_deck_rencontre": ["01190"]}),
    _c("bg018 Psychological Torture : deck epuise sans 3 cartes de meme ressource -> le vilain manigance",
       "« If you run out of cards in your deck this way, the villain schemes »",
       [HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01057', '01088')"], ["Puzzle.Reveal('bg018')"],
       {"menace_min": [[COMPLOT, 1]]}, main_exclusive=["01057"]),
    # ============================================================ bg013 Recalled Trauma
    _c("bg013 Recalled Trauma : branche 1, Barbara s'incline -> l'obligation est retiree de la partie",
       "« Exhaust Barbara Gordon -> remove Recalled Trauma from the game »", [], ["Puzzle.Reveal('bg013')"],
       {"exhausted": ["bg001b"]}, main_exclusive=[], preferer_option="Exhaust Barbara Gordon"),
    _c("bg013 Recalled Trauma : branche 2, les ressources n'ont plus de type -> Applying Pressure payee RR n'inflige PAS les 2 degats",
       "« all cards you spend as resources are considered to have no resource type » (provisoire : drapeau lu par les helpers du pack)",
       [HEROS, "Puzzle.SetThreat('01097b', 6)", "Puzzle.PutIntoPlay('01182')"], ["Puzzle.Reveal('bg013')", HEROS],
       {"menace": [[COMPLOT, 2]], "degats": [["01182", 0]]},
       main_exclusive=["bg004", "01090"], jouer=["bg004"], payer_avec=["01090"], cibles=[COMPLOT, "01182"],
       preferer_option="Cards you spend as resources"),
    # ============================================================ bg014 Return of the Mask
    _c("bg014 Return of the Mask : revelee -> Black Mask entre en jeu, chaque joueur subit 1 degat indirect",
       "« Find the Black Mask minion. Reveal him ... each player takes 1 indirect damage »",
       [HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('bg015', '01098', '01098')"], ["Puzzle.Reveal('bg014')"],
       {"en_jeu": ["bg014", "bg015"], "degats_identite": 1}, main_exclusive=["01090"]),
    # ============================================================ bg015 Black Mask
    _c("bg015 Black Mask : SCH = nombre de cartes [mental] imprimees dans la main du joueur engage (2 -> SCH 2)",
       "« SCH is equal to the number of cards with a printed [mental] resource in the engaged player's hand »",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.CreateHandCards('01089', '01089', '01090')", "Puzzle.PutIntoPlay('bg015')"], [],
       {"attributs_carte": [["bg015", "scheme", 2]]}),
    _c("bg015 Black Mask : SCH 0 sans carte [mental] en main",
       "aucune carte [mental] : SCH 0", [HEROS, "Puzzle.PutIntoPlay('bg015')"], [], {"attributs_carte": [["bg015", "scheme", 0]]},
       main_exclusive=["01090"]),
    # ============================================================ bg016 The Reaper
    _c("bg016 The Reaper : apres la phase du vilain, le joueur engage defausse une carte [energy] imprimee",
       "« must discard a card from their hand with a printed [energy] resource »", [HEROS, "Puzzle.PutIntoPlay('bg016')"],
       ["Puzzle.EndVillainPhase()"], {"defausse_joueur": 1, "menace": [[COMPLOT, 0]]}, main_exclusive=["01088"], cibles=["01088"]),
    _c("bg016 The Reaper : sans carte [energy] en main -> 1 menace sur le complot principal",
       "« If no card was discarded this way, place 1 threat on the main scheme »", [HEROS, "Puzzle.PutIntoPlay('bg016')"],
       ["Puzzle.EndVillainPhase()"], {"menace": [[COMPLOT, 1]]}, main_exclusive=["01090"]),
    # ============================================================ bg017 Mr. Zsasz
    _c("bg017 Mr. Zsasz : au debut de la phase du vilain, le joueur engage defausse une carte [physical] imprimee",
       "« must discard a card from their hand with a [physical] printed resource »", [HEROS, "Puzzle.PutIntoPlay('bg017')"],
       ["Puzzle.BeginVillainPhase()"], {"defausse_joueur": 1, "degats_identite": 0}, main_exclusive=["01090"], cibles=["01090"]),
    _c("bg017 Mr. Zsasz : sans carte [physical] -> 2 degats indirects",
       "« that player takes 2 indirect damage »", [HEROS, "Puzzle.PutIntoPlay('bg017')"], ["Puzzle.BeginVillainPhase()"],
       {"degats_identite_min": 2}, main_exclusive=["01088"]),
    # ============================================================ bg018 Psychological Torture
    _c("bg018 Psychological Torture : defausse du dessus jusqu'a 3 cartes de meme ressource imprimee (3 [physical] au sommet)",
       "« Discard cards from the top of your deck until you have discarded 3 cards with the same printed resource type »",
       [HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01057', '01057', '01090', '01090', '01090')"],
       ["Puzzle.Reveal('bg018')"], {"defausse_joueur": 3, "taille_deck_joueur": 2}, main_exclusive=["01057"]),
    # ============================================================ bg019 Birds of a Feather
    _c("bg019 Birds of a Feather : deux Birds of Prey en jeu (Batgirl + Black Canary) -> 2 choix, 3 degats chacun",
       "« Choose X options ... X is the number of BIRD OF PREY characters in play »", [HEROS] + en_jeu("bg002"), [],
       {"degats": [[VILAIN, 6]]}, main_exclusive=["bg019", "01020", "01020"], jouer=["bg019"], payer_avec=["01020", "01020"],
       cibles=[VILAIN], preferer_option="Deal 3 damage"),
    _c("bg019 Birds of a Feather : TEMOIN, Batgirl seule (un seul personnage nomme) -> la carte n'est pas jouable",
       "« Team-Up (any combination of Batgirl, Black Canary, or Huntress) » : deux personnages nommes exiges", [HEROS], [],
       {"degats": [[VILAIN, 0]]}, main_exclusive=["bg019", "01020", "01020"], jouer=["bg019"], payer_avec=["01020", "01020"],
       cibles=[VILAIN], preferer_option="Deal 3 damage"),
]

VERIFICATIONS = r'''
def bg_etat(monde, aides):
    """Cles propres : `bg_stats` ({attribut: valeur} lus sur l'identite) ; le reste va a etat_attendu."""
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    soucis = []
    identite = aides["identite"](monde)
    for nom, valeur in (attendu.get("bg_stats") or {}).items():
        courant = getattr(identite, nom, None)
        if courant != valeur:
            soucis.append(f"{nom} = {courant} (attendu {valeur})")
    reste = {k: v for k, v in attendu.items() if k != "bg_stats"}
    copie = dict(aides); copie["cas"] = dict(cas); copie["cas"]["attendu"] = reste
    ok, message = etat_attendu(monde, copie)
    if not ok:
        soucis.append(message)
    if soucis:
        return False, " ; ".join(soucis)
    return True, message
'''
