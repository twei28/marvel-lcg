#!/usr/bin/env python3
"""Compare la LIVRAISON d'une autre IA a ce que le depot contient deja (20/10/2026). Bibliotheque standard seulement.

    python3 outils/comparer-livraison-au-depot.py <dossier livraison> <pack> <code> [--moteur <racine>] [--ecrire rapport.md]

CAS D'USAGE : on donne le kit a une IA et on lui fait REFAIRE une campagne que le jeu connait deja (Web of Deceit,
Mad Titan's Shadow...). Ce script dit, element par element, ce qu'elle a retrouve a l'identique, ce qui differe, ce qui
manque et ce qui est en trop. Il ne juge pas : une difference peut etre une ERREUR de l'IA ou une CORRECTION que le
depot attendait. C'est la liste que Claude relit, carte par carte, avec l'image et le livret.

Ce qui est compare (la forme exacte de la livraison : `verifier-livraison-campagne.py`, manuel §12) :
  cartes ........ champ par champ (type, name, subtitle, set_name, traits, desc, text, custom, liens) ; textes normalises
  scenarios ..... JSON normalise, cle par cle
  sets .......... JSON normalise (encounters : multiensemble)
  sets_info ..... l'entree du pack (le numero devant la cle est ignore)
  campagne ...... structure (cles, types, formats, detections, options, ids) SEPAREE de la prose (resume, enjeu, aide...)
  scripts ....... presence ; AST normalise (sans commentaires ni docstrings) ; fabriques appelees ; cles litterales
  campaign.py ... fonctions definies, cles litterales du carnet
  textes FR ..... entree par entree, textes normalises
"""
import argparse
import ast
import collections
import difflib
import io
import json
import os
import re
import sys

PROSE = {"resume", "resume_en", "enjeu", "aide", "libelle", "nom", "nom_en", "nom_fr", "titre", "titre_en", "texte",
         "aide_ajout", "libelle_ajout", "libelle_solde", "note"}


def lire(p):
    with io.open(p, encoding="utf-8", newline="") as f:
        return f.read()


def lire_json(p):
    return json.loads(lire(p))


def norm_txt(t):
    return re.sub(r"\s+", " ", (t or "").replace("\r\n", "\n")).strip()


class Rapport:
    def __init__(self):
        self.titres = []
        self.compte = collections.OrderedDict()
        self.details = []

    def section(self, titre):
        self.titres.append(titre)
        self.compte[titre] = collections.Counter()
        self.details.append(("## " + titre, []))
        self.courant = titre

    def ok(self):
        self.compte[self.courant]["identique"] += 1

    def diff(self, genre, ligne):
        self.compte[self.courant][genre] += 1
        self.details[-1][1].append("- **%s** : %s" % (genre, ligne))

    def texte(self):
        sortie = ["# Comparaison livraison ↔ dépôt", "", "| Élément | identique | différent | manquant (dans la livraison) | en trop (dans la livraison) |",
                  "|---|---|---|---|---|"]
        for t in self.titres:
            c = self.compte[t]
            sortie.append("| %s | %d | %d | %d | %d |" % (t, c["identique"], c["différent"], c["manquant"], c["en trop"]))
        sortie.append("")
        for titre, lignes in self.details:
            if lignes:
                sortie.append(titre)
                sortie.append("")
                sortie.extend(lignes)
                sortie.append("")
        return "\n".join(sortie)


