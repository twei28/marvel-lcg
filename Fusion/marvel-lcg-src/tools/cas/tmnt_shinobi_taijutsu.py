# Cas test_capacites du pack tmnt_shinobi_taijutsu (Inkwire, TMNT Shinobi, les 20 cartes TAIJUTSU, prefixe `sh`), 17/10/2026.
# Filtre : `[sh]`. Gabarits : .planning/tmnt/shinobi-taijutsu-gabarits.md. Questions : .planning/tmnt/shinobi-taijutsu-questions.md.
#
# Conventions (comme tools/cas/tmnt_shinobi_paths.py) :
#  - Spider-Man (01001) demarre en ALTER EGO ; HEROS le met en forme heros ;
#  - aucun Path n'est necessaire : une carte Shinobi se joue sans Path (seul le deck-builder l'exige) ;
#  - Rhino 01094 (vilain du scenario `rhino`, 14 PV, ATQ 2) est la cible des attaques, 01101 Hydra Mercenary (3 PV, ATQ 1,
#    Guard) le sbire, ah016 Fin Fang Foom (ATQ 4, 4 PV) l'attaquant des cas de defense (heros INCLINE : pas de defense) ;
#  - `main_exclusive` vide la main (APRES la mise en place) : chaque cas sait avec QUOI il paie
#    (01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR) ;
#  - deck rencontre bourre de « I'm Tough » (01105, sans icone de boost) : aucune carte rencontre ne brouille la mesure ;
#  - evenements officiels servant de MATIERE de paiement : 01087 Haymaker (ATTACK, cout 2), 01003 Backflip (DEFENSE/SKILL,
#    cout 0), 01005 Swinging Web Kick (ATTACK, cout 3), 05005 Wiggle Room (DEFENSE, cout 0), sh0NN du pack (Toss DEFENSE+THWART...) ;
#    ⚠ dans un cas d'ATTAQUE, une carte DEFENSE servant de paiement ne doit pas etre une Interruption que le pilote jouerait a la
#    place (Backflip, Wiggle Room) : on prend 09015 Desperate Defense (« When your hero defends... », cout 1, ressource [energy]),
#    qui n'est PAS offerte quand le heros est incline.
SC = "rhino"
HEROS = "Puzzle.ChangeForm('01001b')"
COMPLOT = "01097b"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105', '01105', '01105')"]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    # ⚠ `main_exclusive: []` NE VIDE RIEN (liste vide = faux dans le harnais) : une main vide se demande par `EmptyHand`.
    if cle.get("main_exclusive") == []:
        cle.pop("main_exclusive")
        mise = list(mise) + ["Puzzle.EmptyHand()"]
    if not cle.pop("avec_boost", False):
        mise = SANS_BOOST + list(mise)
    cas = {"nom": "[sh] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": list(mise), "declencher": list(declencher),
           "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = []


def DISC(*ids):
    """Defausse du joueur EXACTEMENT egale a `ids` (a mettre dans `declencher`, APRES le vidage de la main par
    `main_exclusive` qui verse la main de depart de Spider-Man dans la defausse : Swinging Web Kick (ATTACK), For Justice!
    (THWART)... fausseraient tout cas qui lit la defausse)."""
    return ["Puzzle.EmptyPlayerDiscardPile()", "Puzzle.CreatePlayerDiscardPile(" + ", ".join(repr(i) for i in ids) + ")"]

# ========================================================================= sh001 Raising Block
FFF = "ah016"   # Fin Fang Foom : ATQ 4, 4 PV (attaquant des cas de defense)
CAS += [
    _c("sh001 Raising Block : Interruption de defense, attaque de 4 : previent EXACTEMENT 3, le heros prend 1",
       "« When you would take any amount of damage from an attack, prevent 3 of that damage » : Fin Fang Foom (ATQ 4) attaque "
       "un heros INCLINE (donc sans defense) : 4 - 3 = 1 degat ; cout 0, la carte part en defausse",
       [HEROS, "Puzzle.Exhaust('01001a')", f"Puzzle.PutIntoPlay('{FFF}')"], [f"Puzzle.Attack('{FFF}')"],
       {"degats_identite": 1, "defausse": ["sh001"]}, main_exclusive=["sh001"]),
    _c("sh001 Raising Block : attaque de 2 seulement (Shocker) : prevent 3 ne depasse pas les degats, 0 degat",
       "« prevent 3 OF THAT damage » : au plus les degats de l'attaque (2), la carte est jouee quand meme",
       [HEROS, "Puzzle.Exhaust('01001a')", "Puzzle.PutIntoPlay('01103')"], ["Puzzle.Attack('01103')"],
       {"degats_identite": 0, "defausse": ["sh001"]}, main_exclusive=["sh001"]),
    _c("sh001 Raising Block : TEMOIN, des degats qui ne viennent PAS d'une attaque ne sont pas prevenus (carte non offerte)",
       "« from an attack » : 3 degats directs (hors attaque) : l'Interruption n'est pas proposee, la carte reste en main",
       [HEROS], ["Puzzle.Damage('01001a', 3)"], {"degats_identite": 3, "en_main": ["sh001"]}, main_exclusive=["sh001"]),
    _c("sh001 Raising Block : TEMOIN, forme ALTER-EGO : « Hero Interrupt » n'est pas offerte, Peter Parker prend les 4 degats",
       "Hero Interrupt : forme heros seulement ; Fin Fang Foom attaque Peter Parker (alter-ego, pret)",
       [f"Puzzle.PutIntoPlay('{FFF}')"], [f"Puzzle.Attack('{FFF}')"],
       {"degats_identite": 4, "en_main": ["sh001"]}, main_exclusive=["sh001"]),
]

CAS += [
    _c("sh001 Raising Block : depensee pour payer un evenement DEFENSE (Desperate Defense 09015) : pioche 1 carte (Reponse)",
       "« After you spend this card to pay for a DEFENSE event, draw 1 card » : le heros pret defend (DEF 3 + 2 de Desperate Defense = 5 > ATQ 4 : "
       "aucun degat) ; Raising Block (cout 0, ressource [physical]) paie les 1 ressource ; main vide + 1 pioche",
       [HEROS, f"Puzzle.PutIntoPlay('{FFF}')"], [f"Puzzle.Attack('{FFF}', defender='01001a')"],
       {"degats_identite": 0, "defausse": ["09015", "sh001"], "taille_main": 1},
       main_exclusive=["09015", "sh001"], payer_avec=["sh001"]),
    _c("sh001 Raising Block : TEMOIN, Desperate Defense payee par Strength : Raising Block reste en main, aucune pioche",
       "la Reponse est portee par la carte DEPENSEE : sans elle dans le paiement, rien",
       [HEROS, f"Puzzle.PutIntoPlay('{FFF}')"], [f"Puzzle.Attack('{FFF}', defender='01001a')"],
       {"degats_identite": 0, "defausse": ["09015", "01090"], "en_main": ["sh001"], "taille_main": 1},
       main_exclusive=["09015", "sh001", "01090"], payer_avec=["01090"]),
    _c("sh001 Raising Block : TEMOIN, depensee pour payer un evenement ATTACK (Stiff Jab) : aucune pioche",
       "« a DEFENSE event » : un evenement ATTACK ne convient pas ; Stiff Jab (cout 1) payee par Raising Block",
       [HEROS], [],
       {"degats": [["01094", 2]], "defausse": ["sh003", "sh001"], "taille_main": 0},
       main_exclusive=["sh003", "sh001"], payer_avec=["sh001"], jouer=["sh003"], cibles=["01094"]),
]

# ========================================================================= sh002 Foot Sweep
CAS += [
    _c("sh002 Foot Sweep : retire 3 menaces du complot principal, payee SANS evenement ATTACK (Strength RR) : rien ne revient",
       "« Remove 3 threat from a scheme. Return each ATTACK event ... that you used to pay » : cout 2 paye par la seule ressource "
       "Strength (RR) : aucun evenement a rendre ; menace 5 -> 2",
       [HEROS], [f"Puzzle.SetThreat('{COMPLOT}', 5)"],
       {"menace": [[COMPLOT, 2]], "defausse": ["sh002"], "taille_main": 0},
       main_exclusive=["sh002", "01090"], payer_avec=["01090"], jouer=["sh002"], cibles=[COMPLOT]),
    _c("sh002 Foot Sweep : payee avec un evenement ATTACK (Haymaker 01087 + Strength) : Haymaker REVIENT en main",
       "Haymaker (ATTACK) depense comme ressource puis rendu a la main ; Strength (ressource) reste en defausse ; menace 5 -> 2",
       [HEROS], [f"Puzzle.SetThreat('{COMPLOT}', 5)"],
       {"menace": [[COMPLOT, 2]], "defausse": ["sh002", "01090"], "en_main": ["01087"], "taille_main": 1},
       main_exclusive=["sh002", "01087", "01090"], payer_avec=["01087", "01090"], jouer=["sh002"], cibles=[COMPLOT]),
    _c("sh002 Foot Sweep : payee avec un evenement DEFENSE (Backflip) et un ATTACK (Haymaker) : SEUL l'ATTACK revient",
       "« each ATTACK event » : Backflip (DEFENSE/SKILL, cout 0, ressource R) paie aussi mais reste en defausse",
       [HEROS], [f"Puzzle.SetThreat('{COMPLOT}', 5)"],
       {"menace": [[COMPLOT, 2]], "defausse": ["sh002", "01003"], "en_main": ["01087"], "absent_main": ["01003"], "taille_main": 1},
       main_exclusive=["sh002", "01087", "01003"], payer_avec=["01087", "01003"], jouer=["sh002"], cibles=[COMPLOT]),
    _c("sh002 Foot Sweep : payee avec DEUX evenements ATTACK (Haymaker + Swinging Web Kick) : les DEUX reviennent",
       "« each ATTACK event » : pas un seul ; deux evenements ATTACK de 1 ressource chacun couvrent le cout 2",
       [HEROS], [f"Puzzle.SetThreat('{COMPLOT}', 5)"],
       {"menace": [[COMPLOT, 2]], "defausse": ["sh002"], "en_main": ["01087", "01005"], "taille_main": 2},
       main_exclusive=["sh002", "01087", "01005"], payer_avec=["01087", "01005"], jouer=["sh002"], cibles=[COMPLOT]),
]

# ========================================================================= sh003 Stiff Jab
CAS += [
    _c("sh003 Stiff Jab : 2 degats a Rhino, payee SANS evenement ATTACK (Strength RR) : aucune hebetude proposee",
       "« Deal 2 damage to an enemy. If you paid ... with an ATTACK event, you may daze that enemy » : cout 1 paye par des ressources",
       [HEROS], [], {"degats": [["01094", 2]], "statuts_absents": [["01094", "Dazed"]], "defausse": ["sh003"]},
       main_exclusive=["sh003", "01090"], payer_avec=["01090"], jouer=["sh003"], cibles=["01094"]),
    _c("sh003 Stiff Jab : payee avec un evenement ATTACK (Haymaker 01087) : Rhino est HEBETE (option « Daze » acceptee)",
       "Haymaker (ATTACK, 1 ressource) paie le cout 1 : 2 degats puis Dazed",
       [HEROS], [], {"degats": [["01094", 2]], "statuts": [["01094", "Dazed"]], "defausse": ["sh003", "01087"]},
       main_exclusive=["sh003", "01087"], payer_avec=["01087"], jouer=["sh003"], cibles=["01094"]),
    _c("sh003 Stiff Jab : « you MAY daze » : la branche « Decline » est refusable, Rhino reste sain",
       "meme paiement, option « Decline » : 2 degats, AUCUN statut",
       [HEROS], [], {"degats": [["01094", 2]], "statuts_absents": [["01094", "Dazed"]], "defausse": ["sh003", "01087"]},
       main_exclusive=["sh003", "01087"], payer_avec=["01087"], jouer=["sh003"], cibles=["01094"], preferer_option="Decline"),
    _c("sh003 Stiff Jab : payee avec un evenement DEFENSE (Backflip 01003) : pas d'hebetude",
       "seul un evenement ATTACK donne le bonus ; Backflip (DEFENSE/SKILL) ne compte pas",
       [HEROS], [], {"degats": [["01094", 2]], "statuts_absents": [["01094", "Dazed"]], "defausse": ["sh003", "01003"]},
       main_exclusive=["sh003", "01003"], payer_avec=["01003"], jouer=["sh003"], cibles=["01094"]),
]

# ========================================================================= sh005 Double Kick
_DK = dict(main_exclusive=None)  # (place-holder lisible : chaque cas donne sa main)
CAS += [
    _c("sh005 Double Kick : 2 degats a Rhino ET 2 menaces retirees, payee par des ressources seules : AUCUNE pioche",
       "« Deal 2 damage to an enemy and remove 2 threat from a scheme » : deux effets sans fleche ; cout 2 paye par Strength (RR) : "
       "ni evenement DEFENSE ni THWART, la main reste vide",
       [HEROS], [f"Puzzle.SetThreat('{COMPLOT}', 5)"],
       {"degats": [["01094", 2]], "menace": [[COMPLOT, 3]], "defausse": ["sh005", "01090"], "taille_main": 0},
       main_exclusive=["sh005", "01090"], payer_avec=["01090"], jouer=["sh005"], cibles=["01094", COMPLOT]),
    _c("sh005 Double Kick : payee avec un evenement DEFENSE (Backflip + Strength) : pioche 1 carte",
       "puce « A DEFENSE event, draw 1 card » : Backflip (DEFENSE) depense comme ressource ; les deux effets de base partent aussi",
       [HEROS], [f"Puzzle.SetThreat('{COMPLOT}', 5)"],
       {"degats": [["01094", 2]], "menace": [[COMPLOT, 3]], "defausse": ["sh005", "01003", "01090"], "taille_main": 1},
       main_exclusive=["sh005", "01003", "01090"], payer_avec=["01003", "01090"], jouer=["sh005"], cibles=["01094", COMPLOT]),
    _c("sh005 Double Kick : payee avec un evenement THWART (Sideswipe sh019 + Strength) : pioche 1 carte",
       "puce « A THWART event, draw 1 card » : Sideswipe (THWART, cout 0, ressource [mental]) depense comme ressource",
       [HEROS], [f"Puzzle.SetThreat('{COMPLOT}', 5)"],
       {"degats": [["01094", 2]], "menace": [[COMPLOT, 3]], "defausse": ["sh005", "sh019", "01090"], "taille_main": 1},
       main_exclusive=["sh005", "sh019", "01090"], payer_avec=["sh019", "01090"], jouer=["sh005"], cibles=["01094", COMPLOT]),
    _c("sh005 Double Kick : payee avec un evenement ATTACK seul (Haymaker + Strength) : AUCUNE pioche",
       "ni DEFENSE ni THWART : les deux puces sont fausses",
       [HEROS], [f"Puzzle.SetThreat('{COMPLOT}', 5)"],
       {"degats": [["01094", 2]], "defausse": ["sh005", "01087", "01090"], "taille_main": 0},
       main_exclusive=["sh005", "01087", "01090"], payer_avec=["01087", "01090"], jouer=["sh005"], cibles=["01094", COMPLOT]),
    _c("sh005 Double Kick : DEUX evenements DEFENSE (Backflip + Wiggle Room) ne donnent qu'UNE pioche (« A DEFENSE event »)",
       "la puce n'est pas « each » : deux evenements du meme trait ne repiochent pas ; Backflip et Wiggle Room valent 1 ressource chacun",
       [HEROS], [f"Puzzle.SetThreat('{COMPLOT}', 5)"],
       {"degats": [["01094", 2]], "defausse": ["sh005", "01003", "05005"], "taille_main": 1},
       main_exclusive=["sh005", "01003", "05005"], payer_avec=["01003", "05005"], jouer=["sh005"], cibles=["01094", COMPLOT]),
    _c("sh005 Double Kick : un evenement DEFENSE + THWART (Toss sh009) satisfait LES DEUX puces : pioche 2 (lecture litterale, Q-T3)",
       "Toss porte les traits DEFENSE et THWART : « A DEFENSE event » ET « A THWART event » sont vraies ; cout 2 = Toss (1) + Strength",
       [HEROS], [f"Puzzle.SetThreat('{COMPLOT}', 5)"],
       {"degats": [["01094", 2]], "defausse": ["sh005", "sh009", "01090"], "taille_main": 2},
       main_exclusive=["sh005", "sh009", "01090"], payer_avec=["sh009", "01090"], jouer=["sh005"], cibles=["01094", COMPLOT]),
]

# ========================================================================= sh006 Flying Kick
CAS += [
    _c("sh006 Flying Kick : 4 degats a Rhino, payee par des ressources seules : AUCUNE pioche",
       "« Draw 1 card for each THWART event used to pay » : zero evenement THWART, zero carte",
       [HEROS], [], {"degats": [["01094", 4]], "defausse": ["sh006", "01090"], "taille_main": 0},
       main_exclusive=["sh006", "01090"], payer_avec=["01090"], jouer=["sh006"], cibles=["01094"]),
    _c("sh006 Flying Kick : payee avec UN evenement THWART (Sideswipe + Strength) : pioche 1",
       "un evenement THWART depense = 1 carte",
       [HEROS], [], {"degats": [["01094", 4]], "defausse": ["sh006", "sh019", "01090"], "taille_main": 1},
       main_exclusive=["sh006", "sh019", "01090"], payer_avec=["sh019", "01090"], jouer=["sh006"], cibles=["01094"]),
    _c("sh006 Flying Kick : payee avec DEUX evenements THWART (Sideswipe + Foot Sweep) : pioche 2",
       "« for EACH » : un nombre ; chacun vaut 1 ressource, ensemble le cout 2",
       [HEROS], [], {"degats": [["01094", 4]], "defausse": ["sh006", "sh019", "sh002"], "taille_main": 2},
       main_exclusive=["sh006", "sh019", "sh002"], payer_avec=["sh019", "sh002"], jouer=["sh006"], cibles=["01094"]),
    _c("sh006 Flying Kick : payee avec un evenement DEFENSE (Backflip + Strength) : AUCUNE pioche",
       "seul le trait THWART compte",
       [HEROS], [], {"degats": [["01094", 4]], "defausse": ["sh006", "01003", "01090"], "taille_main": 0},
       main_exclusive=["sh006", "01003", "01090"], payer_avec=["01003", "01090"], jouer=["sh006"], cibles=["01094"]),
    _c("sh006 Flying Kick : un evenement DEFENSE + THWART (Toss) ne compte qu'UNE fois : pioche 1",
       "Toss est UN evenement : une carte, pas deux (un par trait)",
       [HEROS], [], {"degats": [["01094", 4]], "defausse": ["sh006", "sh009", "01090"], "taille_main": 1},
       main_exclusive=["sh006", "sh009", "01090"], payer_avec=["sh009", "01090"], jouer=["sh006"], cibles=["01094"]),
]

# ========================================================================= sh007 Trading Blows
CAS += [
    _c("sh007 Trading Blows : apres une attaque de 4 subie, 2 degats a l'attaquant, payee SANS evenement DEFENSE : aucun statut",
       "« After you take damage from an enemy attack, deal 2 damage to that enemy » : Fin Fang Foom (ATQ 4) frappe le heros incline ; "
       "Strength paie le cout 1 ; l'attaquant prend 2 (PV 4) ; ni etourdi ni desoriente",
       [HEROS, "Puzzle.Exhaust('01001a')", f"Puzzle.PutIntoPlay('{FFF}')"], [f"Puzzle.Attack('{FFF}')"],
       {"degats_identite": 4, "degats": [[FFF, 2]], "statuts_absents": [[FFF, "Stunned"], [FFF, "Confused"]],
        "defausse": ["sh007", "01090"]},
       main_exclusive=["sh007", "01090"], payer_avec=["01090"]),
    _c("sh007 Trading Blows : payee avec un evenement DEFENSE (Desperate Defense) : l'attaquant est ETOURDI (premier choix « Stun »)",
       "« If you paid for this card with a DEFENSE event, stun or confuse that enemy » : Desperate Defense (1 ressource) paie le cout 1",
       [HEROS, "Puzzle.Exhaust('01001a')", f"Puzzle.PutIntoPlay('{FFF}')"], [f"Puzzle.Attack('{FFF}')"],
       {"degats": [[FFF, 2]], "statuts": [[FFF, "Stunned"]], "statuts_absents": [[FFF, "Confused"]],
        "defausse": ["sh007", "09015"]},
       main_exclusive=["sh007", "09015"], payer_avec=["09015"], choisir_option=["Trading_Blows"]),
    _c("sh007 Trading Blows : meme paiement, option « Confuse » : l'attaquant est DESORIENTE",
       "la seconde branche du « stun or confuse » est atteignable",
       [HEROS, "Puzzle.Exhaust('01001a')", f"Puzzle.PutIntoPlay('{FFF}')"], [f"Puzzle.Attack('{FFF}')"],
       {"degats": [[FFF, 2]], "statuts": [[FFF, "Confused"]], "statuts_absents": [[FFF, "Stunned"]],
        "defausse": ["sh007", "09015"]},
       main_exclusive=["sh007", "09015"], payer_avec=["09015"], preferer_option="Confuse"),
    _c("sh007 Trading Blows : l'attaquant est DEJA desoriente : seule l'option « stun » reste, il est etourdi sans question",
       "une option impossible n'est pas offerte : le choix se resout en « stun » (un etourdi ne ferait pas l'affaire : son attaque "
       "serait annulee avant de frapper, d'ou le choix d'un attaquant desoriente)",
       [HEROS, "Puzzle.Exhaust('01001a')", f"Puzzle.PutIntoPlay('{FFF}')", f"Puzzle.Confuse('{FFF}')"], [f"Puzzle.Attack('{FFF}')"],
       {"degats": [[FFF, 2]], "statuts": [[FFF, "Stunned"], [FFF, "Confused"]], "defausse": ["sh007", "09015"]},
       main_exclusive=["sh007", "09015"], payer_avec=["09015"]),
    _c("sh007 Trading Blows : TEMOIN, des degats hors attaque ne declenchent pas la Reponse",
       "« from an enemy attack » : 3 degats directs, la carte reste en main, aucun ennemi touche",
       [HEROS, f"Puzzle.PutIntoPlay('{FFF}')"], ["Puzzle.Damage('01001a', 3)"],
       {"degats_identite": 3, "degats": [[FFF, 0]], "en_main": ["sh007"]}, main_exclusive=["sh007", "01090"]),
    _c("sh007 Trading Blows : TEMOIN, une attaque entierement paree (DEF 3 contre ATQ 2) ne donne aucun degat subi : pas de Reponse",
       "« After you TAKE damage » : le heros defend (DEF 3), Shocker (ATQ 2) ne l'atteint pas ; la carte reste en main",
       [HEROS, "Puzzle.PutIntoPlay('01103')"], ["Puzzle.Attack('01103', defender='01001a')"],
       {"degats_identite": 0, "degats": [["01103", 0]], "en_main": ["sh007"]}, main_exclusive=["sh007", "01090"]),
    _c("sh007 Trading Blows : l'attaquant (2 PV restants) est VAINCU par les 2 degats : aucun statut a donner, pas d'erreur",
       "Shocker (3 PV) a deja 1 degat : les 2 degats le vainquent ; `GiveStatus` n'est pas appele sur un mort",
       [HEROS, "Puzzle.Exhaust('01001a')", "Puzzle.PutIntoPlay('01103')", "Puzzle.Damage('01103', 1)"], ["Puzzle.Attack('01103')"],
       {"degats_identite": 2, "hors_jeu": ["01103"], "defausse": ["sh007", "09015"]},
       main_exclusive=["sh007", "09015"], payer_avec=["09015"]),
]

# ========================================================================= sh008 Drop In
CAS += [
    _c("sh008 Drop In : forme ALTER-EGO, « Action » : Peter Parker incline est REDRESSE",
       "« Action: Ready your identity » (pas Hero Action) : jouable en alter-ego ; cout 1 paye par Strength",
       ["Puzzle.Exhaust('01001b')"], [],
       {"pret": ["01001b"], "defausse": ["sh008", "01090"]},
       main_exclusive=["sh008", "01090"], payer_avec=["01090"], jouer=["sh008"]),
    _c("sh008 Drop In : forme HEROS : Spider-Man incline est REDRESSE",
       "« your IDENTITY » : le heros aussi",
       [HEROS, "Puzzle.Exhaust('01001a')"], [],
       {"pret": ["01001a"], "defausse": ["sh008", "01090"]},
       main_exclusive=["sh008", "01090"], payer_avec=["01090"], jouer=["sh008"]),
    _c("sh008 Drop In : payee avec un evenement DEFENSE (Backflip) : peut rendre un evenement ATTACK de la defausse (Haymaker)",
       "« you MAY return an ATTACK or THWART event from your discard pile » : Haymaker revient en main (premier choix accepte)",
       ["Puzzle.Exhaust('01001b')"], DISC('01087'),
       {"pret": ["01001b"], "en_main": ["01087"], "defausse": ["sh008", "01003"]},
       main_exclusive=["sh008", "01003"], payer_avec=["01003"], jouer=["sh008"]),
    _c("sh008 Drop In : meme chose avec un evenement THWART de la defausse (Sideswipe)",
       "« ATTACK OR THWART » : le trait THWART convient aussi",
       [], DISC('sh019'),
       {"en_main": ["sh019"], "defausse": ["sh008", "01003"]},
       main_exclusive=["sh008", "01003"], payer_avec=["01003"], jouer=["sh008"]),
    _c("sh008 Drop In : « you MAY » : le retour se refuse (Cancel), Haymaker reste en defausse",
       "la carte est offerte mais refusable (`MayChooseFace`)",
       [], DISC('01087'),
       {"absent_main": ["01087"], "defausse": ["sh008", "01003", "01087"]},
       main_exclusive=["sh008", "01003"], payer_avec=["01003"], jouer=["sh008"], preferer_option="Cancel"),
    _c("sh008 Drop In : un evenement DEFENSE de la defausse n'est PAS rendu (ni ATTACK ni THWART)",
       "seuls les evenements ATTACK ou THWART conviennent : la defausse ne contient qu'un DEFENSE (Wiggle Room)",
       [], DISC('05005'),
       {"absent_main": ["05005"], "defausse": ["sh008", "01003", "05005"]},
       main_exclusive=["sh008", "01003"], payer_avec=["01003"], jouer=["sh008"]),
    _c("sh008 Drop In : payee SANS evenement DEFENSE (Strength) : Haymaker reste en defausse",
       "le retour est conditionne au paiement par un evenement DEFENSE",
       [], DISC('01087'),
       {"absent_main": ["01087"], "defausse": ["sh008", "01090", "01087"]},
       main_exclusive=["sh008", "01090"], payer_avec=["01090"], jouer=["sh008"]),
]

# ========================================================================= sh009 Toss
CAS += [
    _c("sh009 Toss : attaque de 4 : previent EXACTEMENT 3 et retire 1 menace, payee par Strength : l'attaquant n'est pas hebete",
       "« prevent 3 of that damage and remove 1 threat from a scheme » : Fin Fang Foom (ATQ 4) frappe le heros incline ; menace 5 -> 4 ; "
       "aucun evenement ATTACK dans le paiement : pas de Dazed",
       [HEROS, "Puzzle.Exhaust('01001a')", f"Puzzle.PutIntoPlay('{FFF}')"],
       [f"Puzzle.SetThreat('{COMPLOT}', 5)", f"Puzzle.Attack('{FFF}')"],
       {"degats_identite": 1, "menace": [[COMPLOT, 4]], "statuts_absents": [[FFF, "Dazed"]], "defausse": ["sh009", "01090"]},
       main_exclusive=["sh009", "01090"], payer_avec=["01090"], cibles=[COMPLOT]),
    _c("sh009 Toss : payee avec un evenement ATTACK (Haymaker) : l'attaquant est HEBETE",
       "« If you paid for this card with an ATTACK event, daze that enemy » : Haymaker (1 ressource) paie le cout 1 ; « that enemy » = l'attaquant",
       [HEROS, "Puzzle.Exhaust('01001a')", f"Puzzle.PutIntoPlay('{FFF}')"],
       [f"Puzzle.SetThreat('{COMPLOT}', 5)", f"Puzzle.Attack('{FFF}')"],
       {"degats_identite": 1, "menace": [[COMPLOT, 4]], "statuts": [[FFF, "Dazed"]], "defausse": ["sh009", "01087"]},
       main_exclusive=["sh009", "01087"], payer_avec=["01087"], cibles=[COMPLOT]),
    _c("sh009 Toss : payee avec un evenement DEFENSE (Desperate Defense) : pas d'hebetude",
       "seul le trait ATTACK donne le bonus",
       [HEROS, "Puzzle.Exhaust('01001a')", f"Puzzle.PutIntoPlay('{FFF}')"],
       [f"Puzzle.SetThreat('{COMPLOT}', 5)", f"Puzzle.Attack('{FFF}')"],
       {"degats_identite": 1, "statuts_absents": [[FFF, "Dazed"]], "defausse": ["sh009", "09015"]},
       main_exclusive=["sh009", "09015"], payer_avec=["09015"], cibles=[COMPLOT]),
    _c("sh009 Toss : CONVENTION MOTEUR, aucune menace nulle part : la cible « a scheme » (menace requise) n'existe pas, la carte n'est pas offerte",
       "caracterisation (comme l'officielle 18004 Crosscounter) : le moteur impose `has_threat=True` aux cibles de manigance (ability.py), "
       "donc sans menace ni la prevention ni le reste n'est propose ; non prouve : une partie reelle pourrait vouloir prevenir quand meme",
       [HEROS, "Puzzle.Exhaust('01001a')", f"Puzzle.PutIntoPlay('{FFF}')"], [f"Puzzle.Attack('{FFF}')"],
       {"degats_identite": 4, "en_main": ["sh009"]}, main_exclusive=["sh009", "01090"], payer_avec=["01090"]),
    _c("sh009 Toss : TEMOIN, des degats hors attaque ne sont pas prevenus (carte non offerte)",
       "« from an attack » : 3 degats directs, la carte reste en main",
       [HEROS], ["Puzzle.Damage('01001a', 3)"], {"degats_identite": 3, "en_main": ["sh009"]}, main_exclusive=["sh009", "01090"]),
    _c("sh009 Toss : TEMOIN, forme ALTER-EGO : Hero Interrupt non offerte",
       "Peter Parker prend les 4 degats",
       [f"Puzzle.PutIntoPlay('{FFF}')"], [f"Puzzle.Attack('{FFF}')"],
       {"degats_identite": 4, "en_main": ["sh009"]}, main_exclusive=["sh009", "01090"]),
]

# ========================================================================= sh010 Martial Skill
MS = ["Puzzle.PutIntoPlay('sh010', under_control=True)", "Puzzle.Attach('sh010', '01001a')"]
CAS += [
    _c("sh010 Martial Skill : entre en jeu avec 2 compteurs chi (Uses) sur l'identite",
       "« Uses (2 chi counters) » : natif (`desc.Uses = \"2,chi\"`)",
       [HEROS] + MS, [], {"compteurs": [["sh010", "chi", 2]], "en_jeu": ["sh010"]}, main_exclusive=[]),
    _c("sh010 Martial Skill : apres avoir joue un evenement : s'incline, retire 1 compteur chi, pioche 1 carte",
       "« After you play an event, exhaust Martial Skill and remove 1 chi counter from it -> draw 1 card » : Sideswipe (cout 0) joue ; "
       "main vide + 1 pioche",
       [HEROS] + MS, [f"Puzzle.SetThreat('{COMPLOT}', 3)"],
       {"compteurs": [["sh010", "chi", 1]], "exhausted": ["sh010"], "taille_main": 1, "defausse": ["sh019"]},
       main_exclusive=["sh019"], jouer=["sh019"], cibles=[COMPLOT]),
    _c("sh010 Martial Skill : TEMOIN D'EPUISEMENT, un SECOND evenement dans le meme round ne repioche pas (incline)",
       "l'inclinaison est un cout : apres le premier evenement, Martial Skill est incline ; deux Sideswipe joues, UNE seule pioche, 1 compteur",
       [HEROS] + MS, [f"Puzzle.SetThreat('{COMPLOT}', 5)"],
       {"compteurs": [["sh010", "chi", 1]], "exhausted": ["sh010"], "taille_main": 1},
       main_exclusive=["sh019", "sh019"], jouer=["sh019", "sh019"], cibles=[COMPLOT]),
    _c("sh010 Martial Skill : le DERNIER compteur retire fait quitter la carte (Uses) : 2 evenements espaces d'un redressement = 2 cartes",
       "premier evenement : chi 2 -> 1, pioche 1 ; redressement ; second evenement : chi 1 -> 0, pioche 1, la carte est defaussee (Uses)",
       [HEROS] + MS, [f"Puzzle.SetThreat('{COMPLOT}', 5)"], {"hors_jeu": ["sh010"], "taille_main": 2},
       main_exclusive=["sh019", "sh019"], jouer=["sh019"], declencher_apres=["Puzzle.Ready('sh010')"], jouer_apres=["sh019"],
       cibles=[COMPLOT]),
    _c("sh010 Martial Skill : jouer un SOUTIEN (Aunt May) ne declenche rien : ce n'est pas un evenement",
       "« After you play an EVENT » : 01006 Aunt May (Soutien, cout 1) paye par Strength : aucune pioche, 2 compteurs",
       [HEROS] + MS, [], {"compteurs": [["sh010", "chi", 2]], "pret": ["sh010"], "taille_main": 0},
       main_exclusive=["01006", "01090"], payer_avec=["01090"], jouer=["01006"]),
    _c("sh010 Martial Skill : forme ALTER-EGO : « Response » nu, Drop In (Action) joue en civil declenche la pioche",
       "Peter Parker : Drop In (cout 1, paye par Strength) puis Martial Skill pioche 1",
       ["Puzzle.PutIntoPlay('sh010', under_control=True)", "Puzzle.Attach('sh010', '01001b')"], [],
       {"compteurs": [["sh010", "chi", 1]], "exhausted": ["sh010"], "taille_main": 1},
       main_exclusive=["sh008", "01090"], payer_avec=["01090"], jouer=["sh008"]),
]

# ========================================================================= sh011 Elbow Strike
CAS += [
    _c("sh011 Elbow Strike : apres une attaque de base du HEROS qui blesse Rhino : Rhino est HEBETE",
       "« After your hero makes a basic attack and damages an enemy, daze that enemy » : Spider-Man (ATQ 2) attaque Rhino ; cout 0",
       [HEROS], ["Puzzle.Attack('01001a')"],
       {"degats": [["01094", 2]], "statuts": [["01094", "Dazed"]], "defausse": ["sh011"]},
       main_exclusive=["sh011"], cibles=["01094"]),
    _c("sh011 Elbow Strike : TEMOIN, l'attaque d'un ALLIE (Hellcat) n'ouvre pas la Reponse : « your HERO »",
       "Hellcat attaque Rhino (1 degat) : Elbow Strike reste en main, pas d'hebetude",
       [HEROS, "Puzzle.PutIntoPlay('01020', under_control=True)"], ["Puzzle.Attack('01020')"],
       {"degats": [["01094", 1]], "statuts_absents": [["01094", "Dazed"]], "en_main": ["sh011"]},
       main_exclusive=["sh011"], cibles=["01094"]),
    _c("sh011 Elbow Strike : TEMOIN, une attaque qui ne blesse pas (Rhino TENACE : la carte Tough part) : pas de Reponse",
       "« and DAMAGES an enemy » : Tough absorbe l'attaque, aucun degat : la carte reste en main",
       [HEROS, "Puzzle.Tough('01094')"], ["Puzzle.Attack('01001a')"],
       {"degats": [["01094", 0]], "statuts_absents": [["01094", "Dazed"], ["01094", "Tough"]], "en_main": ["sh011"]},
       main_exclusive=["sh011"], cibles=["01094"]),
    _c("sh011 Elbow Strike : TEMOIN, une attaque qui n'est pas de BASE (evenement Haymaker) ne l'ouvre pas",
       "« a BASIC attack » : Haymaker (Hero Action) inflige 3 degats mais n'est pas l'attaque de base : Elbow Strike reste en main",
       [HEROS], [],
       {"degats": [["01094", 3]], "statuts_absents": [["01094", "Dazed"]], "en_main": ["sh011"], "defausse": ["01087"]},
       main_exclusive=["sh011", "01087", "01090"], payer_avec=["01090"], ne_pas_depenser=["sh011"], jouer=["01087"], cibles=["01094"]),
]

# ========================================================================= sh012 Mutant Fight Club
CLUB = ["Puzzle.PutIntoPlay('sh012', under_control=True)"]
CAS += [
    _c("sh012 Mutant Fight Club : Action d'alter-ego : s'incline, Peter prend 1 degat, Haymaker (ATTACK) de la defausse est attache FACE CACHEE",
       "« Exhaust this card and take 1 damage -> attach an ATTACK or DEFENSE event in your discard pile to this card facedown »",
       CLUB, DISC('01087') + ["Puzzle.Action('sh012', 'AlterEgoAction', 0)"],
       {"exhausted": ["sh012"], "degats_identite": 1, "pose_sous": [["sh012", "01087"]]},
       main_exclusive=[], cibles=["01087"]),
    _c("sh012 Mutant Fight Club : un evenement DEFENSE (Backflip) convient aussi",
       "« an ATTACK OR DEFENSE event »",
       CLUB, DISC('01003') + ["Puzzle.Action('sh012', 'AlterEgoAction', 0)"],
       {"exhausted": ["sh012"], "degats_identite": 1, "pose_sous": [["sh012", "01003"]]},
       main_exclusive=[], cibles=["01003"]),
    _c("sh012 Mutant Fight Club : un evenement THWART seul (Sideswipe) ne convient PAS : l'Action n'est pas offerte, aucun cout paye",
       "la defausse ne contient qu'un THWART : ni incline ni degat",
       CLUB, DISC('sh019'),
       {"pret": ["sh012"], "degats_identite": 0}, main_exclusive=[],
       declencher_tolerant=["Puzzle.Action('sh012', 'AlterEgoAction', 0)"]),
    _c("sh012 Mutant Fight Club : TEMOIN, forme HEROS : « Alter-Ego Action » n'est pas offerte",
       "en forme heros le soutien ne se remplit pas : ni incline ni degat",
       [HEROS] + CLUB, DISC('01087'),
       {"pret": ["sh012"], "degats_identite": 0}, main_exclusive=[],
       declencher_tolerant=["Puzzle.Action('sh012', 'AlterEgoAction', 0)"]),
    _c("sh012 Mutant Fight Club : AUCUN plafond imprime : deux evenements attaches en deux Actions",
       "contrairement a Santana Family (max 2) : Haymaker puis Backflip, apres redressement ; Peter prend 2 degats",
       CLUB,
       DISC('01087', '01003') + ["Puzzle.Action('sh012', 'AlterEgoAction', 0)", "Puzzle.Ready('sh012')",
                                 "Puzzle.Action('sh012', 'AlterEgoAction', 0)"],
       {"degats_identite": 2, "pose_sous": [["sh012", "01087"], ["sh012", "01003"]]},
       main_exclusive=[], cibles=["01087", "01003"]),
    _c("sh012 Mutant Fight Club : un evenement attache est JOUABLE comme en main (et pas celui de la defausse)",
       "« You may play events attached to this card as if they were in your hand » : `IsLikeInHand()` vrai pour la carte glissee",
       CLUB + ["Puzzle.PlaceUnder('01087', 'sh012')"], [],
       {"hote": "sh012", "carte": "01087", "comme_en_main": True}, verifier="sh_comme_en_main", main_exclusive=[]),
    _c("sh012 Mutant Fight Club : TEMOIN, la meme carte sous un AUTRE hote (l'identite) n'est pas jouable comme en main",
       "contre-bout : sans le Club, rien ne rend la carte glissee jouable",
       ["Puzzle.PlaceUnder('01087', '01001b')"], [],
       {"hote": "01001b", "carte": "01087", "comme_en_main": False}, verifier="sh_comme_en_main", main_exclusive=[]),
]

# ========================================================================= sh013 Roll With It
CAS += [
    _c("sh013 Roll With It : apres une defense du heros, le HEROS est REDRESSE (Reponse)",
       "« After your hero defends, ready your hero » : Fin Fang Foom (ATQ 4) attaque, Spider-Man defend (DEF 3) et s'incline ; "
       "la Reponse (cout 0) le redresse ; 1 degat subi",
       [HEROS, f"Puzzle.PutIntoPlay('{FFF}')"], [f"Puzzle.Attack('{FFF}', defender='01001a')"],
       {"pret": ["01001a"], "degats_identite": 1, "defausse": ["sh013"]}, main_exclusive=["sh013"]),
    _c("sh013 Roll With It : TEMOIN, le heros NE defend PAS (incline d'avance) : pas de Reponse, la carte reste en main",
       "« After your hero DEFENDS » : sans defense, rien",
       [HEROS, "Puzzle.Exhaust('01001a')", f"Puzzle.PutIntoPlay('{FFF}')"], [f"Puzzle.Attack('{FFF}')"],
       {"exhausted": ["01001a"], "degats_identite": 4, "en_main": ["sh013"]}, main_exclusive=["sh013"]),
    _c("sh013 Roll With It : depensee pour un evenement ATTACK (Haymaker), elle remet un evenement DEFENSE de la defausse SUR le deck",
       "« When you spend this card to pay for an ATTACK event, put a DEFENSE event from your discard pile on top of your deck » : "
       "Backflip passe de la defausse au DESSUS du deck (on le pioche ensuite)",
       [HEROS], DISC('01003'),
       {"en_main": ["01003"], "degats": [["01094", 3]], "defausse": ["01087", "sh013", "01090"]},
       main_exclusive=["01087", "sh013", "01090"], payer_avec=["sh013", "01090"], jouer=["01087"], cibles=["01094"],
       declencher_apres=["Puzzle.Draw(1)"]),
    _c("sh013 Roll With It : TEMOIN, depensee pour un evenement NON-ATTACK (Drop In sh008) : Backflip reste en defausse",
       "seul un evenement ATTACK declenche l'Interruption",
       [HEROS], DISC('01003'),
       {"defausse": ["01003", "sh013", "sh008"], "absent_main": ["01003"]},
       main_exclusive=["sh008", "sh013"], payer_avec=["sh013"], jouer=["sh008"]),
    _c("sh013 Roll With It : aucun evenement DEFENSE en defausse : l'Interruption ne fait rien et rien ne plante",
       "la defausse ne contient que Haymaker (ATTACK) : pas de cible, l'evenement ATTACK se joue normalement",
       [HEROS], [],
       {"degats": [["01094", 3]], "defausse": ["01087", "sh013", "01090"], "taille_main": 0},
       main_exclusive=["01087", "sh013", "01090"], payer_avec=["sh013", "01090"], jouer=["01087"], cibles=["01094"]),
]

# ========================================================================= sh014 Minarai
HC = "01020"  # Hellcat : allie 3 PV, ATQ 1*, CTR 2*, aucun texte d'entree en jeu
CAS += [
    _c("sh014 Minarai : « Attach to an ally you control » : joue sur Hellcat (cout 1, Strength), elle est ATTACHEE a l'allie",
       "le seul allie en jeu est la cible ; l'amelioration est rattachee (`accroche_a`)",
       [HEROS, f"Puzzle.PutIntoPlay('{HC}', under_control=True)"], [],
       {"accroche_a": [["sh014", HC]], "en_jeu": ["sh014"]},
       main_exclusive=["sh014", "01090"], payer_avec=["01090"], jouer=["sh014"], cibles=[HC]),
    _c("sh014 Minarai : l'allie attache subit des degats CONSECUTIFS apres avoir attaque : pioche 1 carte",
       "« After attached ally takes consequential damage, draw 1 card » : Hellcat (ATQ 1*) attaque Rhino, prend 1 degat consecutif ; "
       "main vide + 1 pioche",
       [HEROS, f"Puzzle.PutIntoPlay('{HC}', under_control=True)", "Puzzle.PutIntoPlay('sh014', under_control=True)",
        f"Puzzle.AttachReel('sh014', '{HC}')"], [f"Puzzle.Attack('{HC}')"],
       {"degats": [[HC, 1], ["01094", 1]], "taille_main": 1}, main_exclusive=[], cibles=["01094"]),
    _c("sh014 Minarai : TEMOIN, un AUTRE allie (Jessica Jones) qui subit des degats consecutifs ne declenche pas la Reponse",
       "« ATTACHED ally » : Minarai est sur Hellcat, c'est Jessica qui attaque ; pas de pioche",
       [HEROS, f"Puzzle.PutIntoPlay('{HC}', under_control=True)", "Puzzle.PutIntoPlay('01059', under_control=True)",
        "Puzzle.PutIntoPlay('sh014', under_control=True)", f"Puzzle.AttachReel('sh014', '{HC}')"], ["Puzzle.Attack('01059')"],
       {"degats": [["01059", 1]], "taille_main": 0}, main_exclusive=[], cibles=["01094"]),
    _c("sh014 Minarai : TEMOIN, Hellcat TENACE ne subit aucun degat consecutif (la carte Tough part) : pas de pioche",
       "« takes consequential damage » : seulement si les degats sont reellement subis",
       [HEROS, f"Puzzle.PutIntoPlay('{HC}', under_control=True)", f"Puzzle.Tough('{HC}')", "Puzzle.PutIntoPlay('sh014', under_control=True)",
        f"Puzzle.AttachReel('sh014', '{HC}')"], [f"Puzzle.Attack('{HC}')"],
       {"degats": [[HC, 0]], "taille_main": 0, "statuts_absents": [[HC, "Tough"]]}, main_exclusive=[], cibles=["01094"]),
    _c("sh014 Minarai : l'allie est VAINCU par ces degats consecutifs : l'amelioration part avec lui, aucune pioche",
       "Hellcat (3 PV, 2 degats deja) attaque, le degat consecutif la vainc",
       [HEROS, f"Puzzle.PutIntoPlay('{HC}', under_control=True)", f"Puzzle.Damage('{HC}', 2)", "Puzzle.PutIntoPlay('sh014', under_control=True)",
        f"Puzzle.AttachReel('sh014', '{HC}')"], [f"Puzzle.Attack('{HC}')"],
       {"hors_jeu": [HC, "sh014"], "taille_main": 0}, main_exclusive=[], cibles=["01094"]),
]

# ========================================================================= sh015 Keep the Momentum
CAS += [
    _c("sh015 Keep the Momentum : depensee pour un evenement TAIJUTSU (Stiff Jab) : un evenement Taijutsu de la defausse REVIENT en main",
       "« After you spend this card on an event, return 1 Taijutsu event from your discard pile to your hand » : Raising Block (Taijutsu) "
       "est dans la defausse ; Stiff Jab (cout 1) est payee par la ressource",
       [HEROS], DISC("sh001"),
       {"en_main": ["sh001"], "degats": [["01094", 2]], "defausse": ["sh003", "sh015"], "taille_main": 1},
       main_exclusive=["sh003", "sh015"], payer_avec=["sh015"], jouer=["sh003"], cibles=["01094"]),
    _c("sh015 Keep the Momentum : « on AN event » : depensee pour un evenement NON Taijutsu (Haymaker) elle declenche aussi",
       "Haymaker (cout 2) payee par la ressource + Strength ; Raising Block revient",
       [HEROS], DISC("sh001"),
       {"en_main": ["sh001"], "degats": [["01094", 3]], "defausse": ["01087", "sh015", "01090"], "taille_main": 1},
       main_exclusive=["01087", "sh015", "01090"], payer_avec=["sh015", "01090"], jouer=["01087"], cibles=["01094"]),
    _c("sh015 Keep the Momentum : TEMOIN, depensee pour un SOUTIEN (Aunt May) : pas un evenement, rien ne revient",
       "Aunt May (cout 1, Soutien) payee par la ressource : Raising Block reste en defausse",
       [HEROS], DISC("sh001"),
       {"absent_main": ["sh001"], "defausse": ["sh001", "sh015"], "en_jeu": ["01006"], "taille_main": 0},
       main_exclusive=["01006", "sh015"], payer_avec=["sh015"], jouer=["01006"]),
    _c("sh015 Keep the Momentum : TEMOIN, la defausse ne contient qu'un evenement NON Taijutsu (Haymaker) : rien ne revient",
       "« 1 TAIJUTSU event » : Haymaker (classe Basic) ne convient pas",
       [HEROS], DISC("01087"),
       {"absent_main": ["01087"], "defausse": ["01087", "sh003", "sh015"], "taille_main": 0},
       main_exclusive=["sh003", "sh015"], payer_avec=["sh015"], jouer=["sh003"], cibles=["01094"]),
    _c("sh015 Keep the Momentum : TEMOIN, une amelioration Taijutsu (Martial Skill) en defausse n'est pas un EVENEMENT : rien ne revient",
       "« Taijutsu EVENT » : le type compte",
       [HEROS], DISC("sh010"),
       {"absent_main": ["sh010"], "defausse": ["sh010", "sh003", "sh015"], "taille_main": 0},
       main_exclusive=["sh003", "sh015"], payer_avec=["sh015"], jouer=["sh003"], cibles=["01094"]),
    _c("sh015 Keep the Momentum : DEUX evenements Taijutsu en defausse : UN seul revient, au choix du joueur (Foot Sweep designe)",
       "« return 1 Taijutsu event » : un seul ; Raising Block reste en defausse",
       [HEROS], DISC("sh001", "sh002"),
       {"en_main": ["sh002"], "absent_main": ["sh001"], "defausse": ["sh001", "sh003", "sh015"], "taille_main": 1},
       main_exclusive=["sh003", "sh015"], payer_avec=["sh015"], jouer=["sh003"], cibles=["01094", "sh002"]),
    _c("sh015 Keep the Momentum : defausse VIDE de Taijutsu : rien ne revient et rien ne plante",
       "pas de candidat : la carte payee se joue normalement",
       [HEROS], DISC(),
       {"degats": [["01094", 2]], "defausse": ["sh003", "sh015"], "taille_main": 0},
       main_exclusive=["sh003", "sh015"], payer_avec=["sh015"], jouer=["sh003"], cibles=["01094"]),
]

# ========================================================================= sh016 Jo
JO = ["Puzzle.PutIntoPlay('sh016', under_control=True)", "Puzzle.Attach('sh016', '01001a')"]
CAS += [
    _c("sh016 Jo : entre en jeu avec 3 compteurs cudgel (Uses)",
       "« Uses (3 cudgel counters) » : natif (`desc.Uses = \"3,cudgel\"`, compteur ajoute a CardFace.COUNTER)",
       [HEROS] + JO, [], {"compteurs": [["sh016", "cudgel", 3]], "en_jeu": ["sh016"]}, main_exclusive=[]),
    _c("sh016 Jo : apres un evenement TAIJUTSU (Sideswipe) : +1 compteur cudgel (4 : AUCUN plafond)",
       "« After you play a Taijutsu event, place 1 cudgel counter here » : Uses ne fixe que le nombre d'entree",
       [HEROS] + JO, [f"Puzzle.SetThreat('{COMPLOT}', 3)"], {"compteurs": [["sh016", "cudgel", 4]], "defausse": ["sh019"]},
       main_exclusive=["sh019"], jouer=["sh019"], cibles=[COMPLOT]),
    _c("sh016 Jo : TEMOIN, un evenement NON Taijutsu (For Justice!, sans degats) ne pose aucun compteur",
       "« a TAIJUTSU event » : For Justice! (Justice) retire de la menace sans blesser : Jo reste a 3",
       [HEROS] + JO, [f"Puzzle.SetThreat('{COMPLOT}', 5)"], {"compteurs": [["sh016", "cudgel", 3]], "defausse": ["01060"]},
       main_exclusive=["01060", "01090"], payer_avec=["01090"], jouer=["01060"], cibles=[COMPLOT]),
    _c("sh016 Jo : TEMOIN, une carte Taijutsu qui n'est PAS un evenement (Mutant Fight Club, Soutien) ne pose aucun compteur",
       "« Taijutsu EVENT » : le type compte ; cout 1 paye par Strength",
       [HEROS] + JO, [], {"compteurs": [["sh016", "cudgel", 3]], "en_jeu": ["sh012"]},
       main_exclusive=["sh012", "01090"], payer_avec=["01090"], jouer=["sh012"]),
    _c("sh016 Jo : Hero Response apres l'attaque de base du heros : retire 2 compteurs, Rhino est HEBETE",
       "« After you damage an enemy, remove 2 cudgel counters from this card -> daze that enemy » : 3 -> 1 ; Spider-Man (ATQ 2) blesse Rhino",
       [HEROS] + JO, ["Puzzle.Attack('01001a')"],
       {"compteurs": [["sh016", "cudgel", 1]], "degats": [["01094", 2]], "statuts": [["01094", "Dazed"]]},
       main_exclusive=[], cibles=["01094"]),
    _c("sh016 Jo : TEMOIN, avec UN seul compteur le cout de 2 est impayable : pas de Reponse, pas d'hebetude",
       "1 compteur restant (3 - 2) : la Reponse n'est pas proposee",
       [HEROS] + JO + ["Puzzle.Counter('sh016', 'cudgel', -2)"], ["Puzzle.Attack('01001a')"],
       {"compteurs": [["sh016", "cudgel", 1]], "degats": [["01094", 2]], "statuts_absents": [["01094", "Dazed"]]},
       main_exclusive=[], cibles=["01094"]),
    _c("sh016 Jo : avec exactement 2 compteurs, le cout vide la carte (Uses) : elle part, Rhino est quand meme HEBETE",
       "le cout est paye avant l'effet : les 2 derniers compteurs retires, Jo defaussee, le sort se resout",
       [HEROS] + JO + ["Puzzle.Counter('sh016', 'cudgel', -1)"], ["Puzzle.Attack('01001a')"],
       {"hors_jeu": ["sh016"], "degats": [["01094", 2]], "statuts": [["01094", "Dazed"]]},
       main_exclusive=[], cibles=["01094"]),
    _c("sh016 Jo : lecture codee (Q-T4) : les degats d'un EVENEMENT que vous jouez (Haymaker) ouvrent aussi la Reponse",
       "« After YOU damage an enemy » : comme l'officielle 16032 / ua033 Pete, votre identite ET les cartes que vous jouez ; Haymaker : 3 degats",
       [HEROS] + JO, [], {"compteurs": [["sh016", "cudgel", 1]], "degats": [["01094", 3]], "statuts": [["01094", "Dazed"]]},
       main_exclusive=["01087", "01090"], payer_avec=["01090"], jouer=["01087"], cibles=["01094"]),
    _c("sh016 Jo : lecture codee (Q-T4) : un ALLIE (Hellcat) qui attaque n'ouvre PAS la Reponse",
       "« After YOU damage » : l'identite et ses cartes, pas les allies ; Jo reste a 3, Rhino sain",
       [HEROS, "Puzzle.PutIntoPlay('01020', under_control=True)"] + JO, ["Puzzle.Attack('01020')"],
       {"compteurs": [["sh016", "cudgel", 3]], "degats": [["01094", 1]], "statuts_absents": [["01094", "Dazed"]]},
       main_exclusive=[], cibles=["01094"]),
]

# ========================================================================= sh017 Odyn
ODYN = ["Puzzle.PutIntoPlay('sh017', under_control=True)"]
CAS += [
    _c("sh017 Odyn : attaque de base (ATQ 3**) : 3 degats a Rhino ; la Reponse (defausse Backflip, DEFENSE) donne Tough AVANT les 2 degats consecutifs, qui l'epuisent",
       "« After Odyn uses a basic power, discard a DEFENSE card from your hand -> give Odyn a tough status card » : le moteur resout la Reponse "
       "AVANT les degats consecutifs (journal : « gagne Tough » puis « Tough remplace les degats ») : Odyn n'a AUCUN degat et la carte Tough est "
       "consommee ; le temoin sans carte DEFENSE (cas suivant) subit les 2 degats",
       [HEROS] + ODYN, ["Puzzle.Attack('sh017')"],
       {"degats": [["01094", 3], ["sh017", 0]], "statuts_absents": [["sh017", "Tough"]], "defausse": ["01003"], "taille_main": 0},
       main_exclusive=["01003"], cibles=["01094"]),
    _c("sh017 Odyn : contre de base (CTR 1*) : 1 menace retiree, Reponse identique (Tough avant le degat consecutif, qui l'epuise)",
       "« a basic power » : l'attaque OU le contre ; menace 5 -> 4 ; Odyn n'a aucun degat (sans la Reponse : 1)",
       [HEROS] + ODYN, [f"Puzzle.SetThreat('{COMPLOT}', 5)", "Puzzle.Thwart('sh017')"],
       {"menace": [[COMPLOT, 4]], "degats": [["sh017", 0]], "statuts_absents": [["sh017", "Tough"]], "defausse": ["01003"]},
       main_exclusive=["01003"], cibles=[COMPLOT]),
    _c("sh017 Odyn : TEMOIN, sans carte DEFENSE en main (Haymaker seulement) le cout est impayable : pas de Tough",
       "« discard a DEFENSE card from your hand » est un COUT : la Reponse n'est pas proposee, Haymaker reste en main",
       [HEROS] + ODYN, ["Puzzle.Attack('sh017')"],
       {"degats": [["01094", 3], ["sh017", 2]], "statuts_absents": [["sh017", "Tough"]], "en_main": ["01087"]},
       main_exclusive=["01087"], cibles=["01094"]),
    _c("sh017 Odyn : TEMOIN, c'est le HEROS qui attaque (pas Odyn) : aucune Reponse, Backflip reste en main",
       "« After ODYN uses a basic power » : lui seul",
       [HEROS] + ODYN, ["Puzzle.Attack('01001a')"],
       {"degats": [["01094", 2], ["sh017", 0]], "statuts_absents": [["sh017", "Tough"]], "en_main": ["01003"]},
       main_exclusive=["01003"], cibles=["01094"]),
    _c("sh017 Odyn : TEMOIN, un AUTRE allie (Hellcat) qui attaque ne declenche pas Odyn",
       "idem avec un allie",
       [HEROS, "Puzzle.PutIntoPlay('01020', under_control=True)"] + ODYN, ["Puzzle.Attack('01020')"],
       {"degats": [["sh017", 0]], "statuts_absents": [["sh017", "Tough"]], "en_main": ["01003"]},
       main_exclusive=["01003"], cibles=["01094"]),
]

# ========================================================================= sh018 Countercross
CAS += [
    _c("sh018 Countercross : attaque de 4 : previent 1, inflige 1 a Rhino, retire 1 menace, pioche 1 (le heros prend 3)",
       "« prevent 1 of that damage. Deal 1 damage to an enemy. Remove 1 threat from a scheme. Draw 1 card » : Fin Fang Foom (ATQ 4) "
       "frappe le heros incline ; cout 1 paye par Strength ; menace 5 -> 4 ; main : 1 carte piochee",
       [HEROS, "Puzzle.Exhaust('01001a')", f"Puzzle.PutIntoPlay('{FFF}')"],
       [f"Puzzle.SetThreat('{COMPLOT}', 5)", f"Puzzle.Attack('{FFF}')"],
       {"degats_identite": 3, "degats": [["01094", 1]], "menace": [[COMPLOT, 4]], "taille_main": 1,
        "defausse": ["sh018", "01090"]},
       main_exclusive=["sh018", "01090"], payer_avec=["01090"], cibles=["01094", COMPLOT]),
    _c("sh018 Countercross : attaque de 1 (Hydra Mercenary) : la prevention de 1 vaut tout, les trois autres effets partent quand meme",
       "« prevent 1 OF THAT damage » : 1 - 1 = 0 degat ; riposte 1 (sur le sbire : Guard interdit de viser le vilain), menace -1, pioche 1",
       [HEROS, "Puzzle.Exhaust('01001a')", "Puzzle.PutIntoPlay('01101')"],
       [f"Puzzle.SetThreat('{COMPLOT}', 5)", "Puzzle.Attack('01101')"],
       {"degats_identite": 0, "degats": [["01101", 1], ["01094", 0]], "menace": [[COMPLOT, 4]], "taille_main": 1,
        "defausse": ["sh018", "01090"]},
       main_exclusive=["sh018", "01090"], payer_avec=["01090"], cibles=["01101", COMPLOT]),
    _c("sh018 Countercross : TEMOIN, des degats hors attaque ne sont pas prevenus (carte non offerte)",
       "« from an attack » : 3 degats directs, la carte reste en main",
       [HEROS], ["Puzzle.Damage('01001a', 3)"], {"degats_identite": 3, "en_main": ["sh018"]},
       main_exclusive=["sh018", "01090"]),
    _c("sh018 Countercross : TEMOIN, forme ALTER-EGO : Hero Interrupt non offerte",
       "Peter Parker prend les 4 degats",
       [f"Puzzle.PutIntoPlay('{FFF}')"], [f"Puzzle.Attack('{FFF}')"], {"degats_identite": 4, "en_main": ["sh018"]},
       main_exclusive=["sh018", "01090"]),
]

# ========================================================================= sh019 Sideswipe
CAS += [
    _c("sh019 Sideswipe : retire 1 menace et VIDE la manigance (1 -> 0) : un evenement ATTACK de la defausse revient",
       "« If this removes the last threat on that scheme, return an ATTACK card from your discard pile to your hand » : Haymaker revient",
       [HEROS], DISC("01087") + [f"Puzzle.SetThreat('{COMPLOT}', 1)"],
       {"menace": [[COMPLOT, 0]], "en_main": ["01087"], "defausse": ["sh019"], "taille_main": 1},
       main_exclusive=["sh019"], jouer=["sh019"], cibles=[COMPLOT]),
    _c("sh019 Sideswipe : la manigance garde de la menace (3 -> 2) : RIEN ne revient",
       "« the LAST threat » : pas le dernier",
       [HEROS], DISC("01087") + [f"Puzzle.SetThreat('{COMPLOT}', 3)"],
       {"menace": [[COMPLOT, 2]], "absent_main": ["01087"], "defausse": ["sh019", "01087"], "taille_main": 0},
       main_exclusive=["sh019"], jouer=["sh019"], cibles=[COMPLOT]),
    _c("sh019 Sideswipe : « THAT scheme » : la manigance annexe (Bomb Scare, 1 menace) est videe alors que la principale en garde : retour",
       "la derniere menace de LA manigance choisie, pas de la principale ; Bomb Scare 01109 mise a 1, videe elle quitte le jeu",
       [HEROS, "Puzzle.PutIntoPlay('01109')"], DISC("01087") + [f"Puzzle.SetThreat('{COMPLOT}', 4)", "Puzzle.SetThreat('01109', 1)"],
       {"hors_jeu": ["01109"], "menace": [[COMPLOT, 4]], "en_main": ["01087"], "defausse": ["sh019"], "taille_main": 1},
       main_exclusive=["sh019"], jouer=["sh019"], cibles=["01109"]),
    _c("sh019 Sideswipe : « an ATTACK CARD » : un seul candidat parmi DEUX cartes (Haymaker ATTACK, Wiggle Room DEFENSE) : l'ATTACK revient",
       "seule la carte au trait ATTACK convient ; le DEFENSE reste",
       [HEROS], DISC("05005", "01087") + [f"Puzzle.SetThreat('{COMPLOT}', 1)"],
       {"menace": [[COMPLOT, 0]], "en_main": ["01087"], "absent_main": ["05005"], "defausse": ["sh019", "05005"], "taille_main": 1},
       main_exclusive=["sh019"], jouer=["sh019"], cibles=[COMPLOT]),
    _c("sh019 Sideswipe : DEUX cartes ATTACK en defausse : UNE seule revient, au choix (Swinging Web Kick designe)",
       "« return AN ATTACK card » : une seule",
       [HEROS], DISC("01087", "01005") + [f"Puzzle.SetThreat('{COMPLOT}', 1)"],
       {"menace": [[COMPLOT, 0]], "en_main": ["01005"], "absent_main": ["01087"], "defausse": ["sh019", "01087"], "taille_main": 1},
       main_exclusive=["sh019"], jouer=["sh019"], cibles=[COMPLOT, "01005"]),
    _c("sh019 Sideswipe : manigance videe mais AUCUNE carte ATTACK en defausse : rien ne revient, rien ne plante",
       "defausse vide de traits ATTACK",
       [HEROS], DISC("05005") + [f"Puzzle.SetThreat('{COMPLOT}', 1)"],
       {"menace": [[COMPLOT, 0]], "absent_main": ["05005"], "defausse": ["sh019", "05005"], "taille_main": 0},
       main_exclusive=["sh019"], jouer=["sh019"], cibles=[COMPLOT]),
]

# ========================================================================= sh020 Tough Nut
CAS += [
    _c("sh020 Tough Nut : apres l'attaque de base du heros : carte Tough sur le HEROS, payee par Strength : PAS de soin",
       "« give it a tough status card. If you paid ... with a DEFENSE or THWART event, heal 2 » : Strength n'est pas un evenement ; "
       "Spider-Man (3 degats) reste a 3",
       [HEROS], ["Puzzle.Damage('01001a', 3)", "Puzzle.Attack('01001a')"],
       {"statuts": [["01001a", "Tough"]], "degats_identite": 3, "defausse": ["sh020", "01090"]},
       main_exclusive=["sh020", "01090"], payer_avec=["01090"], cibles=["01094"]),
    _c("sh020 Tough Nut : payee avec un evenement DEFENSE (Backflip) : carte Tough ET soin de 2 (3 -> 1)",
       "« DEFENSE or THWART » : Backflip (DEFENSE) paie le cout 1",
       [HEROS], ["Puzzle.Damage('01001a', 3)", "Puzzle.Attack('01001a')"],
       {"statuts": [["01001a", "Tough"]], "degats_identite": 1, "defausse": ["sh020", "01003"]},
       main_exclusive=["sh020", "01003"], payer_avec=["01003"], cibles=["01094"]),
    _c("sh020 Tough Nut : payee avec un evenement THWART (Sideswipe) : soin de 2",
       "l'autre moitie du « or »",
       [HEROS], ["Puzzle.Damage('01001a', 3)", "Puzzle.Attack('01001a')"],
       {"statuts": [["01001a", "Tough"]], "degats_identite": 1, "defausse": ["sh020", "sh019"]},
       main_exclusive=["sh020", "sh019"], payer_avec=["sh019"], cibles=["01094"]),
    _c("sh020 Tough Nut : payee avec un evenement ATTACK (Haymaker) : PAS de soin (seulement la carte Tough)",
       "ni DEFENSE ni THWART ; cout 1 : Haymaker (1 ressource) suffit",
       [HEROS], ["Puzzle.Damage('01001a', 3)", "Puzzle.Attack('01001a')"],
       {"statuts": [["01001a", "Tough"]], "degats_identite": 3, "defausse": ["sh020", "01087"]},
       main_exclusive=["sh020", "01087"], payer_avec=["01087"], cibles=["01094"]),
    _c("sh020 Tough Nut : le heros est DEJA tenace : pas de seconde carte, mais le soin a lieu (phrase separee)",
       "« give it a tough » ne peut rien donner ; « If you paid ... heal 2 » reste vrai (Backflip) : 3 -> 1",
       [HEROS], ["Puzzle.Damage('01001a', 3)", "Puzzle.Tough('01001a')", "Puzzle.Attack('01001a')"],
       {"statuts": [["01001a", "Tough"]], "degats_identite": 1, "defausse": ["sh020", "01003"]},
       main_exclusive=["sh020", "01003"], payer_avec=["01003"], cibles=["01094"]),
    _c("sh020 Tough Nut : apres un CONTRE de base du heros (THW) : la Reponse part aussi",
       "« uses a basic power » : ATQ, CTR ou DEF ; menace 3 -> 2",
       [HEROS], [f"Puzzle.SetThreat('{COMPLOT}', 3)", "Puzzle.Thwart('01001a')"],
       {"statuts": [["01001a", "Tough"]], "menace": [[COMPLOT, 2]], "defausse": ["sh020", "01090"]},
       main_exclusive=["sh020", "01090"], payer_avec=["01090"], cibles=[COMPLOT]),
    _c("sh020 Tough Nut : TEMOIN, un ALLIE (Hellcat) qui attaque n'ouvre pas la Reponse : « your HERO »",
       "Tough Nut reste en main, le heros n'est pas tenace",
       [HEROS, "Puzzle.PutIntoPlay('01020', under_control=True)"], ["Puzzle.Attack('01020')"],
       {"statuts_absents": [["01001a", "Tough"]], "en_main": ["sh020"]},
       main_exclusive=["sh020", "01090"], cibles=["01094"]),
]

# ========================================================================= sh004 Straight Cross
CAS += [
    _c("sh004 Straight Cross : 5 degats a Rhino, payee SANS evenement ATTACK (Strength RR + Energy YY) : pas d'etourdissement",
       "« Deal 5 damage to an enemy. If you paid with an ATTACK event, stun that enemy » : cout 3 paye par des RESSOURCES ordinaires",
       [HEROS], [], {"degats": [["01094", 5]], "statuts_absents": [["01094", "Stunned"]], "defausse": ["sh004"]},
       main_exclusive=["sh004", "01090", "01088"], payer_avec=["01090", "01088"], jouer=["sh004"], cibles=["01094"]),
    _c("sh004 Straight Cross : payee avec un evenement ATTACK (Haymaker 01087 + Strength) : Rhino est ETOURDI",
       "Haymaker (ATTACK) depense comme ressource : le bonus part ; 5 degats d'abord",
       [HEROS], [], {"degats": [["01094", 5]], "statuts": [["01094", "Stunned"]], "defausse": ["sh004", "01087"]},
       main_exclusive=["sh004", "01087", "01090"], payer_avec=["01087", "01090"], jouer=["sh004"], cibles=["01094"]),
]

# @@FIN-CAS@@


VERIFICATIONS = r'''
def sh_comme_en_main(monde, aides):
    """`attendu` : hote (en jeu), carte (rangee sous l'hote), comme_en_main (bool attendu de `IsLikeInHand()`).
    Contre-bout : une carte de la DEFAUSSE n'est jamais « comme en main » (sans lui la mesure ne discrimine rien)."""
    attendu = aides["cas"]["attendu"]
    hote = aides["par_id"](monde, attendu["hote"])
    if hote is None:
        return False, f"{attendu['hote']} n'est pas en jeu"
    rangees = [c for c in hote.GetPlacedCardArea().Get(True) if c is not None
               and getattr(c.paper, "card_id", None) == attendu["carte"]]
    if len(rangees) != 1:
        return False, f"{len(rangees)} exemplaire(s) de {attendu['carte']} sous {attendu['hote']} (attendu 1)"
    obtenu = bool(rangees[0].IsLikeInHand())
    if obtenu != attendu["comme_en_main"]:
        return False, f"{attendu['carte']} sous {attendu['hote']} : IsLikeInHand() = {obtenu} (attendu {attendu['comme_en_main']})"
    for f in monde.players[0].discard_pile.Get():
        if f is not None and f.IsLikeInHand():
            return False, f"{getattr(f.paper, 'card_id', '?')}, dans la DEFAUSSE, se dit aussi comme en main : la mesure ne discrimine rien"
    return True, f"{attendu['carte']} sous {attendu['hote']} : IsLikeInHand() = {obtenu}, la defausse non"
'''
