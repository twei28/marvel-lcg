#!/usr/bin/env python3
"""Reconstitue, A PARTIR DU DEPOT, la « livraison » d'une campagne deja integree (20/10/2026).

    python3 outils/livraison-depuis-le-depot.py <pack> <code> <dossier sortie> [--officiel]

POURQUOI
--------
Le kit de creation de campagne dit a une autre IA comment LIVRER ses fichiers (`livraison/`, voir §12 du manuel).
Pour que l'exemple soit exact et que le verificateur (`verifier-livraison-campagne.py`) soit CALIBRE sur du vrai
contenu, on refait, pour une campagne qui marche en jeu, le dossier qu'une IA aurait du livrer : fragments de
`cards.json` et `sets_info.json`, scenarios, sets, description de campagne, scripts, textes francais, epreuves,
et les fichiers de suivi (MANIFESTE, CARNET-CLES, images, livret-pages...).

Les fichiers de suivi sont GENERES (liste, table des cles par lecture du `campaign.py`) : ils montrent le FORMAT
attendu, ils ne sont pas la preuve qu'un humain les a relus.
"""
import argparse
import ast
import io
import json
import os
import re
import shutil
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOTEUR = os.path.join(RACINE, "Fusion", "marvel-lcg-src")

EN_TETES_EPREUVES = {
    # code de campagne -> (debut, fin) : reperes de texte dans tools/epreuves_campagnes.py
    "mts": ("L'Ombre du Titan Fou (mts)", "Les plus recherches de la galaxie (gmw)"),
    "web_of_deceit": ("La Toile du Mensonge (web_of_deceit)", "Hunting Season (hunting_season)"),
    "hunting_season": ("Hunting Season (hunting_season)", None),
    "trors": ("L'Avenement de Crane Rouge (trors)", "L'Ombre du Titan Fou (mts)"),
    "gmw": ("Les plus recherches de la galaxie (gmw)", "Sinistres Motivations (sm)"),
    "fne": ("Fear No Evil (fne)", "L'Avenement de Crane Rouge (trors)"),
}


def lire(chemin):
    with io.open(chemin, encoding="utf-8", newline="") as f:
        return f.read()


def ecrire(chemin, contenu):
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with io.open(chemin, "w", encoding="utf-8", newline="") as f:
        f.write(contenu)


def ecrire_json(chemin, valeur):
    ecrire(chemin, json.dumps(valeur, ensure_ascii=False, indent=4) + "\n")


def clean_name(nom):
    return (nom.lstrip("*").strip().lower().replace(" - ", "_").replace(" & ", "_").replace(" ", "_")
            .replace("'", "").replace("-", "_").replace("!", "").replace("?", "").replace("(", "").replace(")", "")
            .replace(".", "").replace(",", "").replace('"', "").replace("&", "_").replace("#", "").replace("/", ""))


def extraire_epreuves(code):
    if code not in EN_TETES_EPREUVES:
        return None
    debut, fin = EN_TETES_EPREUVES[code]
    lignes = lire(os.path.join(MOTEUR, "tools", "epreuves_campagnes.py")).split("\n")
    i0 = next((i for i, l in enumerate(lignes) if l.startswith("# ====") and debut in l), None)
    if i0 is None:
        return None
    i1 = len(lignes)
    if fin:
        i1 = next((i for i in range(i0 + 1, len(lignes)) if lignes[i].startswith("# ====") and fin in lignes[i]), len(lignes))
    return "\n".join(lignes[i0:i1]).rstrip() + "\n"


def extraire_textes_fr(ids):
    lignes = lire(os.path.join(RACINE, "ui-app", "src", "board", "textes-fr-fanmade.ts")).split("\n")
    sortie = []
    for i, l in enumerate(lignes):
        m = re.match(r"^  '([^']+)':", l)
        if m and m.group(1) in ids:
            if i and lignes[i - 1].lstrip().startswith("//"):
                sortie.append(lignes[i - 1])
            sortie.append(l)
    return "\n".join(sortie) + "\n" if sortie else None