def diff_dict(a, b, chemin=""):
    """Differences structurelles entre deux JSON : (chemin, valeur depot, valeur livraison)."""
    sortie = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a:
                sortie.append((chemin + "/" + k, "(absent)", json.dumps(b[k], ensure_ascii=False)[:100]))
            elif k not in b:
                sortie.append((chemin + "/" + k, json.dumps(a[k], ensure_ascii=False)[:100], "(absent)"))
            else:
                sortie += diff_dict(a[k], b[k], chemin + "/" + k)
    elif isinstance(a, list) and isinstance(b, list) and a and b and isinstance(a[0], dict) and isinstance(b[0], dict) \
            and ("id" in a[0] or "cle" in a[0]):
        cle = "id" if "id" in a[0] else "cle"
        da = {x.get(cle): x for x in a}
        db = {x.get(cle): x for x in b}
        for k in sorted(set(da) | set(db), key=str):
            if k not in da:
                sortie.append((chemin + "[" + str(k) + "]", "(absent)", "(present)"))
            elif k not in db:
                sortie.append((chemin + "[" + str(k) + "]", "(present)", "(absent)"))
            else:
                sortie += diff_dict(da[k], db[k], chemin + "[" + str(k) + "]")
        if [x.get(cle) for x in a] != [x.get(cle) for x in b] and set(da) == set(db):
            sortie.append((chemin, "ordre " + str([x.get(cle) for x in a])[:80], "ordre " + str([x.get(cle) for x in b])[:80]))
    elif a != b:
        va, vb = a, b
        if isinstance(a, str) and isinstance(b, str):
            if norm_txt(a) == norm_txt(b):
                return []
        sortie.append((chemin, json.dumps(va, ensure_ascii=False)[:100], json.dumps(vb, ensure_ascii=False)[:100]))
    return sortie


def est_prose(chemin):
    return chemin.rsplit("/", 1)[-1].split("[")[0] in PROSE


def ast_normalise(texte):
    arbre = ast.parse(texte)
    for n in ast.walk(arbre):
        if isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef, ast.Module)):
            corps = n.body
            if corps and isinstance(corps[0], ast.Expr) and isinstance(getattr(corps[0], "value", None), ast.Constant) \
                    and isinstance(corps[0].value.value, str):
                n.body = corps[1:] or [ast.Pass()]
    return ast.dump(arbre, annotate_fields=False, include_attributes=False)


def appels(texte):
    arbre = ast.parse(texte)
    noms = collections.Counter()
    for n in ast.walk(arbre):
        if isinstance(n, ast.Call):
            f = n.func
            nom = f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", None)
            if nom and nom[:1].isupper():
                noms[nom] += 1
    return noms


def litteraux(texte):
    arbre = ast.parse(texte)
    return {n.value for n in ast.walk(arbre) if isinstance(n, ast.Constant) and isinstance(n.value, str) and 3 < len(n.value) < 80}


