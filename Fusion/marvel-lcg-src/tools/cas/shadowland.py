# Cas test_capacites du pack SHADOWLAND (MC65, prefixe `sl`). Prefixe de nom `[sl]`. Rien n'est teste sur un scenario Shadowland
# tant que celui-ci n'existe pas : on monte la position a la main sur `rhino` (Spider-Man, Whirlwind 01130 en mise en place).
HEROS = "spider_man"
RIEN = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"]
FORME_HEROS = "Puzzle.ChangeForm('01001b')"


def _s(nom, pourquoi, mise, declencher, attendu, **cle):
    avant = cle.pop("avant_forme", [])   # ⚠ PIEGE : `ChangeForm` remet la menace du complot a 0 -> poser la menace AVANT
    cas = {"nom": "[sl] " + nom, "pourquoi": pourquoi, "scenario": "rhino", "heros": HEROS, "mise_en_place": [*RIEN, *avant, FORME_HEROS, *mise],
           "declencher": declencher, "verifier": "sl_etat", "attendu": attendu, "main_exclusive": cle.pop("main_exclusive", ["01088"])}
    cas.update(cle)
    return cas


def _pos(v, h):
    # une carte recto-verso se cree par PAIRE « visible,verso » (comme les complots « 56141a,56141b ») : sans le verso, Flip() ne fait rien
    autre = {"a": "b", "b": "a"}
    return [f"Puzzle.PutIntoPlay('sl003{v},sl003{autre[v]}')", f"Puzzle.PutIntoPlay('sl004{h},sl004{autre[h]}')"]