def extraire_bios(ids):
    texte = lire(os.path.join(MOTEUR, "public", "js", "prepare", "mechants-info.js"))
    blocs = []
    for cid in ids:
        m = re.search(r'^    "%s": \{\n.*?^    \},?\n' % re.escape(cid), texte, re.M | re.S)
        if m:
            blocs.append(m.group(0))
    return "\n".join(blocs) if blocs else None


def extraire_pages_livret(code):
    texte = lire(os.path.join(MOTEUR, "tools", "pages_livret.py"))
    m = re.search(r'^    "%s": \{\n.*?^    \},\n' % re.escape(code), texte, re.M | re.S)
    return m.group(0) if m else None


def lire_ts_ids(texte):
    return set(re.findall(r"^  '([^']+)':", texte, re.M))


def table_cles(campagne, campaign_py):
    """Table des cles du carnet (CARNET-CLES.md) : declaration (JSON) et ecriture/lecture (campaign.py, par AST)."""
    ecrites, lues = {}, {}
    if campaign_py and os.path.exists(campaign_py):
        arbre = ast.parse(lire(campaign_py))
        for fonction in [n for n in ast.walk(arbre) if isinstance(n, ast.FunctionDef)]:
            for n in ast.walk(fonction):
                if isinstance(n, ast.Subscript) and isinstance(n.slice, ast.Constant) and isinstance(n.slice.value, str):
                    # updates['cle'] = ... (ecriture) ou x['cle'] (lecture)
                    cible = isinstance(getattr(n, "ctx", None), ast.Store)
                    (ecrites if cible else lues).setdefault(n.slice.value, set()).add(fonction.name)
                elif isinstance(n, ast.Call):
                    for a in n.args:
                        if isinstance(a, ast.Constant) and isinstance(a.value, str) and len(a.value) > 2:
                            nom_appel = n.func.attr if isinstance(n.func, ast.Attribute) else getattr(n.func, "id", "")
                            if nom_appel in ("InPool", "LogSet") or nom_appel.startswith("Get"):
                                cle = "Campaign Pool: " + a.value if nom_appel == "InPool" else a.value
                                lues.setdefault(cle, set()).add(fonction.name)
                            elif nom_appel in ("SetStr",):
                                ecrites.setdefault(a.value, set()).add(fonction.name)
                elif isinstance(n, ast.Constant) and isinstance(n.value, str) and len(n.value) > 3 \
                        and n.value[:1].isupper() and n.value not in ecrites and n.value not in lues:
                    lues.setdefault(n.value, set()).add(fonction.name)
    lignes = ["# Table des cles du carnet (generee a partir du depot : forme attendue, pas relecture humaine)", "",
              "| Cle | Format | Par joueur ? | Ecrite par (campaign.py) | Lue par (campaign.py) | Declaree dans la description |",
              "|---|---|---|---|---|---|"]
    vues = set()

    def champs():
        for s in campagne.get("scenarios", []):
            for c in s.get("victoire", []) or []:
                yield "scenario " + s["id"], c
        for k in ("victoire_commune", "victoire_commune_expert"):
            for c in campagne.get(k, []) or []:
                yield k, c

    for ou, c in champs():
        cle = c["cle"]
        if cle in vues:
            continue
        vues.add(cle)
        e = ", ".join(sorted(ecrites.get(cle, []))) or "(moteur : collecteur commun ou choix du joueur)"
        l = ", ".join(sorted(lues.get(cle, []))) or "(non trouvee par lecture simple : cle composee ou lue ailleurs)"
        decl = "%s, `%s`%s" % (ou, c.get("type"), (", detection `%s`" % c["detection"]) if c.get("detection") else "")
        lignes.append("| `%s` | %s | %s | %s | %s | %s |" % (cle, c.get("format", "texte"), "oui" if c.get("parJoueur") else "non", e, l, decl))
    return "\n".join(lignes) + "\n"


