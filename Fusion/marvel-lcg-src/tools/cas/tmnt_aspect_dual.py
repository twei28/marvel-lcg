# Cas test_capacites du pack tmnt_aspect_dual (Inkwire, TMNT Aspects, « Dual-Aspect », prefixe ud),
# 16/10/2026. Filtre : `[ud]`. Gabarits : .planning/tmnt/aspects-dual-aspect-gabarits.md.
#
# Six ALLIES a double aspect (`desc.Class = "Aggression;Justice"` ...), tous a 1 degat consecutif
# sur THW et ATK, PV 2. Conventions :
#  - Spider-Man (01001) demarre en ALTER EGO ; HEROS le met en forme heros ;
#  - Rhino 01094 (vilain du scenario `rhino`, stade I en standard) est la cible des attaques ;
#  - 01101 Hydra Mercenary est le sbire ;
#  - jouer un allie a 4 : `main_exclusive` = l'allie + 01088 Energy (YY) + 01090 Strength (RR) ;
#  - « vaincu par degats consecutifs » : l'allie a deja 1 degat (PV 2), il attaque Rhino, le degat
#    consecutif le vainc ; le contre-cas le vainc par `Puzzle.Damage` (degats NON consecutifs).
#  - ⚠ `Puzzle.PutIntoPlay` declenche AUSSI les capacites d'entree en jeu (Cloaked de Rōnin et de
#    Stealth Fighter, Tough de Sōhei et Nightwatcher, compteurs amp, pioche de Doomsayer). Un Cloaked
#    reste absorbe 2 degats : `_en_jeu` retire cet etat (bascule de l'API) avant de poser des degats.
SC = "rhino"
HEROS = "Puzzle.ChangeForm('01001b')"
PAIE4 = ["01088", "01090"]

ETAT_D_ENTREE = {"ud001": "Puzzle.Cloak('ud001')", "ud004": "Puzzle.Cloak('ud004')",
                 "ud005": "Puzzle.Tough('ud005')", "ud006": "Puzzle.Tough('ud006')"}


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[ud] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": list(mise), "declencher": list(declencher),
           "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.update(cle)
    return cas


def _en_jeu(cid, degats=0, nu=True):
    """Pose l'allie sous controle, retire l'etat gagne a l'entree (nu=True), puis `degats` degats."""
    etapes = [f"Puzzle.PutIntoPlay('{cid}', under_control=True)"]
    if nu and cid in ETAT_D_ENTREE:
        etapes.append(ETAT_D_ENTREE[cid])
    if degats:
        etapes.append(f"Puzzle.Damage('{cid}', {degats})")
    return etapes


DEUX_SBIRES = ["Puzzle.PutIntoPlay('01101')", "Puzzle.PutIntoPlay(Puzzle.CreateCard('01101'))"]

