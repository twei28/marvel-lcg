# Cas test_capacites de l'agent D du chantier SHADOWLAND : sets NINJA SWARM (sl028-sl036) et BLACK FLOWER (sl072-sl078). Prefixe de nom `[sld]`.
# Cas montes sur `rhino` (Spider-Man) comme tools/cas/shadowland.py, ou sur le scenario REEL `shadows_in_the_night` (graine 42 = vilain Elektra sl014a).
HEROS = "spider_man"
RIEN = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"]
FORME_HEROS = "Puzzle.ChangeForm('01001b')"
CC = "Puzzle.PutIntoPlay('sl072a,sl072b', under_control=True)"          # la Creeping Corruption du joueur 1, face A (paire visible,verso)
CC_B = "Puzzle.PutIntoPlay('sl072b,sl072a', under_control=True)"        # face B visible


def _s(nom, pourquoi, mise, declencher, attendu, verifier="sld_etat", forme_heros=True, **cle):
    avant = cle.pop("avant_forme", [])   # ⚠ PIEGE : `ChangeForm` remet la menace du complot a 0 -> poser la menace AVANT
    cas = {"nom": "[sld] " + nom, "pourquoi": pourquoi, "scenario": "rhino", "heros": HEROS,
           "mise_en_place": [*RIEN, *avant, *([FORME_HEROS] if forme_heros else []), *mise],
           "declencher": declencher, "verifier": verifier, "attendu": attendu, "main_exclusive": cle.pop("main_exclusive", ["01088"])}
    cas.update(cle)
    return cas


CAS = [
    # ------------------------------------------------------------------------------------------------------ sl072a : Creeping Corruption, face A
    _s("sl072a Action : epuise la carte, pose 1 compteur corruption ICI et pioche 1 carte", "« Exhaust Creeping Corruption and place 1 corruption counter here -> draw 1 card »",
       [CC], ["Puzzle.Action('sl072a', 'Action')"], {"compteurs": [["sl072a", "corruption", 1]], "exhausted": ["sl072a"], "taille_main": 2}),
    _s("sl072a Action, TEMOIN : sans l'Action, ni compteur ni pioche", "la mesure suit l'Action",
       [CC], [], {"compteurs": [["sl072a", "corruption", 0]], "taille_main": 1}),
    _s("sl072a, 5e compteur POSE PAR L'ACTION (4 -> 5) : les compteurs partent, la carte se retourne (face B), la pioche a quand meme lieu", "« If there are at least 5 corruption counters here, remove each of them from here and flip this card »",
       [CC, "Puzzle.Counter('sl072a', 'corruption', 4)"], ["Puzzle.Action('sl072a', 'Action')"],
       {"compteurs": [["sl072b", "corruption", 0]], "face_visible": [["sl072", "sl072b"]], "taille_main": 2}),
    _s("sl072a, pose de 2 d'un coup (4 -> 6) : TOUS les compteurs partent (pas seulement 5) et la carte se retourne", "« remove EACH of them from here »",
       [CC, "Puzzle.Counter('sl072a', 'corruption', 4)", "Puzzle.Counter('sl072a', 'corruption', 2)"], [],
       {"compteurs": [["sl072b", "corruption", 0]], "face_visible": [["sl072", "sl072b"]]}),
    _s("sl072a, TEMOIN : 4 compteurs seulement, la carte reste face A", "le seuil est de 5",
       [CC, "Puzzle.Counter('sl072a', 'corruption', 4)"], [], {"compteurs": [["sl072a", "corruption", 4]], "face_visible": [["sl072", "sl072a"]]}),
    # ------------------------------------------------------------------------------------------------------ sl072b : Creeping Corruption, face B
    _s("sl072b Action : epuise la carte, pose 1 compteur, pioche 2 cartes puis defausse 1 carte de la main (choisie)", "« draw 2 cards, then discard 1 card from your hand »",
       [CC_B], ["Puzzle.Action('sl072b', 'Action')"], {"compteurs": [["sl072b", "corruption", 1]], "exhausted": ["sl072b"], "taille_main": 2}),
    _s("sl072b, 5e compteur : le joueur est vaincu (la partie est perdue : seul joueur elimine)", "« If there are at least 5 corruption counters here, you are defeated »",
       [CC_B, "Puzzle.Counter('sl072b', 'corruption', 5)"], [], {"partie_finie": True}),
    _s("sl072b, TEMOIN : 4 compteurs, le joueur n'est pas vaincu", "le seuil est de 5",
       [CC_B, "Puzzle.Counter('sl072b', 'corruption', 4)"], [], {"partie_finie": False, "compteurs": [["sl072b", "corruption", 4]]}),
    _s("sl072b, 5e compteur POSE PAR L'ACTION (4 -> 5) : defaite", "le cout pose le 5e compteur",
       [CC_B, "Puzzle.Counter('sl072b', 'corruption', 4)"], ["Puzzle.Action('sl072b', 'Action')"], {"partie_finie": True}),
    _s("sl072a/b : le trait OVERPOWERING est sur la face B seulement", "le trait est imprime sur la face B",
       [CC_B], [], {"traits_de": [["sl072b", "OVERPOWERING"]]}),
]


VERIFICATIONS = r'''
def sld_etat(monde, aides):
    """etat_attendu + les cles de l'agent D :
         face_visible        [[prefixe, card_id]] la face MONTREE de la carte (deux faces = un prefixe)
         partie_finie        bool
         corruption_joueurs  [[indice_joueur, n_compteurs, card_id_visible]] la Creeping Corruption de CHAQUE joueur (deux heros : meme card_id)"""
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    soucis = []
    for prefixe, voulu in attendu.get("face_visible") or []:
        vues = []
        for objet in monde.object_manager.card_dict.values():
            face = getattr(objet, "face", None)
            cid = str(getattr(getattr(face, "paper", None), "card_id", ""))
            if cid.startswith(prefixe) and cid not in vues:
                vues.append(cid)
        if vues != [voulu]:
            soucis.append(f"faces montrees pour {prefixe} : {vues} (attendu {voulu})")
    if "partie_finie" in attendu and bool(monde.is_game_over) != attendu["partie_finie"]:
        soucis.append(f"partie finie = {bool(monde.is_game_over)} (attendu {attendu['partie_finie']})")
    for indice, n, voulu in attendu.get("corruption_joueurs") or []:
        joueur = monde.const_players[indice]
        cc = [f for f in joueur.GetControlUpgrade() if str(f.paper.card_id) in ("sl072a", "sl072b")]
        if len(cc) != 1:
            soucis.append(f"joueur {indice} : {len(cc)} Creeping Corruption (attendu 1)")
            continue
        vu = cc[0].GetCounters("corruption")
        if vu != n or str(cc[0].paper.card_id) != voulu:
            soucis.append(f"joueur {indice} : {cc[0].paper.card_id} avec {vu} compteurs (attendu {voulu} avec {n})")
    propres = ("face_visible", "partie_finie", "corruption_joueurs")
    reste = {k: v for k, v in attendu.items() if k not in propres}
    cas["attendu"] = reste
    try:
        ok, msg = etat_attendu(monde, aides)
    finally:
        cas["attendu"] = attendu
    if not ok:
        soucis.append(msg)
    return (False, " ; ".join(soucis)) if soucis else (True, "etat conforme")
'''