CAS = [
    # ------------------------------------------------------------------------------------------------------ sl003 : positions du vilain / du heros
    _s("sl003a/sl004a : positions identiques (Streets/Streets) -> chaque personnage a +1 ATK : l'attaque de base inflige 3", "« If both positions are the same: each character gets +1 ATK » (ATK 2 + 1)",
       [*_pos("a", "a"), "Puzzle.PutIntoPlay('01130')"], ["Puzzle.Attack('01001a')"], {"degats": [["01130", 3]]}, cibles=["01130"]),
    _s("sl003b/sl004b : positions identiques (Tenshu/Tenshu) -> +1 ATK aussi (meme texte sur la face b)", "les deux faces de sl003 portent le meme effet",
       [*_pos("b", "b"), "Puzzle.PutIntoPlay('01130')"], ["Puzzle.Attack('01001a')"], {"degats": [["01130", 3]]}, cibles=["01130"]),
    _s("sl003, TEMOIN : sans carte de position, l'attaque de base inflige 2", "la regle seule ajoute le degat",
       ["Puzzle.PutIntoPlay('01130')"], ["Puzzle.Attack('01001a')"], {"degats": [["01130", 2]]}, cibles=["01130"]),
    _s("sl003a/sl004b : positions differentes -> chaque personnage subit 1 degat de moins par attaque : 2 - 1 = 1", "« Reduce the amount of damage each character takes from each attack by 1 »",
       [*_pos("a", "b"), "Puzzle.PutIntoPlay('01130')"], ["Puzzle.Attack('01001a')"], {"degats": [["01130", 1]]}, cibles=["01130"]),
    _s("sl003b/sl004a : positions differentes (l'autre sens) -> 1 degat de moins aussi", "la regle ne depend pas de la face exacte",
       [*_pos("b", "a"), "Puzzle.PutIntoPlay('01130')"], ["Puzzle.Attack('01001a')"], {"degats": [["01130", 1]]}, cibles=["01130"]),
    _s("sl003a/sl004b : positions differentes -> la menace ne peut pas etre retiree du complot principal", "« Threat cannot be removed from the main scheme »",
       [*_pos("a", "b"), "Puzzle.PutIntoPlay('01075', under_control=True)"], ["Puzzle.Thwart('01075')"], {"menace": [["01097b", 5]]}, avant_forme=["Puzzle.SetThreat('01097b', 5)"]),
    _s("sl003a/sl004a : positions identiques -> la menace se retire normalement (temoin)", "le blocage ne vaut que si les positions different",
       [*_pos("a", "a"), "Puzzle.PutIntoPlay('01075', under_control=True)"], ["Puzzle.Thwart('01075')"], {"menace": [["01097b", 3]]}, avant_forme=["Puzzle.SetThreat('01097b', 5)"]),
    # ------------------------------------------------------------------------------------------------------ sl004 : position du heros (First Player Action)
    _s("sl004a, branche 1 : 3 menaces sur le complot et identite etourdie, puis la carte se retourne (sl004b)", "« Resolve one of the effects below, then flip this card »",
       [*_pos("a", "a")], ["Puzzle.Action('sl004a', 'FirstPlayerAction')"], {"menace": [["01097b", 5]], "statuts": [["01001a", "Stunned"]], "face_visible": [["sl004", "sl004b"]]},
       choisir_option="Place_3_threat_on_the_main_scheme_and_stun_your_identity", avant_forme=["Puzzle.SetThreat('01097b', 2)"]),
    _s("sl004b, branche 1 : 3 degats a l'identite, puis la carte se retourne (sl004a)", "face b : « Deal 3 damage to your identity »",
       [*_pos("a", "b")], ["Puzzle.Action('sl004b', 'FirstPlayerAction')"], {"degats_identite": 3, "face_visible": [["sl004", "sl004a"]]},
       choisir_option="Deal_3_damage_to_your_identity"),
    _s("sl004a, branche 2 : depenser [physical][physical] (Strength) puis la carte se retourne", "« Spend [physical][physical] resources »",
       [*_pos("a", "a")], ["Puzzle.Action('sl004a', 'FirstPlayerAction')"], {"face_visible": [["sl004", "sl004b"]], "defausse": ["01090"], "menace": [["01097b", 2]]},
       preferer_option="Spend", payer_avec=["01090"], main_exclusive=["01090"], avant_forme=["Puzzle.SetThreat('01097b', 2)"]),
    _s("sl004a, branche 3 : 1 ressource et epuiser un AERIAL (Falcon) puis la carte se retourne", "« Spend 1 resource of any type and exhaust an AERIAL character you control »",
       [*_pos("a", "a"), "Puzzle.PutIntoPlay('03011', under_control=True)"], ["Puzzle.Action('sl004a', 'FirstPlayerAction')"],
       {"face_visible": [["sl004", "sl004b"]], "exhausted": ["03011"], "statuts_absents": [["01001a", "Stunned"]]}, preferer_option="AERIAL", payer_avec=["01088"], main_exclusive=["01088"], avant_forme=["Puzzle.SetThreat('01097b', 2)"]),
    _s("sl004b, branche 2 : depenser [energy][energy] (Energy) puis la carte se retourne", "« Spend [energy][energy] resources »",
       [*_pos("a", "b")], ["Puzzle.Action('sl004b', 'FirstPlayerAction')"], {"face_visible": [["sl004", "sl004a"]], "defausse": ["01088"], "degats_identite": 0},
       preferer_option="Spend", payer_avec=["01088"], main_exclusive=["01088"]),
    _s("sl004b, branche 3 : defausser un allie que vous controlez puis la carte se retourne", "« Discard an ally or upgrade you control »",
       [*_pos("a", "b"), "Puzzle.PutIntoPlay('01075', under_control=True)"], ["Puzzle.Action('sl004b', 'FirstPlayerAction')"],
       {"face_visible": [["sl004", "sl004a"]], "defausse": ["01075"], "degats_identite": 0}, preferer_option="Discard"),
    _s("sl004a, branche 2, TEMOIN : [physical][physical] impayable (Genius = BB) -> la branche n'est PAS offerte, le pilote retombe sur la branche 1 (menace +3)", "le moteur reduit un choix payant impayable au plus gros morceau payable : on ne l'offre donc que si payable",
       [*_pos("a", "a")], ["Puzzle.Action('sl004a', 'FirstPlayerAction')"], {"face_visible": [["sl004", "sl004b"]], "en_main": ["01089"], "menace": [["01097b", 5]]},
       preferer_option="Spend", main_exclusive=["01089"], avant_forme=["Puzzle.SetThreat('01097b', 2)"]),
    # ------------------------------------------------------------------------------------------------------ sl001a : mise en place du scenario
    {"nom": "[sl] sl001a Setup : les deux The Streets Below en jeu, UN vilain Dark Protege tire face A, ses cartes liees (et elles seules) dans le deck de rencontre",
     "pourquoi": "« Put each The Streets Below environment into play ... Choose 1 random villain ... reveal its side A, then shuffle each card linked to that villain into the encounter deck »",
     "scenario": "shadows_in_the_night", "heros": "spider_man", "mise_en_place": [], "declencher": [], "verifier": "sl_etat",
     "attendu": {"en_jeu": ["sl003a", "sl004a"], "setup_dark_protege": True}, "main_exclusive": ["01088"]},
    {"nom": "[sl] sl001a Setup, graine 1 : le vilain tire et ses cartes liees sont COHERENTS", "pourquoi": "le tirage change avec la graine ; l'invariant (liees = nommant ce vilain, toutes) reste", "scenario": "shadows_in_the_night", "heros": "spider_man",
     "mise_en_place": [], "declencher": [], "verifier": "sl_etat", "attendu": {"en_jeu": ["sl003a", "sl004a"], "setup_dark_protege": True}, "main_exclusive": ["01088"], "graine": 1},
    {"nom": "[sl] sl001a Setup, graine 2 : le vilain tire et ses cartes liees sont COHERENTS", "pourquoi": "le tirage change avec la graine ; l'invariant (liees = nommant ce vilain, toutes) reste", "scenario": "shadows_in_the_night", "heros": "spider_man",
     "mise_en_place": [], "declencher": [], "verifier": "sl_etat", "attendu": {"en_jeu": ["sl003a", "sl004a"], "setup_dark_protege": True}, "main_exclusive": ["01088"], "graine": 2},
    {"nom": "[sl] sl001a Setup, graine 3 : le vilain tire et ses cartes liees sont COHERENTS", "pourquoi": "le tirage change avec la graine ; l'invariant (liees = nommant ce vilain, toutes) reste", "scenario": "shadows_in_the_night", "heros": "spider_man",
     "mise_en_place": [], "declencher": [], "verifier": "sl_etat", "attendu": {"en_jeu": ["sl003a", "sl004a"], "setup_dark_protege": True}, "main_exclusive": ["01088"], "graine": 3},
    {"nom": "[sl] sl001a Setup, graine 4 : le vilain tire et ses cartes liees sont COHERENTS", "pourquoi": "le tirage change avec la graine ; l'invariant (liees = nommant ce vilain, toutes) reste", "scenario": "shadows_in_the_night", "heros": "spider_man",
     "mise_en_place": [], "declencher": [], "verifier": "sl_etat", "attendu": {"en_jeu": ["sl003a", "sl004a"], "setup_dark_protege": True}, "main_exclusive": ["01088"], "graine": 4},
    {"nom": "[sl] sl001a Setup, graine 5 : le vilain tire et ses cartes liees sont COHERENTS", "pourquoi": "le tirage change avec la graine ; l'invariant (liees = nommant ce vilain, toutes) reste", "scenario": "shadows_in_the_night", "heros": "spider_man",
     "mise_en_place": [], "declencher": [], "verifier": "sl_etat", "attendu": {"en_jeu": ["sl003a", "sl004a"], "setup_dark_protege": True}, "main_exclusive": ["01088"], "graine": 5},
    {"nom": "[sl] sl001a Setup, graine 6 : le vilain tire et ses cartes liees sont COHERENTS", "pourquoi": "le tirage change avec la graine ; l'invariant (liees = nommant ce vilain, toutes) reste", "scenario": "shadows_in_the_night", "heros": "spider_man",
     "mise_en_place": [], "declencher": [], "verifier": "sl_etat", "attendu": {"en_jeu": ["sl003a", "sl004a"], "setup_dark_protege": True}, "main_exclusive": ["01088"], "graine": 6},
    {"nom": "[sl] sl001a Setup, graine 7 : le vilain tire et ses cartes liees sont COHERENTS", "pourquoi": "le tirage change avec la graine ; l'invariant (liees = nommant ce vilain, toutes) reste", "scenario": "shadows_in_the_night", "heros": "spider_man",
     "mise_en_place": [], "declencher": [], "verifier": "sl_etat", "attendu": {"en_jeu": ["sl003a", "sl004a"], "setup_dark_protege": True}, "main_exclusive": ["01088"], "graine": 7},
    {"nom": "[sl] sl001a Setup, graine 8 : le vilain tire et ses cartes liees sont COHERENTS", "pourquoi": "le tirage change avec la graine ; l'invariant (liees = nommant ce vilain, toutes) reste", "scenario": "shadows_in_the_night", "heros": "spider_man",
     "mise_en_place": [], "declencher": [], "verifier": "sl_etat", "attendu": {"en_jeu": ["sl003a", "sl004a"], "setup_dark_protege": True}, "main_exclusive": ["01088"], "graine": 8},
    # ------------------------------------------------------------------------------------------------------ sl001b : le vilain se retourne a la place d'etre vaincu
    # ⚠ le vilain est tire au hasard : la graine 42 du harnais donne ELEKTRA (sl014a/sl014b), les cas ci-dessous la nomment.
    {"nom": "[sl] sl001b : le vilain vaincu face A se RETOURNE (face B), ses PV sont remis, chaque joueur recoit 1 carte rencontre face cachee, la position du vilain change",
     "pourquoi": "« When the villain would be defeated on side A, instead flip it to side B, reset its hit points, and change the villain's position. Deal each player 1 facedown encounter card. »",
     "scenario": "shadows_in_the_night", "heros": "spider_man", "mise_en_place": [], "declencher": ["Puzzle.Damage('sl014a', 999)"], "verifier": "sl_etat",
     "attendu": {"vilain_face": "b", "degats": [["sl014b", 0]], "cartes_donnees": [1], "face_visible": [["sl003", "sl003b"]], "partie_finie": False}, "main_exclusive": ["01088"]},
    {"nom": "[sl] sl001b, TEMOIN : un vilain qui n'est PAS vaincu reste face A, position inchangee, aucune carte donnee", "pourquoi": "la regle ne part que sur la defaite",
     "scenario": "shadows_in_the_night", "heros": "spider_man", "mise_en_place": [], "declencher": ["Puzzle.Damage('sl014a', 1)"], "verifier": "sl_etat",
     "attendu": {"vilain_face": "a", "degats": [["sl014a", 1]], "cartes_donnees": [0], "face_visible": [["sl003", "sl003a"]]}, "main_exclusive": ["01088"]},
    {"nom": "[sl] sl001b : vaincu face B, le vilain meurt vraiment et les joueurs GAGNENT (la face B a Toughness : le 1er coup retire son statut Tough, le 2e la vainc)", "pourquoi": "« If the villain is defeated on side B, the players win the game. »",
     "scenario": "shadows_in_the_night", "heros": "spider_man", "mise_en_place": [], "declencher": ["Puzzle.Damage('sl014a', 999)", "Puzzle.Damage('sl014b', 999)", "Puzzle.Damage('sl014b', 999)"],
     "verifier": "sl_etat", "attendu": {"partie_finie": True}, "main_exclusive": ["01088"]},
    # ------------------------------------------------------------------------------------------------------ sl002a : « When Revealed »
    {"nom": "[sl] sl002a Revele : la position du vilain change et le joueur cherche un sbire dans le deck ET la defausse de rencontre, le revele",
     "pourquoi": "« Change the villain's position. Each player searches the encounter deck and discard pile for a minion and reveals it. »",
     "scenario": "shadows_in_the_night", "heros": "spider_man", "mise_en_place": ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105')", "Puzzle.CreateEncounterDiscardPile('sl006')"],
     "declencher": ["Puzzle.AdvanceMainScheme(1)"], "verifier": "sl_etat", "attendu": {"en_jeu": ["sl006"], "face_visible": [["sl003", "sl003b"]]}, "main_exclusive": ["01088"]},
    {"nom": "[sl] sl002a Revele, TEMOIN : sans aucun sbire dans le deck ni la defausse, rien n'entre en jeu (la position change quand meme)", "pourquoi": "la recherche n'est pas obligatoire de reussir",
     "scenario": "shadows_in_the_night", "heros": "spider_man", "mise_en_place": ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105')"],
     "declencher": ["Puzzle.AdvanceMainScheme(1)"], "verifier": "sl_etat", "attendu": {"face_visible": [["sl003", "sl003b"]], "hors_jeu": ["sl006"]}, "main_exclusive": ["01088"]},
    # ------------------------------------------------------------------------------------------------------ mode expert : +1 SCH et +3[per_hero] PV du vilain
    {"nom": "[sl] expert : le vilain a +3 PV par heros (15 -> 18 pour 1 joueur)", "pourquoi": "« In expert mode, the villain gets +1 SCH and +3[per_hero] hit points. »",
     "scenario": "shadows_in_the_night_expert", "heros": "spider_man", "mise_en_place": [], "declencher": [], "verifier": "sl_etat", "attendu": {"vilain_pv_max": 18}, "main_exclusive": ["01088"]},
    {"nom": "[sl] expert, TEMOIN : en standard le meme vilain garde ses 15 PV", "pourquoi": "le bonus ne vaut qu'en expert",
     "scenario": "shadows_in_the_night", "heros": "spider_man", "mise_en_place": [], "declencher": [], "verifier": "sl_etat", "attendu": {"vilain_pv_max": 15}, "main_exclusive": ["01088"]},
]