def construire(pack, code, sortie, officiel):
    if os.path.exists(sortie):
        shutil.rmtree(sortie)
    integ = os.path.join(sortie, "integration")
    donnees = json.loads(lire(os.path.join(MOTEUR, "data", "cards.json")))
    cartes = donnees[pack]
    ids = {c["card_id"] for c in cartes if "card_id" in c}
    ecrire_json(os.path.join(integ, "data", "cards.%s.fragment.json" % pack), {pack: cartes})
    infos = json.loads(lire(os.path.join(MOTEUR, "data", "sets_info.json")))
    cle_info = next(k for k, v in infos.items() if isinstance(v, dict) and v.get("name") == pack)
    entree = infos[cle_info]
    cle_neutre = re.sub(r"^\d+\.", "N.", cle_info) if not officiel else cle_info
    ecrire_json(os.path.join(integ, "data", "sets_info.%s.fragment.json" % pack), {cle_neutre: entree})
    camp = json.loads(lire(os.path.join(MOTEUR, "data", "campagnes", "%s.json" % code)))
    if not officiel:
        camp["cle_extension"] = camp.get("cle_extension")
    ecrire_json(os.path.join(integ, "data", "campagnes", "%s.json" % code), camp)
    sets_utiles = set()
    for s in entree.get("scenarios", []):
        for suffixe in ("", "_expert"):
            chemin = os.path.join(MOTEUR, "data", "scenarios", s + suffixe + ".json")
            if os.path.exists(chemin):
                d = json.loads(lire(chemin))
                ecrire_json(os.path.join(integ, "data", "scenarios", s + suffixe + ".json"), d)
                sets_utiles |= set(d.get("encounter_sets", [])) | set(d.get("modular_sets", []))
    # tous les sets de rencontre dont TOUTES les cartes sont du pack (propres au scenario ou modulaires)
    for f in sorted(os.listdir(os.path.join(MOTEUR, "data", "encounter_sets"))):
        if not f.endswith(".json"):
            continue
        d = json.loads(lire(os.path.join(MOTEUR, "data", "encounter_sets", f)))
        if d.get("encounters") and all(x in ids for x in d["encounters"]):
            ecrire_json(os.path.join(integ, "data", "encounter_sets", f), d)
    # scripts
    src = os.path.join(MOTEUR, "src", "cards", "pack", pack)
    for d, ds, fs in os.walk(src):
        ds[:] = [x for x in ds if x != "__pycache__"]
        for f in fs:
            if f.endswith(".py"):
                rel = os.path.relpath(os.path.join(d, f), src)
                ecrire(os.path.join(integ, "src", "cards", "pack", pack, rel), lire(os.path.join(d, f)))
    # textes francais
    if not officiel:
        fr = extraire_textes_fr(ids)
        if fr:
            ecrire(os.path.join(integ, "textes-fr", "%s.fragment.txt" % pack), fr)
        prefixes = json.loads(lire(os.path.join(MOTEUR, "tools", "prefixes_fanmade.json")))["prefixes"]
        for p, v in prefixes.items():
            if v.get("pack") == pack:
                ecrire_json(os.path.join(integ, "tools", "prefixes.%s.fragment.json" % pack), {p: v})
    premiers = []
    for s in entree.get("scenarios", []):
        chemin = os.path.join(MOTEUR, "data", "scenarios", s + ".json")
        if os.path.exists(chemin):
            v = json.loads(lire(chemin)).get("villain") or []
            if v:
                premiers.append(str(v[0]).split(",")[0])
    bios = extraire_bios(premiers) if not officiel else None
    if bios:
        ecrire(os.path.join(integ, "public", "js", "prepare", "mechants-info.fragment.js"), bios)
    ep = extraire_epreuves(code)
    if ep:
        ecrire(os.path.join(integ, "tools", "epreuves.%s.fragment.py" % code), ep)
    # fichiers de suivi
    fichiers = []
    for d, ds, fs in os.walk(integ):
        for f in sorted(fs):
            fichiers.append(os.path.relpath(os.path.join(d, f), integ).replace("\\", "/"))
    fichiers.sort()
    manifeste = ["# MANIFESTE (genere depuis le depot : forme attendue)", "",
                 "| Chemin (dans integration/) | Role |", "|---|---|"]
    for f in fichiers:
        manifeste.append("| %s | %s |" % (f, role(f)))
    manifeste += ["", "Cartes (faces) : %d. Scenarios : %d. Scripts : %d." % (
        len(cartes), len(entree.get("scenarios", [])), sum(1 for f in fichiers if f.startswith("src/") and re.search(r"/[0-9a-z]+\.py$", f)))]
    ecrire(os.path.join(sortie, "MANIFESTE.md"), "\n".join(manifeste) + "\n")
    ecrire(os.path.join(sortie, "CARNET-CLES.md"), table_cles(camp, os.path.join(src, "campaign.py")))
    # images.md
    img = ["# images.md (genere depuis le depot)", "", "| card_id | fichier | orientation |", "|---|---|---|"]
    try:
        from PIL import Image  # facultatif
    except Exception:
        Image = None
    for c in cartes:
        cid = c.get("card_id")
        if not cid or "full_link" in c:
            continue
        trouve = None
        for ext in ("jpg", "png", "webp"):
            p = os.path.join(MOTEUR, "assets", "pics", "%s.%s" % (cid, ext))
            if os.path.exists(p):
                trouve = p
                break
        orient = ""
        if trouve and Image:
            try:
                w, h = Image.open(trouve).size
                orient = "paysage" if w > h else "portrait"
            except Exception:
                orient = ""
        img.append("| %s | %s | %s |" % (cid, os.path.basename(trouve) if trouve else "(absente du depot)", orient))
    ecrire(os.path.join(sortie, "images.md"), "\n".join(img) + "\n")
    pages = extraire_pages_livret(code)
    ecrire(os.path.join(sortie, "livret-pages.md"), "# livret-pages.md\n\n```python\n%s```\n" % (pages or "# (pas de livret a decouper pour cette campagne)\n"))
    auteurs = sorted({c.get("custom") for c in cartes if c.get("custom")})
    ecrire(os.path.join(sortie, "CREDITS.md"), "# CREDITS\n\nAuteur(s) (cle `custom` des cartes) : %s\n" % (", ".join(auteurs) or "(contenu officiel)"))
    for nom, txt in (("QUESTIONS.md", "# QUESTIONS\n\n(Aucune : campagne deja integree. Format : manuel §12.4.)\n"),
                     ("BESOINS-MOTEUR.md", "# BESOINS-MOTEUR\n\n(Aucun : campagne deja integree. Format : manuel §12.5.)\n"),
                     ("A_FAIRE_CLAUDE.md", "# A_FAIRE_CLAUDE\n\n(Aucun marqueur : campagne deja integree.)\n"),
                     ("AUTO-VERIFICATION.md", "# AUTO-VERIFICATION\n\n(Exemple de forme : manuel §12.7.)\n"),
                     ("GABARITS.md", "# GABARITS\n\n(Exemple de forme : manuel §6.8.)\n")):
        ecrire(os.path.join(sortie, nom), txt)
    print("livraison de %s ecrite dans %s (%d fichiers dans integration/)" % (pack, sortie, len(fichiers)))


def role(f):
    if f.startswith("data/cards."):
        return "cartes du pack"
    if f.startswith("data/sets_info."):
        return "entree de l'index des packs"
    if f.startswith("data/campagnes/"):
        return "description de la campagne"
    if f.startswith("data/scenarios/"):
        return "scenario" + (" (expert)" if f.endswith("_expert.json") else "")
    if f.startswith("data/encounter_sets/"):
        return "set de rencontre"
    if f.endswith("campaign.py"):
        return "logique de campagne"
    if f.endswith("__init__.py"):
        return "helpers partages"
    if f.startswith("src/"):
        return "script de carte"
    if f.startswith("textes-fr/"):
        return "textes francais"
    if f.startswith("tools/prefixes."):
        return "prefixe fan-made"
    if f.startswith("tools/epreuves."):
        return "epreuves de boucle de campagne"
    if f.startswith("public/js/prepare/mechants-info"):
        return "biographies des vilains"
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pack")
    ap.add_argument("code")
    ap.add_argument("sortie")
    ap.add_argument("--officiel", action="store_true")
    a = ap.parse_args()
    construire(a.pack, a.code, a.sortie, a.officiel)


if __name__ == "__main__":
    main()
