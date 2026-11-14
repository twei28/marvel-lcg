# Cas test_capacites du heros custom PREDATOR (RyCoRan, prefixe `pd`) : noms prefixes « [pd] » puis le card_id
# (substituer_pack.py filtre dessus). Suite : predator_b.py (cartes signature), predator_c.py (nemesis, Team-Up).
#
# Rappels de montage :
#  - Predator demarre en ALTER EGO (pd001b) ; `Puzzle.ChangeToFace('pd001b', 'pd001a')` la passe en forme HEROS ;
#  - Infralocked (pd002, Permanent) est mis de cote et entre en jeu au Setup (pd001b) : elle est donc DEJA sur l'identite au
#    debut de chaque cas. `accroche_a` mesure sur quel hote elle est ;
#  - `player_deck` est complete par le harnais (ressources inertes), `main_exclusive` fixe la main ;
#  - Rhino 01094 est le vilain, 01097b son complot principal, 01103 Shocker (3 PV) et 01121 Weapons Runner (2 PV) des
#    sbires sans Guard, 01101 Hydra Mercenary a GUARD ;
#  - ressources : 01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR ;
#  - icones imprimees (verifiees contre les 3 ressources du MEME pack) : pd003 G, pd004 Y, pd005 R, pd006 B, pd007 R,
#    pd008 B, pd009 G, pd010 B, pd011 YY, pd012 R, pd013 Y, pd014 B.
SC = "rhino"
HEROS = "Puzzle.ChangeToFace('pd001b', 'pd001a')"
CIVIL = "Puzzle.ChangeToFace('pd001a', 'pd001b')"
SANS_DECK = "Puzzle.EmptyPlayerDeck()"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105', '01105', '01105')"]
COMPLOT = "01097b"
VILAIN = "01094"
INFRA = "pd002"
SHOCKER = "01103"
RUNNER = "01121"
GUARD = "01101"