def comparer(livraison, pack, code, moteur, r):
    integ = os.path.join(livraison, "integration")
    # --- cartes
    r.section("Cartes (faces)")
    depot = {c["card_id"]: c for c in lire_json(os.path.join(moteur, "data", "cards.json"))[pack] if "card_id" in c}
    frag = [f for f in os.listdir(os.path.join(integ, "data")) if f.startswith("cards.") and f.endswith(".fragment.json")]
    liv = {}
    for f in frag:
        for p, cartes in lire_json(os.path.join(integ, "data", f)).items():
            if p == pack:
                liv.update({c["card_id"]: c for c in cartes if "card_id" in c})
    for cid in sorted(set(depot) | set(liv)):
        if cid not in liv:
            r.diff("manquant", "`%s` %s" % (cid, depot[cid].get("name", "")))
        elif cid not in depot:
            r.diff("en trop", "`%s` %s" % (cid, liv[cid].get("name", "")))
        else:
            d = diff_dict(depot[cid], liv[cid])
            if d:
                r.diff("différent", "`%s` %s — %s" % (cid, depot[cid].get("name", ""),
                                                      " ; ".join("%s : dépôt %s ↔ livraison %s" % x for x in d[:6])))
            else:
                r.ok()
    # --- scenarios et sets
    for nom, sous in (("Scénarios", "scenarios"), ("Sets de rencontre", "encounter_sets")):
        r.section(nom)
        dossier_l = os.path.join(integ, "data", sous)
        livres = {f[:-5]: lire_json(os.path.join(dossier_l, f)) for f in os.listdir(dossier_l) if f.endswith(".json")} if os.path.isdir(dossier_l) else {}
        # ce que le depot associe a ce pack : scenarios du sets_info ; sets dont toutes les cartes sont du pack
        infos = lire_json(os.path.join(moteur, "data", "sets_info.json"))
        entree = next(v for k, v in infos.items() if isinstance(v, dict) and v.get("name") == pack)
        attendus = {}
        if sous == "scenarios":
            for s in entree.get("scenarios", []):
                for suff in ("", "_expert"):
                    p = os.path.join(moteur, "data", "scenarios", s + suff + ".json")
                    if os.path.exists(p):
                        attendus[s + suff] = lire_json(p)
        else:
            for f in os.listdir(os.path.join(moteur, "data", "encounter_sets")):
                if f.endswith(".json"):
                    d = lire_json(os.path.join(moteur, "data", "encounter_sets", f))
                    if d.get("encounters") and all(x in depot for x in d["encounters"]):
                        attendus[f[:-5]] = d
        for k in sorted(set(attendus) | set(livres)):
            if k not in livres:
                r.diff("manquant", "`%s`" % k)
            elif k not in attendus:
                r.diff("en trop", "`%s`" % k)
            else:
                a, b = attendus[k], livres[k]
                if sous == "encounter_sets" and isinstance(a.get("encounters"), list):
                    if collections.Counter(a["encounters"]) != collections.Counter(b.get("encounters", [])):
                        r.diff("différent", "`%s` : cartes dépôt %s ↔ livraison %s" % (k, sorted(collections.Counter(a["encounters"]).items())[:8], sorted(collections.Counter(b.get("encounters", [])).items())[:8]))
                        continue
                    a = {x: y for x, y in a.items() if x != "encounters"}
                    b = {x: y for x, y in b.items() if x != "encounters"}
                d = diff_dict(a, b)
                (r.diff("différent", "`%s` — %s" % (k, " ; ".join("%s : %s ↔ %s" % x for x in d[:6]))) if d else r.ok())
    # --- sets_info
    r.section("Entrée sets_info")
    fr = [f for f in os.listdir(os.path.join(integ, "data")) if f.startswith("sets_info.") and f.endswith(".fragment.json")]
    if not fr:
        r.diff("manquant", "fragment sets_info")
    else:
        livre = list(lire_json(os.path.join(integ, "data", fr[0])).values())[0]
        infos = lire_json(os.path.join(moteur, "data", "sets_info.json"))
        entree = next(v for k, v in infos.items() if isinstance(v, dict) and v.get("name") == pack)
        d = diff_dict(entree, livre)
        (r.diff("différent", " ; ".join("%s : %s ↔ %s" % x for x in d)) if d else r.ok())
    # --- campagne
    r.section("Description de campagne — STRUCTURE")
    p = os.path.join(integ, "data", "campagnes", code + ".json")
    prose = []
    if not os.path.exists(p):
        r.diff("manquant", "data/campagnes/%s.json" % code)
    else:
        a = lire_json(os.path.join(moteur, "data", "campagnes", code + ".json"))
        b = lire_json(p)
        for chemin, va, vb in diff_dict(a, b):
            if est_prose(chemin):
                prose.append((chemin, va, vb))
            else:
                r.diff("différent", "`%s` : dépôt %s ↔ livraison %s" % (chemin, va, vb))
        if not [1 for c in r.details[-1][1]]:
            r.ok()
    r.section("Description de campagne — PROSE (résumés, enjeux, aides : lecture humaine)")
    for chemin, va, vb in prose:
        r.diff("différent", "`%s` : dépôt %s ↔ livraison %s" % (chemin, va, vb))
    if not prose:
        r.ok()
    # --- scripts
    r.section("Scripts de cartes")
    base_d = os.path.join(moteur, "src", "cards", "pack", pack)
    base_l = os.path.join(integ, "src", "cards", "pack", pack)

    def lister(base):
        out = {}
        for d, ds, fs in os.walk(base):
            ds[:] = [x for x in ds if x != "__pycache__"]
            for f in fs:
                if f.endswith(".py"):
                    out[os.path.relpath(os.path.join(d, f), base).replace("\\", "/")] = os.path.join(d, f)
        return out
    sd, sl = lister(base_d), lister(base_l)
    for rel in sorted(set(sd) | set(sl)):
        if rel not in sl:
            r.diff("manquant", "`%s`" % rel)
        elif rel not in sd:
            r.diff("en trop", "`%s`" % rel)
        else:
            ta, tb = lire(sd[rel]), lire(sl[rel])
            try:
                if ast_normalise(ta) == ast_normalise(tb):
                    r.ok()
                    continue
                ca, cb = appels(ta), appels(tb)
                manque = sorted((ca - cb).elements())
                trop = sorted((cb - ca).elements())
                la, lb = litteraux(ta), litteraux(tb)
                r.diff("différent", "`%s` — appels absents de la livraison : %s ; en plus : %s ; chaînes absentes : %s"
                       % (rel, manque[:8] or "aucun", trop[:8] or "aucun", sorted(la - lb)[:5] or "aucune"))
            except SyntaxError as e:
                r.diff("différent", "`%s` — erreur de syntaxe dans la livraison : %s" % (rel, e))
    # --- campaign.py
    r.section("campaign.py : fonctions et clés de carnet")
    if "campaign.py" in sd:
        if "campaign.py" not in sl:
            r.diff("manquant", "campaign.py")
        else:
            fa = {n.name for n in ast.parse(lire(sd["campaign.py"])).body if isinstance(n, ast.FunctionDef)}
            fb = {n.name for n in ast.parse(lire(sl["campaign.py"])).body if isinstance(n, ast.FunctionDef)}
            ka, kb = litteraux(lire(sd["campaign.py"])), litteraux(lire(sl["campaign.py"]))
            if fa == fb and ka == kb:
                r.ok()
            else:
                r.diff("différent", "fonctions absentes : %s ; en plus : %s ; chaînes (clés) absentes : %s ; en plus : %s"
                       % (sorted(fa - fb) or "aucune", sorted(fb - fa) or "aucune", sorted(ka - kb)[:8] or "aucune", sorted(kb - ka)[:8] or "aucune"))
    # --- textes francais
    r.section("Textes français")
    ts = lire(os.path.join(os.path.dirname(moteur), "..", "ui-app", "src", "board", "textes-fr-fanmade.ts")) \
        if os.path.exists(os.path.join(os.path.dirname(moteur), "..", "ui-app", "src", "board", "textes-fr-fanmade.ts")) else ""
    depot_fr = dict(re.findall(r"""^  '([^']+)':\s*"(.*)",\s*$""", ts, re.M))
    depot_fr = {k: v for k, v in depot_fr.items() if k in depot}
    liv_fr = {}
    d_fr = os.path.join(integ, "textes-fr")
    if os.path.isdir(d_fr):
        for f in os.listdir(d_fr):
            liv_fr.update(dict(re.findall(r"""^  '([^']+)':\s*"(.*)",\s*$""", lire(os.path.join(d_fr, f)), re.M)))
    for cid in sorted(set(depot_fr) | set(liv_fr)):
        if cid not in liv_fr:
            r.diff("manquant", "`%s`" % cid)
        elif cid not in depot_fr:
            r.diff("en trop", "`%s`" % cid)
        elif norm_txt(depot_fr[cid]) == norm_txt(liv_fr[cid]):
            r.ok()
        else:
            r.diff("différent", "`%s` : dépôt « %s » ↔ livraison « %s »" % (cid, depot_fr[cid][:90], liv_fr[cid][:90]))
    if not depot_fr and not liv_fr:
        r.diff("différent", "aucun texte français ni dans le dépôt ni dans la livraison")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("livraison")
    ap.add_argument("pack")
    ap.add_argument("code")
    ap.add_argument("--moteur", default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Fusion", "marvel-lcg-src"))
    ap.add_argument("--ecrire")
    a = ap.parse_args()
    r = Rapport()
    comparer(os.path.abspath(a.livraison), a.pack, a.code, os.path.abspath(a.moteur), r)
    texte = r.texte()
    if a.ecrire:
        with io.open(a.ecrire, "w", encoding="utf-8", newline="") as f:
            f.write(texte)
        print("rapport ecrit : %s" % a.ecrire)
        print("\n".join(texte.split("\n")[:18]))
    else:
        print(texte)
    return 0


if __name__ == "__main__":
    sys.exit(main())