CAS = [
    # ================================================================ moteur : double aspect
    _c("ud001 Rōnin (Aggression/Justice) : payee par The Power of Justice ET The Power of Aggression (2+2 = 4)",
       "« If used to pay for a JUSTICE card » et « ... an AGGRESSION card » : la carte double aspect est une carte de "
       "CHACUN des deux aspects (`IsClass`), chaque Power double : 4 ressources, Rōnin entre en jeu",
       [HEROS], [],
       {"en_jeu": ["ud001"]},
       main_exclusive=["ud001", "01062", "01055"], jouer=["ud001"], accepter_choix=True),
    _c("ud001 Rōnin : TEMOIN, The Power of LEADERSHIP ne double pas (2+1 = 3 < 4), Rōnin reste en main",
       "contre-cas : un troisieme aspect n'est pas un des siens ; sans lui le cas precedent prouverait seulement que "
       "toute Power double",
       [HEROS], [],
       {"en_main": ["ud001"], "hors_jeu": ["ud001"]},
       main_exclusive=["ud001", "01062", "01072"], jouer=["ud001"], accepter_choix=True),
    _c("ud003 Heavy Metal (Aggression/Protection) : The Power of Protection + The Power of Aggression = 4",
       "deuxieme paire d'aspects : la classe n'est pas lue sur son seul premier membre",
       [HEROS], [],
       {"en_jeu": ["ud003"]},
       main_exclusive=["ud003", "01079", "01055"], jouer=["ud003"], accepter_choix=True),

    # ================================================================ ud001 Rōnin
    _c("ud001 Rōnin : Response, apres son entree en jeu il est cloake (Cloaked)",
       "« After Rōnin enters play, cloak him » : la carte d'etat Cloaked est sur Rōnin, pas sur le heros",
       [HEROS], [],
       {"en_jeu": ["ud001"], "statuts": [["ud001", "Cloaked"]], "statuts_absents": [["01001a", "Cloaked"]]},
       main_exclusive=["ud001"] + PAIE4, jouer=["ud001"], accepter_choix=True),
    _c("ud001 Rōnin : Interrupt, vaincu par degat consecutif + depense d'une ressource [wild] -> pioche 3",
       "1 degat deja (PV 2), il attaque, le degat consecutif le vainc ; The Power of Aggression (wild) paie : main "
       "= 0 + 3",
       [HEROS, *_en_jeu("ud001", 1), "Puzzle.EmptyHand()", "Puzzle.CreateHandCards('01055')"],
       ["Puzzle.Attack('ud001')"],
       {"hors_jeu": ["ud001"], "taille_main": 3, "defausse": ["01055"]},
       cibles=["01094"], accepter_choix=True),
    _c("ud001 Rōnin : Interrupt, TEMOIN sans ressource WILD (seulement Strength RR) : rien n'est pioche",
       "« spend a [wild] resource » : une ressource physique ne paie pas (`HasColor('G')` sans conversion)",
       [HEROS, *_en_jeu("ud001", 1), "Puzzle.EmptyHand()", "Puzzle.CreateHandCards('01090')"],
       ["Puzzle.Attack('ud001')"],
       {"hors_jeu": ["ud001"], "taille_main": 1, "en_main": ["01090"]},
       cibles=["01094"], accepter_choix=True),
    _c("ud001 Rōnin : Interrupt, TEMOIN vaincu par des degats NON consecutifs : rien n'est pioche",
       "« defeated by CONSEQUENTIAL damage » : 2 degats d'une autre source ne declenchent pas l'Interruption",
       [HEROS, *_en_jeu("ud001"), "Puzzle.EmptyHand()", "Puzzle.CreateHandCards('01055')"],
       ["Puzzle.Damage('ud001', 2)"],
       {"hors_jeu": ["ud001"], "taille_main": 1, "en_main": ["01055"]},
       accepter_choix=True),

    # ================================================================ ud002 Doomsayer
    _c("ud002 Doomsayer : Response, entree en jeu au stade I de Rhino -> pioche 1",
       "« draw X cards, where X is equal to the villain's stage number » : stade 1 -> 1 carte (main vide apres "
       "paiement, donc main = 1)",
       [HEROS], [],
       {"en_jeu": ["ud002"], "taille_main": 1},
       main_exclusive=["ud002"] + PAIE4, jouer=["ud002"], accepter_choix=True),
    _c("ud002 Doomsayer : Response, au stade II -> pioche 2",
       "le chiffre suit le stade (Puzzle.AdvanceVillain : Rhino I -> II). Le plafond « maximum of 3 » n'est pas "
       "mordable ici : aucun vilain du harnais n'a de stade 4",
       [HEROS, "Puzzle.AdvanceVillain()"], [],
       {"en_jeu": ["ud002"], "taille_main": 2},
       main_exclusive=["ud002"] + PAIE4, jouer=["ud002"], accepter_choix=True),
    _c("ud002 Doomsayer : Interrupt, vaincu par degat consecutif avec 2 sbires engages -> pioche 2",
       "« draw 1 card for each minion engaged with you » : deux Hydra Mercenary engages, main videe apres la pose "
       "(la Reponse d'entree a pioche 1) -> 2",
       [HEROS, *_en_jeu("ud002", 1), *DEUX_SBIRES, "Puzzle.EmptyHand()"],
       ["Puzzle.Attack('ud002')"],
       {"hors_jeu": ["ud002"], "taille_main": 2},
       cibles=["01094"], accepter_choix=True),
    _c("ud002 Doomsayer : Interrupt, TEMOIN aucun sbire engage -> 0 carte",
       "le chiffre vient bien des sbires : sans eux, rien",
       [HEROS, *_en_jeu("ud002", 1), "Puzzle.EmptyHand()"],
       ["Puzzle.Attack('ud002')"],
       {"hors_jeu": ["ud002"], "taille_main": 0},
       cibles=["01094"], accepter_choix=True),
    _c("ud002 Doomsayer : Interrupt, TEMOIN vaincu par degats NON consecutifs (2 sbires) -> 0 carte",
       "« defeated by CONSEQUENTIAL damage »",
       [HEROS, *_en_jeu("ud002"), *DEUX_SBIRES, "Puzzle.EmptyHand()"],
       ["Puzzle.Damage('ud002', 2)"],
       {"hors_jeu": ["ud002"], "taille_main": 0},
       accepter_choix=True),

    # ================================================================ ud003 Heavy Metal
    _c("ud003 Heavy Metal : entre en jeu avec 2 compteurs amp",
       "« Heavy Metal enters play with 2 amp counters on her »",
       [HEROS], [],
       {"en_jeu": ["ud003"], "compteurs": [["ud003", "amp", 2]]},
       main_exclusive=["ud003"] + PAIE4, jouer=["ud003"], accepter_choix=True),
    _c("ud003 Heavy Metal : Response (lecture provisoire Q-UD2), degat consecutif -> 1 amp retire, un etat sur Rhino",
       "elle attaque Rhino (1 degat consecutif, PV 2 : elle survit) ; « remove 1 amp counter from her -> place a "
       "status card on a character » : amp 2 -> 1, Rhino porte une carte d'etat (la premiere proposee : Stunned)",
       [HEROS, *_en_jeu("ud003")],
       ["Puzzle.Attack('ud003')"],
       {"compteurs": [["ud003", "amp", 1]], "statuts": [["01094", "Stunned"]], "degats": [["ud003", 1]]},
       cibles=["01094", "01094"], accepter_choix=True),
    _c("ud003 Heavy Metal : Response, TEMOIN sans compteur amp : la Reponse n'est pas payable, Rhino sans etat",
       "le retrait du compteur est un COUT : a 0, rien n'est pose",
       [HEROS, *_en_jeu("ud003"), "Puzzle.Counter('ud003', 'amp', -2)"],
       ["Puzzle.Attack('ud003')"],
       {"compteurs": [["ud003", "amp", 0]], "statuts_absents": [["01094", "Stunned"], ["01094", "Confused"]],
        "degats": [["ud003", 1]]},
       cibles=["01094", "01094"], accepter_choix=True),
    _c("ud003 Heavy Metal : Response, TEMOIN Tenace : le degat consecutif est empeche, pas de Reponse (amp 2)",
       "« takes consequential damage » = degats REELLEMENT subis (note de 19012 Martyr)",
       [HEROS, *_en_jeu("ud003"), "Puzzle.Tough('ud003')"],
       ["Puzzle.Attack('ud003')"],
       {"compteurs": [["ud003", "amp", 2]], "statuts_absents": [["01094", "Stunned"]], "degats": [["ud003", 0]]},
       cibles=["01094", "01094"], accepter_choix=True),

    # ================================================================ ud004 Stealth Fighter
    _c("ud004 Stealth Fighter : Response, apres son entree en jeu il est cloake",
       "« After Stealth Fighter enters play ..., cloak him »",
       [HEROS], [],
       {"en_jeu": ["ud004"], "statuts": [["ud004", "Cloaked"]]},
       main_exclusive=["ud004"] + PAIE4, jouer=["ud004"], accepter_choix=True),
    _c("ud004 Stealth Fighter : Response, apres un degat consecutif subi (il survit) il est cloake",
       "« ... or takes consequential damage, cloak him » : Cloaked d'entree retire, il contre, subit 1 degat "
       "consecutif et porte de nouveau Cloaked",
       [HEROS, *_en_jeu("ud004"), "Puzzle.SetThreat('01097b', 5)"],
       ["Puzzle.Thwart('ud004')"],
       {"statuts": [["ud004", "Cloaked"]], "degats": [["ud004", 1]]},
       cibles=["01097b"], accepter_choix=True),
    _c("ud004 Stealth Fighter : Interrupt (lecture provisoire Q-UD3), vaincu par degat consecutif -> un ami cloake",
       "« cloak a friendly character » : le seul autre ami est Spider-Man, qui porte Cloaked",
       [HEROS, *_en_jeu("ud004", 1)],
       ["Puzzle.Attack('ud004')"],
       {"hors_jeu": ["ud004"], "statuts": [["01001a", "Cloaked"]]},
       cibles=["01094"], accepter_choix=True),
    _c("ud004 Stealth Fighter : Interrupt, TEMOIN vaincu par degats NON consecutifs -> personne n'est cloake",
       "« defeated by CONSEQUENTIAL damage »",
       [HEROS, *_en_jeu("ud004")],
       ["Puzzle.Damage('ud004', 2)"],
       {"hors_jeu": ["ud004"], "statuts_absents": [["01001a", "Cloaked"]]},
       accepter_choix=True),

    # ================================================================ ud005 Sōhei
    _c("ud005 Sōhei : Toughness, il entre en jeu avec une carte Tough",
       "mot-cle lu dans `desc.Toughness` (aucun code)",
       [HEROS], [],
       {"en_jeu": ["ud005"], "statuts": [["ud005", "Tough"]]},
       main_exclusive=["ud005"] + PAIE4, jouer=["ud005"], accepter_choix=True),
    _c("ud005 Sōhei : Interrupt, vaincu par degat consecutif -> le heros gagne +2 taille de main",
       "Tough retiree, 1 degat deja : l'attaque le vainc ; « your hero gets +2 hand size until the end of the "
       "round » : taille de main imprimee + 2",
       [HEROS, *_en_jeu("ud005", 1)],
       ["Puzzle.Attack('ud005')"],
       {"hors_jeu": ["ud005"], "attributs": {"hand_size": 2}},
       cibles=["01094"], accepter_choix=True),
    _c("ud005 Sōhei : Interrupt, TEMOIN vaincu par degats NON consecutifs -> taille de main inchangee",
       "« defeated by CONSEQUENTIAL damage »",
       [HEROS, *_en_jeu("ud005")],
       ["Puzzle.Damage('ud005', 2)"],
       {"hors_jeu": ["ud005"], "attributs": {"hand_size": 0}},
       accepter_choix=True),
    _c("ud005 Sōhei : Interrupt, le bonus vaut jusqu'a la fin du ROUND (encore la apres la fin de la phase joueur)",
       "« until the end of the round » et non « of the phase » : apres Puzzle.EndPlayerPhase, +2 toujours la",
       [HEROS, *_en_jeu("ud005", 1)],
       ["Puzzle.Attack('ud005')", "Puzzle.EndPlayerPhase()"],
       {"hors_jeu": ["ud005"], "attributs": {"hand_size": 2}},
       cibles=["01094"], accepter_choix=True),
    _c("ud005 Sōhei : Interrupt (lecture provisoire Q-UD4), joueur en ALTER EGO : pas de bonus",
       "« YOUR HERO » : l'identite est en forme alter ego au moment ou Sōhei tombe -> rien (lecture recommandee)",
       [*_en_jeu("ud005", 1)],
       ["Puzzle.Attack('ud005')"],
       {"hors_jeu": ["ud005"], "attributs": {"hand_size": 0}},
       cibles=["01094"], accepter_choix=True),

    # ================================================================ ud006 Nightwatcher
    _c("ud006 Nightwatcher : Toughness, elle entre en jeu avec une carte Tough",
       "mot-cle lu dans `desc.Toughness`",
       [HEROS], [],
       {"en_jeu": ["ud006"], "statuts": [["ud006", "Tough"]]},
       main_exclusive=["ud006"] + PAIE4, jouer=["ud006"], accepter_choix=True),
    _c("ud006 Nightwatcher : Response, degat consecutif subi -> elle recoit une carte Tough",
       "Tough d'entree retiree : elle attaque, subit 1 degat consecutif, puis « give her a tough status card »",
       [HEROS, *_en_jeu("ud006")],
       ["Puzzle.Attack('ud006')"],
       {"statuts": [["ud006", "Tough"]], "degats": [["ud006", 1]]},
       cibles=["01094"], accepter_choix=True),
    _c("ud006 Nightwatcher : Response, TEMOIN avec Tough : le degat est empeche (Tough consommee), pas de nouvelle Tough",
       "« takes » : une Tough qui empeche le degat ne donne pas de Reponse (19012) ; elle finit sans Tough, 0 degat",
       [HEROS, *_en_jeu("ud006", nu=False)],
       ["Puzzle.Attack('ud006')"],
       {"statuts_absents": [["ud006", "Tough"]], "degats": [["ud006", 0]]},
       cibles=["01094"], accepter_choix=True),
]
