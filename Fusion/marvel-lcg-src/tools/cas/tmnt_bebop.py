# Cas test_capacites du scenario BEBOP & ROCKSTEADY (TMNT Villains v3, Inkwire, prefixe `tk`).
SC = "bebop_rocksteady"
CAS = [
    {"nom": "[bebop] tk005a fumee : la partie monte, deux vilains en jeu",
     "pourquoi": "smoke", "scenario": SC, "heros": "spider_man",
     "mise_en_place": [], "declencher": [], "verifier": "bb_etat",
     "attendu": {"en_jeu": ["tk001a", "tk003a", "tk006a", "tk007a", "tk008a", "tk101"], "attache": [["tk007a", "tk001a"], ["tk008a", "tk003a"]]}},
]

# Verification outillee du pack : etat_attendu (cles de base) + extensions lues sur les faces EN JEU.
VERIFICATIONS = r'''
def bb_etat(monde, aides):
    """Extensions de `etat_attendu` : attache [[carte, hote]], compteurs_sur [[id, nom, n]],
    menace [[id, n]], attaque [[id, n]], statuts_sur [[id, 'stunned'|'tough'|'confused', n]],
    vie [[id, pv_max]], absents [ids hors jeu], traits [[id, TRAIT, bool]], bascule : etat_attendu d'abord."""
    attendu = aides["cas"].get("attendu") or {}
    ok, msg = etat_attendu(monde, aides)
    soucis = [] if ok else [msg]
    par_id = aides["par_id"]
    for cid, hote in attendu.get("attache", []):
        f = par_id(monde, cid)
        if f is None:
            soucis.append(f"{cid} n'est pas en jeu"); continue
        b = f.bind_face
        got = getattr(getattr(b, "paper", None), "card_id", None) if b else None
        if got != hote:
            soucis.append(f"{cid} attache a {got} (attendu {hote})")
    for cid, nom, n in attendu.get("compteurs_sur", []):
        f = par_id(monde, cid)
        if f is None:
            soucis.append(f"{cid} n'est pas en jeu"); continue
        if f.GetCounters(nom) != n:
            soucis.append(f"{cid} compteurs {nom} = {f.GetCounters(nom)} (attendu {n})")
    for cid, n in attendu.get("menace", []):
        f = par_id(monde, cid)
        if f is None:
            soucis.append(f"{cid} n'est pas en jeu"); continue
        if f.threat != n:
            soucis.append(f"{cid} menace = {f.threat} (attendu {n})")
    for cid, n in attendu.get("attaque", []):
        f = par_id(monde, cid)
        if f is None:
            soucis.append(f"{cid} n'est pas en jeu"); continue
        if f.attack != n:
            soucis.append(f"{cid} ATK = {f.attack} (attendu {n})")
    for cid, n in attendu.get("vie", []):
        f = par_id(monde, cid)
        if f is None:
            soucis.append(f"{cid} n'est pas en jeu"); continue
        if f.max_health != n:
            soucis.append(f"{cid} PV max = {f.max_health} (attendu {n})")
    for cid, st, n in attendu.get("statuts_sur", []):
        f = par_id(monde, cid)
        if f is None:
            soucis.append(f"{cid} n'est pas en jeu"); continue
        v = getattr(f, st)
        if v != n:
            soucis.append(f"{cid} statut {st} = {v} (attendu {n})")
    for cid in attendu.get("absents", []):
        if par_id(monde, cid) is not None:
            soucis.append(f"{cid} est encore en jeu")
    for cid, tr, b in attendu.get("traits", []):
        f = par_id(monde, cid)
        if f is None:
            soucis.append(f"{cid} n'est pas en jeu"); continue
        if bool(f.HasTrait(tr)) != b:
            soucis.append(f"{cid} trait {tr} = {f.HasTrait(tr)} (attendu {b})")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "etat conforme"
'''