VERIFICATIONS = r'''
def sl_etat(monde, aides):
    """etat_attendu + `face_visible` : [[prefixe, card_id attendu]] = la face MONTREE de la carte (les deux faces d'une carte partagent un prefixe)."""
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
    if attendu.get("setup_dark_protege"):
        import re as _re
        from game.operate.worlds import Worlds as _W
        vilains = [f for f in _W.GetAllVillains(monde)]
        ids_vilains = sorted(str(v.paper.card_id) for v in vilains)
        if len(vilains) != 1 or not ids_vilains[0].endswith("a") or not ids_vilains[0].startswith("sl01"):
            soucis.append(f"vilains en jeu : {ids_vilains} (attendu UN vilain Dark Protege, face a)")
        else:
            nom = vilains[0].paper.name.lstrip("* ").strip()
            def lies(face):
                m = _re.search(r"Linked \(([^)]*)\)", face.paper.text or "")
                return [] if m is None else [m.group(1)]       # le segment brut : « nom in segment » (independant de l'analyse du script)
            deck = [f for f in monde.GetScenario().encounter_deck.Get(True) if str(f.paper.card_id) in [f"sl0{n}" for n in range(18, 28)]]
            cote = [f for f in monde.aside_deck.Get(True) if str(f.paper.card_id) in [f"sl0{n}" for n in range(18, 28)]]
            faux = [str(f.paper.card_id) for f in deck if not any(nom in s for s in lies(f))]
            manque = [str(f.paper.card_id) for f in cote if any(nom in s for s in lies(f))]
            reste_lies = [str(f.paper.card_id) for f in cote if not any(nom in s for s in lies(f))]
            if faux: soucis.append(f"dans le deck mais PAS lies a {nom} : {faux}")
            if manque: soucis.append(f"lies a {nom} mais restees de cote : {manque}")
            if not deck: soucis.append(f"aucune carte liee a {nom} dans le deck de rencontre")
    if any(k in attendu for k in ("vilain_face", "vilain_degats", "cartes_donnees", "partie_finie")):
        from game.operate.worlds import Worlds as _W2
        vilains = _W2.GetAllVillains(monde)
        if "vilain_face" in attendu:
            faces = [str(v.paper.card_id)[-1] for v in vilains]
            if faces != [attendu["vilain_face"]]:
                soucis.append(f"face du vilain {faces} (attendu {attendu['vilain_face']})")
        if "vilain_degats" in attendu:
            degats = [v.GetCounters("damage") if hasattr(v, "GetCounters") else None for v in vilains]
            if degats != [attendu["vilain_degats"]]:
                soucis.append(f"degats sur le vilain {degats} (attendu {attendu['vilain_degats']})")
        if "cartes_donnees" in attendu:
            donnees = [len(j.dealt_encounter_cards.Get(True)) for j in monde.players]
            if donnees != attendu["cartes_donnees"]:
                soucis.append(f"cartes de rencontre donnees face cachee {donnees} (attendu {attendu['cartes_donnees']})")
        if "partie_finie" in attendu and bool(monde.is_game_over) != attendu["partie_finie"]:
            soucis.append(f"partie finie = {bool(monde.is_game_over)} (attendu {attendu['partie_finie']})")
    reste = {k: v for k, v in attendu.items() if k not in ("face_visible", "setup_dark_protege", "vilain_face", "vilain_degats", "cartes_donnees", "partie_finie", "vilain_pv_max")}
    if "vilain_pv_max" in attendu:       # le vilain est tire au hasard : on lit SON identifiant en jeu
        from game.operate.worlds import Worlds as _W3
        reste["pv_max"] = [[str(v.paper.card_id), attendu["vilain_pv_max"]] for v in _W3.GetAllVillains(monde)]
    cas["attendu"] = reste
    try:
        ok, msg = etat_attendu(monde, aides)
    finally:
        cas["attendu"] = attendu
    if not ok:
        soucis.append(msg)
    return (False, " ; ".join(soucis)) if soucis else (True, "etat conforme")
'''
