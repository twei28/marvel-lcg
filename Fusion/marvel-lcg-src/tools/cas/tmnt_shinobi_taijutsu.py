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
    if not cle.pop("avec_boost", False):
        mise = SANS_BOOST + list(mise)
    cas = {"nom": "[sh] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": list(mise), "declencher": list(declencher),
           "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = []

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
       ["Puzzle.Exhaust('01001b')", "Puzzle.CreatePlayerDiscardPile('01087')"], [],
       {"pret": ["01001b"], "en_main": ["01087"], "defausse": ["sh008", "01003"]},
       main_exclusive=["sh008", "01003"], payer_avec=["01003"], jouer=["sh008"]),
    _c("sh008 Drop In : meme chose avec un evenement THWART de la defausse (Sideswipe)",
       "« ATTACK OR THWART » : le trait THWART convient aussi",
       ["Puzzle.CreatePlayerDiscardPile('sh019')"], [],
       {"en_main": ["sh019"], "defausse": ["sh008", "01003"]},
       main_exclusive=["sh008", "01003"], payer_avec=["01003"], jouer=["sh008"]),
    _c("sh008 Drop In : « you MAY » : le retour se refuse (Cancel), Haymaker reste en defausse",
       "la carte est offerte mais refusable (`MayChooseFace`)",
       ["Puzzle.CreatePlayerDiscardPile('01087')"], [],
       {"absent_main": ["01087"], "defausse": ["sh008", "01003", "01087"]},
       main_exclusive=["sh008", "01003"], payer_avec=["01003"], jouer=["sh008"], preferer_option="Cancel"),
    _c("sh008 Drop In : un evenement DEFENSE de la defausse n'est PAS rendu (ni ATTACK ni THWART)",
       "seuls les evenements ATTACK ou THWART conviennent : la defausse ne contient qu'un DEFENSE (Wiggle Room)",
       ["Puzzle.CreatePlayerDiscardPile('05005')"], [],
       {"absent_main": ["05005"], "defausse": ["sh008", "01003", "05005"]},
       main_exclusive=["sh008", "01003"], payer_avec=["01003"], jouer=["sh008"]),
    _c("sh008 Drop In : payee SANS evenement DEFENSE (Strength) : Haymaker reste en defausse",
       "le retour est conditionne au paiement par un evenement DEFENSE",
       ["Puzzle.CreatePlayerDiscardPile('01087')"], [],
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