def en_jeu(*ids):
    return [f"Puzzle.PutIntoPlay('{i}', under_control=True)" for i in ids]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    if not cle.pop("avec_boost", False):
        mise = SANS_BOOST + list(mise)
    cas = {"nom": "[pd] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "predator"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    # ============================================================ pd001b Yd'Nar : Setup
    _c("pd001b Setup : Infralocked entre en jeu AU SETUP sur l'identite",
       "« Setup: Put Infralocked into play »",
       [], [], {"accroche_a": [[INFRA, "pd001b"]]}, main_exclusive=["01090"]),
    # ============================================================ pd001a Predator : Response
    _c("pd001a Response : apres l'entree d'un sbire, Infralocked s'attache a lui",
       "« Response: After a minion enters play, attach Infralocked to it »",
       [HEROS], [f"Puzzle.PutIntoPlay('{SHOCKER}')"], {"accroche_a": [[INFRA, SHOCKER]]},
       main_exclusive=["01090"]),
    _c("pd001a Response : un SECOND sbire reprend Infralocked (une seule carte, elle change d'hote)",
       "Infralocked n'a qu'un exemplaire : « attach Infralocked to it » la deplace",
       [HEROS], [f"Puzzle.PutIntoPlay('{SHOCKER}')", f"Puzzle.PutIntoPlay('{RUNNER}')"],
       {"accroche_a": [[INFRA, RUNNER]]}, main_exclusive=["01090"]),
    _c("pd001a Camouflaged Hunter : apres avoir vaincu un sbire, Predator recoit une carte Cloaked",
       "« Response: After you defeat a minion, give Predator a cloaked status card »",
       [HEROS, f"Puzzle.PutIntoPlay('{RUNNER}')"], ["Puzzle.Attack('pd001a')"],
       {"statuts": [["pd001a", "Cloaked"]], "hors_jeu": [RUNNER]}, main_exclusive=["01090"], cibles=[RUNNER]),
    _c("pd001a Camouflaged Hunter : le sbire SURVIT (3 PV, ATK 3 = mort) -> choisir un sbire a 4 PV : pas de Cloaked",
       "contre-cas : « after you DEFEAT » exige la defaite",
       [HEROS, "Puzzle.PutIntoPlay('01182')"], ["Puzzle.Attack('pd001a')"],
       {"statuts_absents": [["pd001a", "Cloaked"]], "degats": [["01182", 3]]}, main_exclusive=["01090"], cibles=["01182"]),
    _c("pd001a Predator : valeurs imprimees PV 13, THW 0, ATK 3, DEF 2, SOLDIER YAUTJA",
       "nombres texte <-> code (scan HERO) : HAND SIZE 5 / HIT POINTS 13",
       [HEROS], [], {"pv_max": [["pd001a", 13]], "traits": ["SOLDIER", "YAUTJA"]}, main_exclusive=["01090"]),
    _c("pd001b Yd'Nar : valeurs imprimees PV 13, REC 4, SOLDIER YAUTJA",
       "nombres texte <-> code (scan ALTER-EGO) : HAND SIZE 6 / HIT POINTS 13 / REC 4",
       [], [], {"pv_max": [["pd001b", 13]], "traits": ["SOLDIER", "YAUTJA"]}, main_exclusive=["01090"]),
    # ============================================================ pd002 Infralocked : Hero Interrupt
    _c("pd002 Infralocked : Predator vainc le sbire porteur -> 2 menaces retirees du complot principal, retour sur l'identite",
       "« Hero Interrupt: When Predator defeats attached minion, remove 2 threat from a scheme. Then, return this card to your play area »",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)", f"Puzzle.PutIntoPlay('{RUNNER}')"], ["Puzzle.Attack('pd001a')"],
       {"menace": [[COMPLOT, 3]], "accroche_a": [[INFRA, "pd001a"]], "hors_jeu": [RUNNER]},
       main_exclusive=["01090"], cibles=[RUNNER, COMPLOT]),
    _c("pd002 Infralocked : sur une manigance ANNEXE, 3 menaces et non 2 (« 3 threat instead from a side scheme »)",
       "« remove 2 threat from a scheme (3 threat instead from a side scheme) »",
       [HEROS, "Puzzle.PutIntoPlay('01109')", "Puzzle.SetThreat('01109', 5)", f"Puzzle.PutIntoPlay('{RUNNER}')"],
       ["Puzzle.Attack('pd001a')"],
       {"menace": [["01109", 2]], "accroche_a": [[INFRA, "pd001a"]]},
       main_exclusive=["01090"], cibles=[RUNNER, "01109"]),
    _c("pd002 Infralocked : le sbire porteur tombe par une AUTRE cause que Predator -> Infralocked ne disparait pas",
       "Permanent : la carte ne quitte jamais le jeu ; elle ne doit pas rester accrochee a un sbire disparu",
       [HEROS, f"Puzzle.PutIntoPlay('{RUNNER}')"], [f"Puzzle.Damage('{RUNNER}', 9)"],
       {"accroche_a": [[INFRA, "pd001a"]], "hors_jeu": [RUNNER]}, main_exclusive=["01090"]),
    _c("pd001a Response : le joueur REFUSE (« Response » est optionnelle) -> Infralocked reste sur l'identite, pas sur le sbire",
       "DECISION UTILISATEUR (25/10, question 5/6) : « on peut choisir de la mettre sur le sbire ou pas, ce n'est pas automatique »",
       [HEROS], [f"Puzzle.PutIntoPlay('{SHOCKER}')"], {"accroche_a": [[INFRA, "pd001a"]]},
       main_exclusive=["01090"], passer_sur_option="Response"),
    _c("pd002 Infralocked : le joueur REFUSE l'Interruption (« Hero Interrupt » optionnelle) -> aucune menace retiree, la carte revient quand meme sur l'identite",
       "contre-cas : l'Interruption est facultative ; le sbire porteur disparait, Permanent ramene la carte",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)", f"Puzzle.PutIntoPlay('{RUNNER}')"], ["Puzzle.Attack('pd001a')"],
       {"menace": [[COMPLOT, 5]], "accroche_a": [[INFRA, "pd001a"]], "hors_jeu": [RUNNER]},
       main_exclusive=["01090"], cibles=[RUNNER, COMPLOT], passer_sur_option="Hero_Interrupt"),
]
