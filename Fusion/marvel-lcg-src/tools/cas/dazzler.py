# Cas test_capacites du pack custom DAZZLER (Lord Havok, set « Dazzler », dz001a-dz038) : verification
# carte par carte des cartes hors irefrixs (backlog 12, `.planning/todos/2026-10-06-verification-cartes-hors-irefrixs.md`),
# reprise le 20/10/2026 a la carte dz004. Noms prefixes « [dazzler] dzNNN » : `substituer_pack.py` filtre sur
# « <card_id> » suivi d'une espace, un nom de cas ne cite donc JAMAIS un autre card_id suivi d'une espace.
# Gabarits PROCESSUS-CARTE : `.planning/todos/2026-10-20-backlog-12-gabarits-processus-carte.md`.
#
# Rappels de montage :
#  - Dazzler demarre en ALTER EGO (dz001b Alison Blaire) ; `Puzzle.ChangeForm('dz001b')` la passe en HEROINE.
#    Le Setup d'Alison Blaire pose Live Concert (dz017a) en jeu.
#  - Une CHANSON jouee (evenement SONG) est rangee par la Reponse de Live Concert dans la Setlist (zone posee
#    sous dz017a) : elle ne va PAS en defausse tant que la Setlist a de la place.
#  - Un « Showtime! » ne part que par Rehearsal (Hero Action de dz001a) ou par le retournement de Live Concert.
#    Pour l'isoler de la Hero Action de la meme carte, la chanson est posee DIRECTEMENT dans la Setlist :
#    `Puzzle.PlaceUnder('<chanson>', 'dz017a', face_up=True)` (argument ajoute le 20/10/2026), puis
#    `Puzzle.Action('dz001a', 'HeroAction')`.
#  - `main_exclusive` dit avec QUOI on paie (01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR) et
#    DEFAUSSE la main de depart APRES `mise_en_place` : menace et defausse construites vont dans `declencher`.
#  - Rhino 01094 est le vilain, 01097b son complot principal, 01101 Hydra Mercenary le sbire (Guard),
#    01103 Shocker un sbire sans Guard. Complots annexes neutres : 01109 Bomb Scare (2), 01126 Illegal Arms
#    Factory (3).
SC = "rhino"
HEROINE = "Puzzle.ChangeForm('dz001b')"
COMPLOT = "01097b"
SANS_DECK = "Puzzle.EmptyPlayerDeck()"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105', '01105', '01105')"]
REPETER = "Puzzle.Action('dz001a', 'HeroAction')"
FIN_DE_PHASE = "Puzzle.EndPlayerPhase()"
VIDER_DEFAUSSE = "Puzzle.EmptyPlayerDiscardPile()"


def dans_setlist(*ids):
    return [f"Puzzle.PlaceUnder('{i}', 'dz017a', face_up=True)" for i in ids]


def en_jeu(*ids):
    return [f"Puzzle.PutIntoPlay('{i}', under_control=True)" for i in ids]


