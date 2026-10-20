#!/usr/bin/env python3
"""Compare la LIVRAISON d'un HEROS a ce que le depot contient deja (20/10/2026). Bibliotheque standard seulement.

    python3 outils/comparer-livraison-heros-au-depot.py <dossier livraison> <pack> <deck> [--moteur <racine>] [--ecrire rapport.md]

CAS D'USAGE : on donne le kit a une IA et on lui fait REFAIRE un heros que le jeu connait deja (Lockjaw, Iron Fist...).
Ce script dit, element par element, ce qu'elle a retrouve a l'identique, ce qui differe, ce qui manque et ce qui est
en trop. Il ne juge pas : une difference peut etre une ERREUR de l'IA ou une CORRECTION que le depot attendait. C'est
la liste que Claude relit, carte par carte, avec l'image.

Ce qui est compare (la forme exacte de la livraison : `verifier-livraison-heros.py`, manuel chapitre 9) :
  cartes ........ champ par champ (type, name, subtitle, set_name, traits, desc, text, custom, liens)
  sets_info ..... l'entree du pack (le numero devant la cle est ignore)
  decks ......... deck de depart et variantes (hero, hero_deck, obligations, nemesis_set, player_deck, metadata) ;
                  les listes de cartes sont comparees comme des MULTIENSEMBLES
  nemesis ....... data/nemesis/<deck>_nemesis.json
  scripts ....... presence ; AST normalise (sans commentaires ni docstrings) ; fabriques appelees ; chaines litterales
  textes FR ..... entree par entree, textes normalises
  biographie .... l'entree de heros-info.js, cle par cle
  repliques ..... la ligne de repliques-heros.js
"""
import argparse
import collections
import glob
import importlib.util
import io
import json
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)


def charger(nom, fichier):
    spec = importlib.util.spec_from_file_location(nom, os.path.join(ICI, fichier))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


C = charger("comparer_livraison_au_depot", "comparer-livraison-au-depot.py")
lire, lire_json, norm_txt, diff_dict = C.lire, C.lire_json, C.norm_txt, C.diff_dict


def bloc_bio(texte, cid):
    m = re.search(r'^    "%s": \{\n(.*?)^    \},?\n' % re.escape(cid), texte, re.M | re.S)
    return m.group(1) if m else None


def champs_bio(corps):
    """{cle: texte} d'un bloc d'entree de heros-info.js."""
    return {k: v for k, v in re.findall(r'^\s{8}([A-Za-z]+):\s*"((?:[^"\\]|\\.)*)",?\s*$', corps, re.M)}


def listes(a, b):
    """Differences de deux listes de card_id vues comme multiensembles."""
    ca, cb = collections.Counter(a), collections.Counter(b)
    manque = sorted((ca - cb).elements())
    trop = sorted((cb - ca).elements())
    return manque, trop


