# Cas test_capacites : l'EXPORT de l'etat de la ville vers l'interface (`ToDescriptor.Ville`, champ `ville` du WorldDescriptor), pour l'onglet
# « Ville » (decisions de l'utilisateur du 22/10/2026 : .planning/mcdc-punisher/decisions-interface-ville.md). Prefixe `[vexp]`.
import importlib.util, os
_s = importlib.util.spec_from_file_location("ba", os.path.join(os.path.dirname(__file__), "big_apple.py"))
_ba = importlib.util.module_from_spec(_s); _s.loader.exec_module(_ba)


def _v(nom, pourquoi, declencher, attendu, **cle):
    cas = {"nom": "[vexp] " + nom, "pourquoi": pourquoi, "scenario": "rhino", "heros": "spider_man",
           "mise_en_place": [*_ba.RIEN, _ba.FORME_HEROS], "declencher": declencher, "verifier": "ville_export", "attendu": attendu,
           "main_exclusive": cle.pop("main_exclusive", ["01088"])}
    cas.update(cle)
    return cas


CAS = [
    _v("hors de la ville : le champ `ville` est VIDE (aucune partie ordinaire n'est touchee)", "dictionnaire vide sans `Ville.Installer`",
       [], {"vide": True}),
    _v("la ville installee : 9 cases, 3 rangees, un joueur a Midtown (1, 1)", "grille 3x3 et depart R1",
       _ba.ville(), {"cases": 9, "lignes": 3, "joueurs": [[0, 1, 1]], "case_joueurs": [[1, 1, [0]]]}),
    _v("apres un deplacement a Theater District : le pion est en (0, 1)", "la position exportee suit `Ville.Deplacer`",
       [*_ba.ville(), "Puzzle.DeplacerDansLaVille((0, 1))"], {"joueurs": [[0, 0, 1]], "case_joueurs": [[0, 1, [0]], [1, 1, []]]}),
    _v("un sbire attache a Theater District : la case l'exporte", "pastille de sbire attache (decision 6)",
       [*_ba.ville(), "Puzzle.PutIntoPlay('pu013')", "Puzzle.AttacherAuLieu('pu013', 'pu031')"], {"attaches": [[0, 1, 1]]}),
    _v("la capacite « une fois par round » deja utilisee est marquee, les autres non", "indicateur de limite utilisee (decision 6)",
       [*_ba.ville(), "Puzzle.DeplacerDansLaVille((0, 1))", "Puzzle.Damage('01001a', 4)", "Puzzle.Action('pu031', 'Action')"],
       {"limite": [[0, 1, True], [1, 1, False]]}, cibles=["01001a"]),
    {"nom": "[vexp] scenario REEL the_big_apple : un CAPO par rangee et la piste revelee au joueur, avec ses compteurs", "pourquoi": "mise en place reelle -> capos (zones) et pistes (aires des joueurs)",
     "scenario": "the_big_apple", "heros": "spider_man", "mise_en_place": [], "declencher": [], "verifier": "ville_export",
     "attendu": {"cases": 9, "lignes": 3, "capos": 3, "pistes": 1}, "main_exclusive": ["01088"]},
]

VERIFICATIONS = r'''
def ville_export(monde, aides):
    from game.render.to_descriptor import ToDescriptor
    attendu = aides["cas"].get("attendu") or {}
    d = ToDescriptor.Ville(monde)
    soucis = []
    if attendu.get("vide"):
        return (not d, "vide" if not d else f"attendu vide, recu {list(d)}")
    if "cases" in attendu and len(d.get("cases", [])) != attendu["cases"]:
        soucis.append(f"{len(d.get('cases', []))} cases (attendu {attendu['cases']})")
    if "lignes" in attendu and len(d.get("lignes", [])) != attendu["lignes"]:
        soucis.append(f"{len(d.get('lignes', []))} lignes (attendu {attendu['lignes']})")
    for pid, l, c in attendu.get("joueurs") or []:
        if {"player_id": pid, "ligne": l, "colonne": c} not in d.get("joueurs", []):
            soucis.append(f"joueur {pid} pas en ({l}, {c}) : {d.get('joueurs')}")
    par_case = {(x["ligne"], x["colonne"]): x for x in d.get("cases", [])}
    for l, c, pids in attendu.get("case_joueurs") or []:
        if par_case.get((l, c), {}).get("joueurs") != pids:
            soucis.append(f"case ({l}, {c}) joueurs {par_case.get((l, c), {}).get('joueurs')} (attendu {pids})")
    for l, c, n in attendu.get("attaches") or []:
        if len(par_case.get((l, c), {}).get("sbires_attaches", [])) != n:
            soucis.append(f"case ({l}, {c}) sbires attaches {par_case.get((l, c), {}).get('sbires_attaches')} (attendu {n})")
    for l, c, u in attendu.get("limite") or []:
        if par_case.get((l, c), {}).get("limite_utilisee") != u:
            soucis.append(f"case ({l}, {c}) limite_utilisee {par_case.get((l, c), {}).get('limite_utilisee')} (attendu {u})")
    if "capos" in attendu and sum(1 for x in d.get("lignes", []) if x.get("capo") is not None) != attendu["capos"]:
        soucis.append(f"capos par rangee : {[x.get('capo_card_id') for x in d.get('lignes', [])]} (attendu {attendu['capos']})")
    if "pistes" in attendu and sum(1 for x in d.get("cases", []) if x.get("piste")) != attendu["pistes"]:
        soucis.append(f"pistes : {[x.get('piste') for x in d.get('cases', []) if x.get('piste')]} (attendu {attendu['pistes']})")
    import json
    json.dumps(d)   # serialisable tel quel pour le client
    return (False, " ; ".join(soucis)) if soucis else (True, "ville exportee conforme")
'''