def menace(scheme, n):
    return f"Puzzle.SetThreat('{scheme}', {n})"


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    if not cle.pop("avec_boost", False):
        mise = SANS_BOOST + list(mise)
    cas = {"nom": "[dazzler] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "dazzler"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.update(cle)
    return cas


VERIFICATIONS = r'''
CLES_DAZZLER = {'mains', 'setlist', 'compteurs_setlist', 'deck_joueur_taille', 'jouable', 'face_cachee_sous',
                'compteurs_defausse'}


def dz_etat(monde, aides):
    """etat_attendu + cles propres au pack dazzler :
    - mains : [[rang du joueur, taille]] (taille de la main de CHAQUE joueur, « each player ») ;
    - setlist : liste EXACTE des card_id dans la Setlist (zone posee sous Live Concert, l'une ou l'autre face) ;
    - compteurs_setlist : [[card_id, compteur, n]] sur une carte de la Setlist (hors jeu, donc invisible a `compteurs`) ;
    - deck_joueur_taille : [[rang du joueur, taille]] ;
    - jouable : [[card_id, bool]], la carte EN MAIN du joueur 0 est-elle jouable (`CanPlayBy`) ?"""
    cas = aides["cas"]
    attendu = dict(cas.get("attendu") or {})
    propres = {k: attendu.pop(k) for k in list(attendu) if k in CLES_DAZZLER}
    soucis = []
    for cid, compteur, n in propres.get("compteurs_defausse") or []:
        pile = [f for f in monde.const_players[0].discard_pile.Get() if getattr(f.paper, "card_id", None) == cid]
        if not pile:
            soucis.append(f"{cid} absente de la defausse (compteurs_defausse)")
            continue
        vu = pile[0].CastTo(aides["CanPlaceCounter"]).GetCounters(compteur)
        if vu != n:
            soucis.append(f"{cid} en defausse porte {vu} compteur(s) {compteur} (attendu {n})")
    for hote_id, cid, cachee in propres.get("face_cachee_sous") or []:
        hote = aides["par_id"](monde, hote_id)
        zone = hote.GetPlacedCardArea() if hote is not None else None
        trouves = [f for f in (zone.Get(True) if zone is not None else [])
                   if getattr(f.paper, "card_id", None) == cid]
        if not trouves:
            soucis.append(f"{cid} absente de la zone posee sous {hote_id}")
        elif (not trouves[0].card.state.is_face_up) != cachee:
            soucis.append(f"{cid} sous {hote_id} : face cachee = {not trouves[0].card.state.is_face_up} "
                          f"(attendu {cachee})")
    for cid, voulu in propres.get("jouable") or []:
        j = monde.const_players[0]
        main = [f for f in j.hand_cards.GetAll() if getattr(f.paper, "card_id", None) == cid]
        if not main:
            soucis.append(f"{cid} absente de la main")
            continue
        vu = bool(main[0].CanPlayBy(j))
        if vu != voulu:
            soucis.append(f"{cid} jouable={vu} (attendu {voulu})")
    for rang, taille in propres.get("mains") or []:
        j = monde.const_players[rang]
        vu = len(list(j.hand_cards.GetAll()))
        if vu != taille:
            soucis.append(f"main du joueur {rang} = {vu} (attendu {taille})")
    for rang, taille in propres.get("deck_joueur_taille") or []:
        j = monde.const_players[rang]
        vu = len(list(j.player_deck.Get(True)))
        if vu != taille:
            soucis.append(f"deck du joueur {rang} = {vu} (attendu {taille})")
    concert = None
    for objet in monde.object_manager.card_dict.values():
        f = objet.face
        if f is not None and f.IsInPlay() and getattr(f.paper, "card_id", None) in ("dz017a", "dz017b"):
            concert = f
    zone = concert.GetPlacedCardArea() if concert is not None else None
    dans = list(zone.Get(True)) if zone is not None else []
    ids = [getattr(f.paper, "card_id", "?") for f in dans]
    if "setlist" in propres and sorted(ids) != sorted(propres["setlist"]):
        soucis.append(f"setlist = {ids} (attendu {propres['setlist']})")
    for cid, compteur, n in propres.get("compteurs_setlist") or []:
        trouves = [f for f in dans if getattr(f.paper, "card_id", None) == cid]
        if not trouves:
            soucis.append(f"{cid} absente de la setlist ({ids})")
            continue
        vu = trouves[0].CastTo(aides["CanPlaceCounter"]).GetCounters(compteur)
        if vu != n:
            soucis.append(f"{cid}.{compteur} = {vu} (attendu {n})")
    sauvegarde = cas["attendu"]
    cas["attendu"] = attendu
    try:
        ok, msg = etat_attendu(monde, aides)
    finally:
        cas["attendu"] = sauvegarde
    if not ok:
        soucis.append(msg)
    if soucis:
        return False, " ; ".join(soucis)
    return True, msg
'''


CAS = [
    # ============================================================ dz004 "Beautiful Dreamer"
    _c("dz004 Beautiful Dreamer : Hero Action, 3 menaces retirees d'un complot annexe a 2 (vaincu) puis 2 de plus sur un AUTRE",
       "« Remove 3 threat from a scheme. If this removes the last threat from that scheme, you may remove 2 threat "
       "from another scheme » : Bomb Scare (2) tombe a 0, le bonus part sur le complot principal (5 -> 3)",
       [HEROINE], [*en_jeu("01109"), menace(COMPLOT, 5)],
       {"menace": [[COMPLOT, 3]], "hors_jeu": ["01109"]},
       main_exclusive=["dz004", "01089"], cibles=["01109", COMPLOT], jouer=["dz004"]),
    _c("dz004 Beautiful Dreamer : Hero Action, la derniere menace n'est PAS retiree -> aucun bonus (6 -> 3, l'annexe garde 2)",
       "temoin de la condition : le complot principal a 6 garde 3 menaces, Bomb Scare (2) n'est pas touche",
       [HEROINE], [*en_jeu("01109"), menace(COMPLOT, 6)],
       {"menace": [[COMPLOT, 3], ["01109", 2]]},
       main_exclusive=["dz004", "01089"], cibles=[COMPLOT, "01109"], jouer=["dz004"]),
    _c("dz004 Beautiful Dreamer : Hero Action, « you MAY » refuse -> le second complot garde sa menace",
       "le bonus est facultatif : refuse (Cancel), le complot principal reste a 5",
       [HEROINE], [*en_jeu("01109"), menace(COMPLOT, 5)],
       {"menace": [[COMPLOT, 5]], "hors_jeu": ["01109"]},
       main_exclusive=["dz004", "01089"], cibles=["01109", COMPLOT], jouer=["dz004"], choisir_option=["Cancel"]),
    _c("dz004 Beautiful Dreamer : Showtime!, 2 menaces retirees d'un complot (Rehearsal, 5 -> 3)",
       "« Showtime!: Remove 2 threat from a scheme », resolu par Rehearsal depuis la Setlist",
       [HEROINE, *dans_setlist("dz004")], [menace(COMPLOT, 5), REPETER],
       {"menace": [[COMPLOT, 3]]},
       main_exclusive=["01088"], cibles=[COMPLOT]),
    # ============================================================ dz005 "Beauty and the Beast"
    _c("dz005 Beauty and the Beast : Hero Action, l'allie cherche dans le deck entre en jeu",
       "« Search your deck for an ally and put it into play » : deck = fond + Jessica Jones (01059), seul allie",
       [HEROINE, SANS_DECK, "Puzzle.CreatePlayerDeck('01088', '01088', '01088', '01088', '01088', '01088', '01059', '01088')"],
       [], {"en_jeu": ["01059"]},
       main_exclusive=["dz005", "01089"], jouer=["dz005"]),
    _c("dz005 Beauty and the Beast : Hero Action, l'allie encore en jeu a la fin de la phase revient en MAIN",
       "« If that ally is still in play at the end of the phase, add it to your hand » : fin de la phase des joueurs",
       [HEROINE, SANS_DECK, "Puzzle.CreatePlayerDeck('01088', '01088', '01088', '01088', '01088', '01088', '01059', '01088')"],
       [], {"en_main": ["01059"], "hors_jeu": ["01059"]},
       main_exclusive=["dz005", "01089"], jouer=["dz005"], declencher_apres=[FIN_DE_PHASE]),
    _c("dz005 Beauty and the Beast : Hero Action, l'allie vaincu avant la fin de la phase ne revient PAS en main",
       "contre-cas de « still in play » : Jessica Jones (3 PV) vaincue avant la fin de phase reste dans la defausse",
       [HEROINE, SANS_DECK, "Puzzle.CreatePlayerDeck('01088', '01088', '01088', '01088', '01088', '01088', '01059', '01088')"],
       [], {"defausse": ["01059"], "absent_main": ["01059"]},
       main_exclusive=["dz005", "01089"], jouer=["dz005"],
       declencher_apres=["Puzzle.Damage('01059', 3)", FIN_DE_PHASE]),
    _c("dz005 Beauty and the Beast : Showtime!, +2 THW a l'heroine (Rehearsal)",
       "« Showtime!: Give a friendly character +2 THW until the end of the phase »",
       [HEROINE, *dans_setlist("dz005")], [REPETER],
       {"attributs": {"thwart": 2}},
       main_exclusive=["01088"], cibles=["dz001a"]),
    _c("dz005 Beauty and the Beast : Showtime!, le bonus tombe a la fin de la phase",
       "« until the end of the phase » : apres la fin de la phase des joueurs, THW revient a l'imprime",
       [HEROINE, *dans_setlist("dz005")], [REPETER],
       {"attributs": {"thwart": 0}},
       main_exclusive=["01088"], cibles=["dz001a"], declencher_apres=[FIN_DE_PHASE]),
    _c("dz005 Beauty and the Beast : Showtime!, un personnage ami d'un AUTRE joueur est une cible legale (+2 THW a Spider-Man)",
       "« a FRIENDLY character » : tout personnage du cote des joueurs, pas seulement ceux du joueur de Dazzler "
       "(le module visait `YouControlUnit` jusqu'au 20/10/2026). Partie a DEUX, Spider-Man (01001a) choisi",
       [HEROINE, "Puzzle.ChangeForm('01001b')", *dans_setlist("dz005")], [REPETER],
       {"attributs_carte": [["01001a", "thwart", 2]]},
       main_exclusive=["01088"], choisir_option=["Spider-Man"], heros2="spider_man"),
    # ============================================================ dz006 "Doll"
    _c("dz006 Doll : Hero Interrupt, l'activation du vilain contre le joueur de Dazzler est annulee (0 degat)",
       "« When the villain would activate against you, cancel that activation » : Rhino (ATK 2) attaque l'heroine "
       "inclinee (pas de defense), Doll en main avec de quoi payer : aucun degat",
       [HEROINE, "Puzzle.Exhaust('dz001a')"], ["Puzzle.Attack('01094')"],
       {"degats_identite": 0},
       main_exclusive=["dz006", "01089"]),
    _c("dz006 Doll : Hero Interrupt, l'activation d'un SBIRE n'est pas annulee (Shocker, 2 degats)",
       "« the VILLAIN » seulement : un sbire qui s'active contre le joueur frappe normalement",
       [HEROINE, "Puzzle.Exhaust('dz001a')", *en_jeu("01103")], ["Puzzle.Attack('01103')"],
       {"degats_identite": 2},
       main_exclusive=["dz006", "01089"]),
    _c("dz006 Doll : Hero Interrupt, l'activation du vilain contre un AUTRE joueur n'est pas annulee",
       "« against YOU » : partie a DEUX, Rhino attaque Peter Parker (01001b), Doll reste en main et Peter "
       "encaisse 2 degats (le filtre du joueur vise manquait jusqu'au 20/10/2026). L'heroine est inclinee : "
       "sinon elle defend pour Peter (regle legale) et le cas ne mesure plus rien",
       [HEROINE, "Puzzle.Exhaust('dz001a')"], ["Puzzle.Attack('01094', against='01001b')"],
       {"degats": [["01001b", 2]], "en_main": ["dz006"]},
       main_exclusive=["dz006", "01089"], heros2="spider_man"),
    _c("dz006 Doll : Showtime!, l'identite du joueur recoit une carte Tough (Rehearsal)",
       "« Showtime!: Give your identity a tough status card »",
       [HEROINE, *dans_setlist("dz006")], [REPETER],
       {"statuts": [["dz001a", "Tough"]]},
       main_exclusive=["01088"]),
    # ============================================================ dz007 "Hush Now Baby"
    _c("dz007 Hush Now Baby : Hero Action, l'ennemi choisi est etourdi ET desoriente (Rhino)",
       "« Stun and confuse an enemy » : UNE cible recoit les DEUX statuts",
       [HEROINE], [], {"statuts": [["01094", "Stunned"], ["01094", "Confused"]]},
       main_exclusive=["dz007", "01088", "01089"], cibles=["01094"], jouer=["dz007"]),
    _c("dz007 Hush Now Baby : Hero Action, un ennemi DEJA etourdi reste une cible legale et devient desoriente",
       "carte officielle de meme texte, 04036 Pheromones : `canbe_status=[\"Stunned\", \"Confused\"]` (l'un OU "
       "l'autre). Le module exigeait `canbe_stunned` jusqu'au 20/10/2026 : Shocker deja etourdi etait ecarte",
       [HEROINE, *en_jeu("01103"), "Puzzle.Stun(Puzzle.FindFaceInPlay('01103'))"], [],
       {"statuts": [["01103", "Stunned"], ["01103", "Confused"]], "statuts_absents": [["01094", "Confused"]]},
       main_exclusive=["dz007", "01088", "01089"], cibles=["01103"], jouer=["dz007"]),
    _c("dz007 Hush Now Baby : Showtime!, CHAQUE joueur pioche 1 carte (partie a deux)",
       "« Showtime!: Each player draws 1 card » : la main de Dazzler passe de 1 a 2, celle de Peter Parker de 6 a 7",
       [HEROINE, *dans_setlist("dz007")], [REPETER],
       {"mains": [[0, 2], [1, 7]]},
       main_exclusive=["01088"], heros2="spider_man", verifier="dz_etat"),
    # ============================================================ dz008 "In the Darkest Light"
    _c("dz008 In the Darkest Light : Hero Action, 2 degats a CHAQUE ennemi (Rhino et Shocker)",
       "« Deal 2 damage to each enemy » : le vilain et le sbire, sans selection",
       [HEROINE, *en_jeu("01103")], [], {"degats": [["01094", 2], ["01103", 2]]},
       main_exclusive=["dz008", "01089"], jouer=["dz008"]),
    _c("dz008 In the Darkest Light : Showtime!, le sbire choisi est etourdi (Shocker)",
       "« Showtime!: Stun a non-ELITE enemy » : Rhino et Shocker sont candidats, Shocker choisi",
       [HEROINE, *en_jeu("01103"), *dans_setlist("dz008")], [REPETER],
       {"statuts": [["01103", "Stunned"]], "statuts_absents": [["01094", "Stunned"]]},
       main_exclusive=["01088"], choisir_option=["Shocker"]),
    _c("dz008 In the Darkest Light : Showtime!, un sbire ELITE n'est pas une cible (Klaw ecarte, Rhino etourdi)",
       "« non-ELITE » : Klaw (dz020, ELITE) en jeu, seul Rhino est candidat et le recoit",
       [HEROINE, *en_jeu("dz020"), *dans_setlist("dz008")], [REPETER],
       {"statuts": [["01094", "Stunned"]], "statuts_absents": [["dz020", "Stunned"]]},
       main_exclusive=["01088"]),
    # ============================================================ dz009 "Out and Proud"
    _c("dz009 Out and Proud : Hero Action, le sbire non-ELITE choisi est vaincu (Shocker)",
       "« Defeat a non-ELITE minion » : Shocker (3 PV, aucun degat) quitte le jeu",
       [HEROINE, *en_jeu("01103")], [], {"hors_jeu": ["01103"]},
       main_exclusive=["dz009", "01088", "01089"], cibles=["01103"], jouer=["dz009"]),
    _c("dz009 Out and Proud : Hero Action, un sbire ELITE n'est pas une cible (seul Klaw en jeu : la carte reste en main)",
       "« non-ELITE » : sans autre sbire, aucune cible legale, la carte n'est pas jouee et Klaw reste en jeu",
       [HEROINE, *en_jeu("dz020")], [], {"en_jeu": ["dz020"], "jouable": [["dz009", False]]},
       main_exclusive=["dz009", "01088", "01089"], verifier="dz_etat"),
    _c("dz009 Out and Proud : Hero Action, temoin de jouabilite (Klaw ET Shocker en jeu : la carte est jouable)",
       "temoin du cas precedent : le meme montage avec un sbire non-ELITE rend la carte jouable",
       [HEROINE, *en_jeu("dz020", "01103")], [], {"jouable": [["dz009", True]]},
       main_exclusive=["dz009", "01088", "01089"], verifier="dz_etat"),
    _c("dz009 Out and Proud : Showtime!, 1 degat soigne sur CHAQUE allie en jeu (2 -> 1 et 1 -> 0)",
       "« Showtime!: Heal 1 damage from each ally in play » : deux allies blesses",
       [HEROINE, *en_jeu("01059", "01020"), "Puzzle.Damage('01059', 2)", "Puzzle.Damage('01020', 1)",
        *dans_setlist("dz009")], [REPETER],
       {"degats": [["01059", 1], ["01020", 0]]},
       main_exclusive=["01088"]),
    # ============================================================ dz010 "Rich Angel"
    _c("dz010 Rich Angel : Hero Interrupt, tous les degats d'une ATTAQUE contre l'heroine sont prevenus (Rhino, 0 degat)",
       "« When you would take any amount of damage from an attack, prevent all of that damage » : heroine inclinee "
       "(pas de defense de base), Rhino ATK 2",
       [HEROINE, "Puzzle.Exhaust('dz001a')"], ["Puzzle.Attack('01094')"],
       {"degats_identite": 0},
       main_exclusive=["dz010", "01088"]),
    _c("dz010 Rich Angel : Hero Interrupt, des degats qui ne viennent PAS d'une attaque ne sont pas prevenus (3 degats)",
       "« from an ATTACK » : 3 degats directs (Puzzle.Damage) sont encaisses, la carte reste en main",
       [HEROINE], ["Puzzle.Damage('dz001a', 3)"],
       {"degats_identite": 3, "en_main": ["dz010"]},
       main_exclusive=["dz010", "01088"]),
    _c("dz010 Rich Angel : Showtime!, 2 degats soignes sur l'identite du joueur (3 -> 1)",
       "« Showtime!: Heal 2 damage from an identity »",
       [HEROINE, "Puzzle.Damage('dz001a', 3)", *dans_setlist("dz010")], [REPETER],
       {"degats_identite": 1},
       main_exclusive=["01088"]),
    _c("dz010 Rich Angel : Showtime!, l'identite d'un AUTRE joueur peut etre soignee (Spider-Man 3 -> 1)",
       "« an identity » : n'importe laquelle, partie a deux, Spider-Man choisi",
       [HEROINE, "Puzzle.ChangeForm('01001b')", "Puzzle.Damage('01001a', 3)", "Puzzle.Damage('dz001a', 3)",
        *dans_setlist("dz010")], [REPETER],
       {"degats": [["01001a", 1]], "degats_identite": 3},
       main_exclusive=["01088"], heros2="spider_man", choisir_option=["Spider-Man"]),
    # ============================================================ dz011 "The Serpent is Coming"
    _c("dz011 The Serpent is Coming : Hero Action (attack), 6 degats a l'ennemi choisi (Rhino)",
       "« Deal 6 damage to an enemy »",
       [HEROINE], [], {"degats": [["01094", 6]]},
       main_exclusive=["dz011", "01088", "01089"], cibles=["01094"], jouer=["dz011"]),
    _c("dz011 The Serpent is Coming : Hero Action, l'attaque est A DISTANCE (Riposte 2 ignoree)",
       "« This attack gains ranged » : Tracksuit Mafioso (60202, Retaliate 2) garde en vie par une carte Tough ; "
       "une attaque sans distance ferait encaisser 2 degats a l'heroine. La carte Tough consommee prouve "
       "que l'attaque a bien eu lieu",
       [HEROINE, "Puzzle.Tough(Puzzle.PutIntoPlay('60202'))"], [],
       {"degats_identite": 0, "en_jeu": ["60202"], "statuts_absents": [["60202", "Tough"]]},
       main_exclusive=["dz011", "01088", "01089"], cibles=["60202"], jouer=["dz011"]),
    _c("dz011 The Serpent is Coming : Showtime!, 2 degats a un ennemi (Rhino)",
       "« Showtime!: Deal 2 damage to an enemy »",
       [HEROINE, *dans_setlist("dz011")], [REPETER],
       {"degats": [["01094", 2]]},
       main_exclusive=["01088"]),
    # ============================================================ dz012 "Too Good to be True"
    _c("dz012 Too Good to be True : Hero Action, pioche 3 puis defausse 1 carte choisie (main 0 -> 2, deck 5 -> 2)",
       "« Draw 3 cards. Choose and discard 1 card from your hand » : la main ne contient que la carte et Genius "
       "(paiement) ; apres la pioche de 3 et la defausse de 1, il reste 2 cartes en main",
       [HEROINE, SANS_DECK, "Puzzle.CreatePlayerDeck('01090', '01090', '01090', '01090', '01090')"], [],
       {"taille_main": 2, "deck_joueur_taille": [[0, 2]]},
       main_exclusive=["dz012", "01089"], jouer=["dz012"], verifier="dz_etat"),
    _c("dz012 Too Good to be True : Showtime!, 3 cartes de la defausse sont melangees dans le deck (defausse de 3 exactement)",
       "« Showtime!: Shuffle 3 cards from your discard pile into your deck » : defausse construite de 3 cartes, "
       "deck de 2 -> 5, defausse videe. Le CHOIX des 3 quand la defausse en a plus est une question ouverte "
       "(`.planning/todos/2026-10-20-backlog-12-questions.md`)",
       [HEROINE, SANS_DECK, "Puzzle.CreatePlayerDeck('01090', '01090')", *dans_setlist("dz012")],
       [VIDER_DEFAUSSE, "Puzzle.CreatePlayerDiscardPile('01092', '01093', '01064')", REPETER],
       {"deck_joueur_taille": [[0, 5]]},
       main_exclusive=["01088"], verifier="dz_etat"),
    # ============================================================ dz013 "Velvet Sky"
    _c("dz013 Velvet Sky : Hero Interrupt, la traitrise revelee est annulee et defaussee (Stampede : aucune attaque)",
       "« When a treachery is revealed from the encounter deck, cancel all of its effects and discard it » : "
       "Stampede (01106, « Rhino attacks you ») revelee, heroine inclinee : 0 degat, Stampede en defausse rencontre",
       [HEROINE, "Puzzle.Exhaust('dz001a')"], ["Puzzle.Reveal('01106')"],
       {"degats_identite": 0, "defausse_rencontre": ["01106"]},
       main_exclusive=["dz013", "01088"]),
    _c("dz013 Velvet Sky : Showtime!, une carte de statut retiree d'un personnage ami (heroine etourdie)",
       "« Showtime!: Remove a status card from a friendly character »",
       [HEROINE, "Puzzle.Stun('dz001a')", *dans_setlist("dz013")], [REPETER],
       {"statuts_absents": [["dz001a", "Stunned"]]},
       main_exclusive=["01088"]),
    _c("dz013 Velvet Sky : Showtime!, le personnage ami d'un AUTRE joueur est une cible (Spider-Man desoriente)",
       "« a FRIENDLY character » : partie a deux, Spider-Man (01001a) desoriente, choisi ; le module visait "
       "`YouControlUnit` jusqu'au 20/10/2026",
       [HEROINE, "Puzzle.ChangeForm('01001b')", "Puzzle.Confuse('01001a')", "Puzzle.Stun('dz001a')",
        *dans_setlist("dz013")], [REPETER],
       {"statuts_absents": [["01001a", "Confused"]], "statuts": [["dz001a", "Stunned"]]},
       main_exclusive=["01088"], heros2="spider_man", choisir_option=["Spider-Man"]),
    _c("dz013 Velvet Sky : Showtime!, avec DEUX statuts le joueur choisit lequel retirer (Tough retire, Stunned reste)",
       "« Remove A status card » : une seule, au choix du joueur (RECETTES §2, « plusieurs statuts -> le CHOIX "
       "revient au joueur »). L'ancien helper retirait d'office Stunned avant Tough",
       [HEROINE, "Puzzle.Stun('dz001a')", "Puzzle.Tough('dz001a')", *dans_setlist("dz013")], [REPETER],
       {"statuts": [["dz001a", "Stunned"]], "statuts_absents": [["dz001a", "Tough"]]},
       main_exclusive=["01088"], choisir_option=["Discard_a_Tough_status_card"]),
    _c("dz013 Velvet Sky : Showtime!, une carte d'etat d'un autre genre (Dazed) est aussi retiree",
       "« a status card » : toutes les cartes d'etat du moteur (Dazed, Exposed, Cloaked...), pas seulement "
       "Stunned / Confused / Tough que l'ancien helper connaissait",
       [HEROINE, "Puzzle.Daze('dz001a')", *dans_setlist("dz013")], [REPETER],
       {"statuts_absents": [["dz001a", "Dazed"]]},
       main_exclusive=["01088"]),
    # ============================================================ dz014 Lightbringr
    _c("dz014 Lightbringr : Alter-Ego Action, incliner -> un evenement SONG de la main est glisse FACE CACHEE dessous",
       "« Exhaust Lightbringr -> attach 1 SONG event from your hand facedown here »",
       [*en_jeu("dz014")], ["Puzzle.Action('dz014', 'AlterEgoAction')"],
       {"face_cachee_sous": [["dz014", "dz004", True]], "taille_pose_sous": [["dz014", 1]], "exhausted": ["dz014"]},
       main_exclusive=["dz004", "01088"], verifier="dz_etat"),
    _c("dz014 Lightbringr : Alter-Ego Action, plafond de 3 cartes (la 4e reste en main)",
       "« (to a maximum of 3) » : trois chansons deja dessous, l'action n'est plus offerte",
       [*en_jeu("dz014"), "Puzzle.PlaceUnder('dz007', 'dz014')", "Puzzle.PlaceUnder('dz008', 'dz014')",
        "Puzzle.PlaceUnder('dz009', 'dz014')"], [],
       {"taille_pose_sous": [["dz014", 3]], "en_main": ["dz004"], "pret": ["dz014"]},
       main_exclusive=["dz004", "01088"], declencher_tolerant=["Puzzle.Action('dz014', 'AlterEgoAction')"]),
    _c("dz014 Lightbringr : Alter-Ego Action, un evenement NON SONG ne peut pas etre glisse",
       "« 1 SONG event » : seule For Justice! (01060, evenement sans SONG) en main, rien n'est glisse",
       [*en_jeu("dz014")], [],
       {"taille_pose_sous": [["dz014", 0]], "en_main": ["01060"]},
       main_exclusive=["01060"], declencher_tolerant=["Puzzle.Action('dz014', 'AlterEgoAction')"]),
    _c("dz014 Lightbringr : une chanson glissee dessous se JOUE comme depuis la main, 1 ressource de moins (cout 2 paye avec 1)",
       "« Events attached to Lightbringr may be played as if they were in your hand. Reduce the resource cost of "
       "cards played this way by 1 » : Beautiful Dreamer (cout 2) dessous, une seule carte a 1 ressource en main "
       "(Longshot, dz002) : jouable seulement avec la reduction. Menace 6 -> 3",
       [HEROINE, *en_jeu("dz014"), "Puzzle.PlaceUnder('dz004', 'dz014')"], [menace(COMPLOT, 6)],
       {"menace": [[COMPLOT, 3]], "taille_pose_sous": [["dz014", 0]]},
       main_exclusive=["dz002"], cibles=[COMPLOT], jouer_sous=[["dz014", "dz004"]]),
    _c("dz014 Lightbringr : la reduction ne vaut PAS pour une carte jouee depuis la main (temoin, menace inchangee)",
       "« cards played THIS WAY » : la meme chanson jouee depuis la main, payee avec Longshot seul, reste impayable",
       [HEROINE, *en_jeu("dz014")], [menace(COMPLOT, 6)],
       {"menace": [[COMPLOT, 6]], "en_main": ["dz004"]},
       main_exclusive=["dz004", "dz002"], cibles=[COMPLOT], ne_pas_depenser=["dz004"], jouer=["dz004"]),
    # ============================================================ dz015 Dazzler's Rollerskates
    _c("dz015 Dazzler's Rollerskates : l'amelioration se joue depuis la main (cout 2 paye)",
       "carte sans « Attach to » : elle entre en jeu dans la zone du joueur",
       [HEROINE], [], {"en_jeu": ["dz015"]},
       main_exclusive=["dz015", "01088"], jouer=["dz015"]),
    _c("dz015 Dazzler's Rollerskates : Hero Action, incliner les patins -> Dazzler se redresse",
       "« Exhaust Dazzler's Rollerskates -> ready Dazzler »",
       [HEROINE, *en_jeu("dz015"), "Puzzle.Exhaust('dz001a')"], ["Puzzle.Action('dz015', 'HeroAction')"],
       {"pret": ["dz001a"], "exhausted": ["dz015"]},
       main_exclusive=["01088"]),
    _c("dz015 Dazzler's Rollerskates : Hero Action, patins deja inclines -> pas d'action, Dazzler reste inclinee",
       "le cout « Exhaust Dazzler's Rollerskates » doit pouvoir etre paye",
       [HEROINE, *en_jeu("dz015"), "Puzzle.Exhaust('dz001a')", "Puzzle.Exhaust('dz015')"], [],
       {"exhausted": ["dz001a", "dz015"]},
       main_exclusive=["01088"], declencher_tolerant=["Puzzle.Action('dz015', 'HeroAction')"]),
    _c("dz015 Dazzler's Rollerskates : pas de Hero Action en alter ego (Alison reste inclinee)",
       "« Hero Action » : jouable en forme heros seulement",
       [*en_jeu("dz015"), "Puzzle.Exhaust('dz001b')"], [],
       {"exhausted": ["dz001b"], "pret": ["dz015"]},
       main_exclusive=["01088"], declencher_tolerant=["Puzzle.Action('dz015', 'HeroAction')"]),
    # ============================================================ dz016 Sound Collector Suit
    # (« Dazzler gets +1 DEF » : cas historique « dz016 Sound Collector Suit — Dazzler gagne +1 DEF » de test_capacites.py)
    _c("dz016 Sound Collector Suit : Resource, l'energie generee paie une CHANSON (cout 2 = Longshot + la combinaison)",
       "« Exhaust Sound Collector Suit -> generate a [energy] resource for a SONG » : Beautiful Dreamer (cout 2) payee "
       "avec Longshot (1 ressource) et la combinaison ; menace 6 -> 3",
       [HEROINE, *en_jeu("dz016")], [menace(COMPLOT, 6)],
       {"menace": [[COMPLOT, 3]], "exhausted": ["dz016"]},
       main_exclusive=["dz004", "dz002"], ne_pas_depenser=["dz004"], cibles=[COMPLOT], jouer=["dz004"]),
    _c("dz016 Sound Collector Suit : Resource, l'energie ne paie PAS une carte sans SONG (For Justice! reste en main)",
       "« for a SONG » : For Justice! (01060, cout 2, sans SONG) avec Longshot seul et la combinaison : impayable",
       [HEROINE, *en_jeu("dz016")], [menace(COMPLOT, 6)],
       {"menace": [[COMPLOT, 6]], "en_main": ["01060"], "pret": ["dz016"]},
       main_exclusive=["01060", "dz002"], ne_pas_depenser=["01060"], cibles=[COMPLOT], jouer=["01060"]),
    _c("dz016 Sound Collector Suit : incliner -> retirer 1 compteur sound d'une chanson de la Setlist (lecture actuelle : Action)",
       "« or remove 1 sound counter from a SONG in the Setlist » : Rehearsal marque Beautiful Dreamer, la combinaison "
       "efface la marque. ⚠ Le MOMENT ou cette branche s'utilise est une question ouverte (Q2) : le module en fait "
       "une Action ; ce cas mesure l'effet, pas la fenetre",
       [HEROINE, *en_jeu("dz016"), *dans_setlist("dz004")], [menace(COMPLOT, 6), REPETER, "Puzzle.Action('dz016', 'Action')"],
       {"compteurs_setlist": [["dz004", "sound", 0]], "exhausted": ["dz016"], "menace": [[COMPLOT, 4]]},
       main_exclusive=["01088"], cibles=[COMPLOT], verifier="dz_etat"),
    # ============================================================ dz017a Live Concert
    # (Setup : cas historique « dz017a Live Concert — Setup : posee en jeu par Alison Blaire » de test_capacites.py)
    _c("dz017a Live Concert : Response, une chanson jouee et resolue est rangee dans la Setlist",
       "« After you resolve a SONG event attach it here [...] This is the Setlist » : Beautiful Dreamer jouee "
       "(menace 6 -> 3) puis rangee sous Live Concert, pas en defausse",
       [HEROINE], [menace(COMPLOT, 6)],
       {"menace": [[COMPLOT, 3]], "setlist": ["dz004"]},
       main_exclusive=["dz004", "01089"], cibles=[COMPLOT], jouer=["dz004"], verifier="dz_etat"),
    _c("dz017a Live Concert : Response, plafond de 4 (une 5e chanson part en defausse)",
       "« (to a maximum of 4) » : Setlist deja pleine, Beautiful Dreamer jouee va a la defausse",
       [HEROINE, *dans_setlist("dz007", "dz008", "dz009", "dz010")], [menace(COMPLOT, 6)],
       {"menace": [[COMPLOT, 3]], "setlist": ["dz007", "dz008", "dz009", "dz010"], "defausse": ["dz004"]},
       main_exclusive=["dz004", "01089"], cibles=[COMPLOT], jouer=["dz004"], verifier="dz_etat"),
    _c("dz017a Live Concert : Response, un evenement SANS SONG n'est pas range (For Justice! en defausse)",
       "« a SONG event » : For Justice! (01060) jouee, Setlist vide",
       [HEROINE], [menace(COMPLOT, 6)],
       {"setlist": [], "defausse": ["01060"]},
       main_exclusive=["01060", "01088"], cibles=[COMPLOT], jouer=["01060"], verifier="dz_etat"),
    _c("dz017a Live Concert : Hero Action, retourner sur Showtime! et le reveler (Setlist resolue puis videe)",
       "« Flip this card to its Showtime! side and reveal it » : le When Revealed de dz017b part (Beautiful Dreamer "
       "retire 2 menaces), la Setlist est defaussee, la carte revient sur Live Concert",
       [HEROINE, *dans_setlist("dz004")], [menace(COMPLOT, 6), "Puzzle.Action('dz017a', 'HeroAction')"],
       {"menace": [[COMPLOT, 4]], "setlist": [], "defausse": ["dz004"], "en_jeu": ["dz017a"]},
       main_exclusive=["01088"], cibles=[COMPLOT], verifier="dz_etat"),
    # ============================================================ dz017b Showtime!
    _c("dz017b Showtime! : When Revealed, chaque Showtime! de la Setlist est resolu puis la Setlist est defaussee (2 cartes)",
       "« Resolve the Showtime! ability on each card in the Setlist [...] Then, discard all cards from the Setlist » : "
       "Beautiful Dreamer (2 menaces) et The Serpent is Coming (2 degats) ; pas de bonus a 2 cartes",
       [HEROINE, *dans_setlist("dz004", "dz011")], [menace(COMPLOT, 6), "Puzzle.Action('dz017a', 'HeroAction')"],
       {"menace": [[COMPLOT, 4]], "degats": [["01094", 2]], "setlist": [], "defausse": ["dz004", "dz011"]},
       main_exclusive=["01088"], cibles=[COMPLOT, "01094"], verifier="dz_etat"),
    _c("dz017b Showtime! : When Revealed, 4 cartes defaussees -> 4 degats a un ennemi en prime",
       "« If 4 cards were discarded this way, you may either deal 4 damage to an enemy or remove 4 threat from a "
       "scheme » : Setlist de 4, premiere branche choisie (degats) : Rhino 2 (Serpent) + 4 = 6",
       [HEROINE, *dans_setlist("dz004", "dz011", "dz007", "dz009")],
       [menace(COMPLOT, 6), "Puzzle.Action('dz017a', 'HeroAction')"],
       {"menace": [[COMPLOT, 4]], "degats": [["01094", 6]], "setlist": []},
       main_exclusive=["01088"], cibles=[COMPLOT, "01094"], choisir_option=["Deal_4_damage"], verifier="dz_etat"),
    _c("dz017b Showtime! : When Revealed, 4 cartes -> la prime peut etre 4 menaces retirees",
       "seconde branche de la prime : complot principal 6 -> 0 (Beautiful Dreamer 2 + prime 4)",
       [HEROINE, *dans_setlist("dz004", "dz011", "dz007", "dz009")],
       [menace(COMPLOT, 6), "Puzzle.Action('dz017a', 'HeroAction')"],
       {"menace": [[COMPLOT, 0]], "degats": [["01094", 2]], "setlist": []},
       main_exclusive=["01088"], cibles=[COMPLOT, "01094"], choisir_option=["Remove_4_threat"], verifier="dz_etat"),
    _c("dz017b Showtime! : When Revealed, 3 cartes seulement -> AUCUNE prime (Rhino 2 degats)",
       "« If 4 cards were discarded » : a 3, pas de prime",
       [HEROINE, *dans_setlist("dz004", "dz011", "dz007")],
       [menace(COMPLOT, 6), "Puzzle.Action('dz017a', 'HeroAction')"],
       {"menace": [[COMPLOT, 4]], "degats": [["01094", 2]], "setlist": []},
       main_exclusive=["01088"], cibles=[COMPLOT, "01094"], verifier="dz_etat"),
    _c("dz017b Showtime! : When Revealed, « in any order » : le joueur choisit l'ordre (Doll avant Velvet Sky -> plus de Tough)",
       "« in any order » : Velvet Sky (retirer un statut) est rangee APRES Doll (Tough sur l'identite), donc au "
       "DESSUS de la Setlist, la ou le module commence. Le joueur fait resoudre Doll d'abord, puis Velvet Sky retire "
       "la carte Tough. Dans l'ordre impose par l'ancien module, Velvet Sky ne trouvait aucun statut et la Tough restait",
       [HEROINE, *dans_setlist("dz006", "dz013")], ["Puzzle.Action('dz017a', 'HeroAction')"],
       {"statuts_absents": [["dz001a", "Tough"]], "setlist": []},
       main_exclusive=["01088"], choisir_option=['"Doll"'], verifier="dz_etat"),
    _c("dz017b Showtime! : les chansons defaussees perdent leur compteur sound",
       "le compteur sound est la memoire de Rehearsal DANS la Setlist ; defaussee, une chanson ne doit plus le porter "
       "(sinon, rejouee apres Encore, elle ne serait plus repetable). Rehearsal marque Beautiful Dreamer, puis "
       "Showtime! vide la Setlist",
       [HEROINE, *dans_setlist("dz004")], [menace(COMPLOT, 6), REPETER, "Puzzle.Action('dz017a', 'HeroAction')"],
       {"compteurs_defausse": [["dz004", "sound", 0]], "setlist": []},
       main_exclusive=["01088"], cibles=[COMPLOT], verifier="dz_etat"),
]