def comparer(livraison, pack, deck, moteur, r):
    integ = os.path.join(livraison, "integration")
    # --- cartes
    r.section("Cartes (faces)")
    depot = {c["card_id"]: c for c in lire_json(os.path.join(moteur, "data", "cards.json"))[pack] if "card_id" in c}
    liv = {}
    dossier = os.path.join(integ, "data")
    for f in sorted(os.listdir(dossier)) if os.path.isdir(dossier) else []:
        if f.startswith("cards.") and f.endswith(".fragment.json"):
            for p, cartes in lire_json(os.path.join(dossier, f)).items():
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
    # --- sets_info
    r.section("Entrée sets_info")
    fr = [f for f in os.listdir(dossier) if f.startswith("sets_info.") and f.endswith(".fragment.json")] if os.path.isdir(dossier) else []
    if not fr:
        r.diff("manquant", "fragment sets_info")
    else:
        livre = list(lire_json(os.path.join(dossier, fr[0])).values())[0]
        infos = lire_json(os.path.join(moteur, "data", "sets_info.json"))
        entree = next(v for k, v in infos.items() if isinstance(v, dict) and v.get("name") == pack)
        d = diff_dict(entree, livre)
        (r.diff("différent", " ; ".join("%s : %s ↔ %s" % x for x in d)) if d else r.ok())
    # --- decks
    r.section("Decks de départ (base et variantes)")
    attendus = {}
    for f in sorted(glob.glob(os.path.join(moteur, "deck", "starter", "*.json"))):
        nom = os.path.basename(f)[:-5]
        d = lire_json(f)
        if nom == deck or (d.get("metadata") or {}).get("variante_de") == deck:
            attendus[nom] = d
    livres = {}
    dd = os.path.join(integ, "deck", "starter")
    if os.path.isdir(dd):
        for f in sorted(os.listdir(dd)):
            if f.endswith(".json"):
                livres[f[:-5]] = lire_json(os.path.join(dd, f))
    for nom in sorted(set(attendus) | set(livres)):
        if nom not in livres:
            r.diff("manquant", "deck `%s`" % nom)
            continue
        if nom not in attendus:
            r.diff("en trop", "deck `%s`" % nom)
            continue
        a, b = attendus[nom], livres[nom]
        soucis = []
        for k in ("version", "name", "hero", "set_aside"):
            if a.get(k) != b.get(k):
                soucis.append("%s : dépôt %s ↔ livraison %s" % (k, json.dumps(a.get(k), ensure_ascii=False)[:60], json.dumps(b.get(k), ensure_ascii=False)[:60]))
        for k in ("hero_deck", "obligations", "nemesis_set", "player_deck"):
            manque, trop = listes(a.get(k, []), b.get(k, []))
            if manque or trop:
                soucis.append("%s : cartes absentes de la livraison %s ; en plus %s" % (k, manque[:8] or "aucune", trop[:8] or "aucune"))
        if "linked_identity" in a or "linked_identity" in b:
            if a.get("linked_identity") != b.get("linked_identity"):
                soucis.append("linked_identity différente")
        for chemin, va, vb in diff_dict(a.get("metadata", {}), b.get("metadata", {}), "metadata"):
            soucis.append("%s : dépôt %s ↔ livraison %s" % (chemin, va, vb))
        (r.diff("différent", "deck `%s` — %s" % (nom, " ; ".join(soucis))) if soucis else r.ok())
    # --- nemesis
    r.section("Set némésis nommé (data/nemesis)")
    pa = os.path.join(moteur, "data", "nemesis", deck + "_nemesis.json")
    pl = os.path.join(integ, "data", "nemesis", deck + "_nemesis.json")
    if os.path.exists(pa) and not os.path.exists(pl):
        r.diff("manquant", "`%s_nemesis.json` (facultatif)" % deck)
    elif os.path.exists(pl) and not os.path.exists(pa):
        r.diff("en trop", "`%s_nemesis.json`" % deck)
    elif os.path.exists(pa):
        d = diff_dict(lire_json(pa), lire_json(pl))
        (r.diff("différent", " ; ".join("%s : %s ↔ %s" % x for x in d)) if d else r.ok())
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
                if C.ast_normalise(ta) == C.ast_normalise(tb):
                    r.ok()
                    continue
                ca, cb = C.appels(ta), C.appels(tb)
                manque = sorted((ca - cb).elements())
                trop = sorted((cb - ca).elements())
                la, lb = C.litteraux(ta), C.litteraux(tb)
                r.diff("différent", "`%s` — appels absents de la livraison : %s ; en plus : %s ; chaînes absentes : %s"
                       % (rel, manque[:8] or "aucun", trop[:8] or "aucun", sorted(la - lb)[:5] or "aucune"))
            except SyntaxError as e:
                r.diff("différent", "`%s` — erreur de syntaxe dans la livraison : %s" % (rel, e))
    # --- textes francais
    r.section("Textes français")
    chemin_ts = os.path.join(RACINE, "ui-app", "src", "board", "textes-fr-fanmade.ts")
    ts = lire(chemin_ts) if os.path.exists(chemin_ts) else ""
    depot_fr = {k: v for k, v in re.findall(r"""^  '([^']+)':\s*"(.*)",\s*$""", ts, re.M) if k in depot}
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
    # --- biographie
    r.section("Biographie (heros-info.js)")
    face = (attendus.get(deck) or {}).get("hero", [""])[0].split(",")[0]
    texte_d = lire(os.path.join(moteur, "public", "js", "prepare", "heros-info.js"))
    bd = bloc_bio(texte_d, face) if face else None
    pb = os.path.join(integ, "public", "js", "prepare", "heros-info.fragment.js")
    bl = bloc_bio(lire(pb), face) if os.path.exists(pb) and face else None
    if bd is None and bl is None:
        r.diff("différent", "aucune biographie ni dans le dépôt ni dans la livraison pour %s" % face)
    elif bl is None:
        r.diff("manquant", "biographie de `%s`" % face)
    elif bd is None:
        r.diff("en trop", "biographie de `%s` (le dépôt n'en a pas)" % face)
    else:
        a, b = champs_bio(bd), champs_bio(bl)
        d = [(k, a.get(k, "(absent)")[:70], b.get(k, "(absent)")[:70]) for k in sorted(set(a) | set(b))
             if norm_txt(a.get(k, "")) != norm_txt(b.get(k, ""))]
        (r.diff("différent", "`%s` — %s" % (face, " ; ".join("%s : dépôt « %s » ↔ livraison « %s »" % x for x in d))) if d else r.ok())
    # --- repliques
    r.section("Réplique de recrutement (repliques-heros.js)")
    ligne_d = re.search(r"^    %s: \[(.*)\],?$" % re.escape(deck), lire(os.path.join(moteur, "public", "js", "prepare", "repliques-heros.js")), re.M)
    pr = os.path.join(integ, "public", "js", "prepare", "repliques-heros.fragment.js")
    ligne_l = re.search(r"^    %s: \[(.*)\],?$" % re.escape(deck), lire(pr), re.M) if os.path.exists(pr) else None
    if ligne_d and not ligne_l:
        r.diff("manquant", "répliques de `%s` (facultatif)" % deck)
    elif ligne_l and not ligne_d:
        r.diff("en trop", "répliques de `%s` (le dépôt n'en a pas)" % deck)
    elif ligne_d:
        (r.ok() if norm_txt(ligne_d.group(1)) == norm_txt(ligne_l.group(1))
         else r.diff("différent", "dépôt %s ↔ livraison %s" % (ligne_d.group(1)[:90], ligne_l.group(1)[:90])))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("livraison")
    ap.add_argument("pack")
    ap.add_argument("deck")
    ap.add_argument("--moteur", default=os.path.join(RACINE, "Fusion", "marvel-lcg-src"))
    ap.add_argument("--ecrire")
    a = ap.parse_args()
    r = C.Rapport()
    comparer(os.path.abspath(a.livraison), a.pack, a.deck, os.path.abspath(a.moteur), r)
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
