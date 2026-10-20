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
CLES_DAZZLER = {'mains', 'setlist', 'compteurs_setlist', 'deck_joueur_taille'}


def dz_etat(monde, aides):
    """etat_attendu + cles propres au pack dazzler :
    - mains : [[rang du joueur, taille]] (taille de la main de CHAQUE joueur, « each player ») ;
    - setlist : liste EXACTE des card_id dans la Setlist (zone posee sous Live Concert, l'une ou l'autre face) ;
    - compteurs_setlist : [[card_id, compteur, n]] sur une carte de la Setlist (hors jeu, donc invisible a `compteurs`) ;
    - deck_joueur_taille : [[rang du joueur, taille]]."""
    cas = aides["cas"]
    attendu = dict(cas.get("attendu") or {})
    propres = {k: attendu.pop(k) for k in list(attendu) if k in CLES_DAZZLER}
    soucis = []
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
       "« a FRIENDLY character » : tout personnage du cote des joueurs, pas seulement ceux que tu controles "
       "(le module visait `YouControlUnit` jusqu'au 20/10/2026). Partie a DEUX, Spider-Man (01001a) choisi",
       [HEROINE, "Puzzle.ChangeForm('01001b')", *dans_setlist("dz005")], [REPETER],
       {"attributs_carte": [["01001a", "thwart", 2]]},
       main_exclusive=["01088"], choisir_option=["Spider-Man"], heros2="spider_man"),
    # ============================================================ dz006 "Doll"
    _c("dz006 Doll : Hero Interrupt, l'activation du vilain contre toi est annulee (0 degat)",
       "« When the villain would activate against you, cancel that activation » : Rhino (ATK 2) attaque l'heroine "
       "inclinee (pas de defense), Doll en main avec de quoi payer : aucun degat",
       [HEROINE, "Puzzle.Exhaust('dz001a')"], ["Puzzle.Attack('01094')"],
       {"degats_identite": 0},
       main_exclusive=["dz006", "01089"]),
    _c("dz006 Doll : Hero Interrupt, l'activation d'un SBIRE n'est pas annulee (Shocker, 2 degats)",
       "« the VILLAIN » seulement : un sbire qui s'active contre toi frappe normalement",
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
    _c("dz006 Doll : Showtime!, ton identite recoit une carte Tough (Rehearsal)",
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
]
