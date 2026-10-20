#!/usr/bin/env python3
"""Construit le KIT DE CREATION DE CAMPAGNE pour une autre IA (20/10/2026).

    python3 outils/construire-kit-campagne.py            # ecrit le MD complet et le zip
    python3 outils/construire-kit-campagne.py --sans-zip # seulement le MD

Ce que ca produit (tout vient du depot, rien n'est recopie a la main) :

  docs/kit-campagne-ia/KIT-CAMPAGNE-COMPLET.md   le manuel : les parties de `docs/kit-campagne-ia/parties/*.md`
                                                 assemblees, avec les directives `{{...}}` remplacees par le
                                                 contenu REEL des fichiers du depot (jamais une copie a la main).
  docs/kit-campagne-ia/LISEZ-MOI.md              a lire d'abord : que donner a l'IA, que recuperer.
  docs/kit-campagne-ia/LISTE-DES-FICHIERS.md     la liste maitresse des fichiers d'une campagne.
  kit-campagne-ia.zip (racine du projet)         le manuel + les modeles (une campagne maison, une officielle)
                                                 + les fichiers communs + les annexes + l'index de l'API du moteur
                                                 + le verificateur de livraison.

Directives reconnues dans les parties (une par ligne, seule sur sa ligne) :

  {{FICHIER:chemin|langage}}              tout le fichier, en bloc de code
  {{EXTRAIT:chemin|debut|fin|langage}}    les lignes debut..fin (1-indexees, incluses)
  {{CARTE:card_id}}                       l'entree de cards.json de cette carte
  {{JSONCLES:chemin}}                     la liste des cles de premier niveau d'un fichier JSON
  {{SECTION:chemin|debut|fin|decalage}}   un morceau de Markdown d'un autre document (titres decales)
  {{INVENTAIRE:pack|code[|officiel]}}      un tableau recapitulatif d'une campagne modele (cartes par set, scripts, scenarios, sets, epreuves...)
  {{PUZZLE:}}                             la liste des commandes `Puzzle.*` du harnais de test, lue dans game/puzzle/puzzle.py
  {{TEXTESFR:prefixe|n}}                 les n premieres entrees de ui-app/src/board/textes-fr-fanmade.ts dont l'id commence par prefixe
  {{PREFIXE:xx}}                          l'entree d'un prefixe dans tools/prefixes_fanmade.json
  {{CHAMP:code|cle}}                      un champ de victoire de data/campagnes/<code>.json, par sa cle
  {{SCENARIOJSON:code|id|sans}}           un objet scenario de data/campagnes/<code>.json (sans = cles omises, separees par des virgules)
  {{BLOC:chemin|debut|fin|langage}}       un morceau d'un fichier de code, delimite par deux reperes de texte (stable si les lignes bougent)
  {{TITRES:chemin|debut|fin}}              la liste des titres (niveaux 3 et 4) d'un morceau de Markdown
  {{SETSINFO:cle}}                        l'entree de data/sets_info.json pour cette cle ("21. The Mad Titan's Shadow")
  {{JSONCLE:chemin|cle}}                  la valeur d'une cle de premier niveau d'un fichier JSON
  {{PREFIXES:}}                           les prefixes fan-made deja pris (registre tools/prefixes_fanmade.json)

Un chemin est relatif a la racine du depot (`Fusion/marvel-lcg-src/...`, `docs/...`, `ui-app/...`).
"""
import argparse
import ast
import io
import json
import os
import re
import sys
import zipfile

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOTEUR = os.path.join(RACINE, "Fusion", "marvel-lcg-src")
KIT = os.path.join(RACINE, "docs", "kit-campagne-ia")
PARTIES = os.path.join(KIT, "parties")
ZIP = os.path.join(RACINE, "kit-campagne-ia.zip")

DIRECTIVE = re.compile(r"^\{\{(FICHIER|EXTRAIT|CARTE|JSONCLES|PREFIXES|SETSINFO|JSONCLE|SECTION|TITRES|BLOC|CHAMP|SCENARIOJSON|TEXTESFR|PREFIXE|PUZZLE|INVENTAIRE):([^}]*)\}\}\s*$")

LANGAGES = {".py": "python", ".json": "json", ".js": "javascript", ".ts": "typescript", ".tsx": "tsx",
            ".css": "css", ".html": "html", ".md": "markdown", ".sh": "bash", ".mjs": "javascript"}


def lire(chemin):
    with io.open(os.path.join(RACINE, chemin), encoding="utf-8", newline="") as f:
        return f.read()


def bloc(code, langage):
    code = code.replace("\r\n", "\n")
    # Une fence plus longue que toute suite de backticks du contenu : le contenu ne la ferme jamais.
    plus_long = max([len(m) for m in re.findall(r"`+", code)] + [2])
    cloture = "`" * max(3, plus_long + 1)
    if not code.endswith("\n"):
        code += "\n"
    return f"{cloture}{langage}\n{code}{cloture}\n"


def langage_de(chemin, force=""):
    return force or LANGAGES.get(os.path.splitext(chemin)[1], "")


_cartes = None


def cartes():
    global _cartes
    if _cartes is None:
        donnees = json.loads(lire("Fusion/marvel-lcg-src/data/cards.json"))
        _cartes = {}
        for pack, liste in donnees.items():
            if pack == "checksum":
                continue
            for c in liste:
                _cartes.setdefault(c.get("card_id"), c)
        personnalisees = json.loads(lire("Fusion/marvel-lcg-src/data/cards_custom.json"))
        for pack, liste in personnalisees.items():
            for c in liste:
                _cartes.setdefault(c.get("card_id"), c)
    return _cartes


_inventaires = {}


def inventaire_modele(pack, code, officiel):
    """Un tableau de ce que contient la livraison reconstituee d'une campagne modele."""
    import collections
    import importlib.util
    import tempfile
    cle = (pack, code, officiel)
    if cle in _inventaires:
        return _inventaires[cle]
    spec = importlib.util.spec_from_file_location("livraison_depuis_le_depot", os.path.join(RACINE, "outils", "livraison-depuis-le-depot.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tmp = tempfile.mkdtemp(prefix="inventaire-")
    import contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        mod.construire(pack, code, os.path.join(tmp, "liv"), officiel)
    integ = os.path.join(tmp, "liv", "integration")
    cartes = json.load(open(os.path.join(integ, "data", "cards.%s.fragment.json" % pack), encoding="utf-8"))[pack]
    par_set = collections.Counter((c.get("set_name") or "(aspect / sans set)") for c in cartes if "set_name" in c)
    par_type = collections.Counter(c.get("type") for c in cartes if c.get("type"))
    scripts = collections.Counter()
    for d, ds, fs in os.walk(os.path.join(integ, "src", "cards", "pack", pack)):
        for f in fs:
            if f.endswith(".py") and f not in ("__init__.py", "campaign.py"):
                scripts[os.path.relpath(d, os.path.join(integ, "src", "cards", "pack", pack))] += 1
    def liste(sous):
        base = os.path.join(integ, *sous.split("/"))
        return sorted(f[:-5] for f in os.listdir(base) if f.endswith(".json")) if os.path.isdir(base) else []
    scen = liste("data/scenarios")
    sets = liste("data/encounter_sets")
    epr = os.path.join(integ, "tools", "epreuves.%s.fragment.py" % code)
    nb_ep = open(epr, encoding="utf-8").read().count('"nom":') if os.path.exists(epr) else 0
    fr = os.path.join(integ, "textes-fr", "%s.fragment.txt" % pack)
    nb_fr = sum(1 for l in open(fr, encoding="utf-8") if re.match(r"^  '", l)) if os.path.exists(fr) else 0
    nb_scripts = sum(scripts.values())
    sortie = ["| Élément | Contenu |", "|---|---|",
              "| Cartes (faces) | **%d** : %s |" % (len(cartes), ", ".join("%s %d" % (t, n) for t, n in par_type.most_common())),
              "| Sets (`set_name`) | %s |" % "; ".join("%s (%d)" % (s, n) for s, n in sorted(par_set.items())),
              "| Scénarios | %d fichiers : %s |" % (len(scen), ", ".join("`%s`" % s for s in scen)),
              "| Sets de rencontre propres au pack | %d : %s |" % (len(sets), ", ".join("`%s`" % s for s in sets)),
              "| Scripts de cartes | **%d** fichiers dans %d dossiers de set |" % (nb_scripts, len(scripts)),
              "| Textes français | %s |" % ("%d entrées" % nb_fr if nb_fr else "**aucune entrée** (manque connu)"),
              "| Épreuves de boucle | %s |" % ("%d" % nb_ep if nb_ep else "aucune"),
              ]
    texte = "\n".join(sortie) + "\n"
    _inventaires[cle] = texte
    return texte


def expanser(ligne):
    m = DIRECTIVE.match(ligne)
    if not m:
        return None
    genre, args = m.group(1), m.group(2).split("|")
    if genre == "FICHIER":
        chemin = args[0]
        return f"*Fichier `{chemin}` (copie exacte, lue dans le depot au moment de la construction).*\n\n" \
               + bloc(lire(chemin), langage_de(chemin, args[1] if len(args) > 1 else ""))
    if genre == "EXTRAIT":
        chemin, debut, fin = args[0], int(args[1]), int(args[2])
        lignes = lire(chemin).split("\n")[debut - 1:fin]
        return f"*Extrait de `{chemin}`, lignes {debut} a {fin}.*\n\n" \
               + bloc("\n".join(lignes), langage_de(chemin, args[3] if len(args) > 3 else ""))
    if genre == "CARTE":
        c = cartes().get(args[0])
        if c is None:
            raise SystemExit(f"directive CARTE : card_id inconnu : {args[0]}")
        return bloc(json.dumps(c, ensure_ascii=False, indent=4), "json")
    if genre == "SECTION":
        # {{SECTION:chemin|debut|fin|decalage}} : le texte Markdown d'un fichier, de la premiere ligne qui COMMENCE par
        # `debut` jusqu'a (exclue) la premiere ligne suivante qui commence par `fin` ; les titres (hors blocs de code)
        # descendent de `decalage` niveaux, pour s'emboiter dans le plan de ce manuel.
        chemin, debut, fin = args[0], args[1], args[2]
        decalage = int(args[3]) if len(args) > 3 and args[3] else 0
        lignes = lire(chemin).split("\n")
        i0 = next((i for i, l in enumerate(lignes) if l.startswith(debut)), None)
        if i0 is None:
            raise SystemExit(f"directive SECTION : debut introuvable dans {chemin} : {debut!r}")
        i1 = next((i for i in range(i0 + 1, len(lignes)) if lignes[i].startswith(fin)), len(lignes))
        sortie_s, dans = [], False
        for l in lignes[i0:i1]:
            if l.startswith("```") or l.startswith("````"):
                dans = not dans
            if not dans and decalage and re.match(r"^#{1,6} ", l):
                l = "#" * decalage + l
            sortie_s.append(l)
        while sortie_s and sortie_s[-1].strip() in ("", "---"):
            sortie_s.pop()
        return f"<!-- extrait de {chemin} -->\n" + "\n".join(sortie_s) + "\n"
    if genre == "INVENTAIRE":
        return inventaire_modele(args[0], args[1], len(args) > 2 and args[2] == "officiel")
    if genre == "PUZZLE":
        arbre = ast.parse(lire("Fusion/marvel-lcg-src/src/game/puzzle/puzzle.py"))
        lignes_p = []
        for n in ast.walk(arbre):
            if isinstance(n, ast.ClassDef) and n.name == "RunPuzzle":
                for m in n.body:
                    if isinstance(m, ast.FunctionDef) and not m.name.startswith("_") and m.name[0].isupper():
                        a = m.args
                        noms = [x.arg for x in a.args if x.arg not in ("self", "cls")]
                        defauts = [None] * (len(a.args) - len(a.defaults)) + list(a.defaults)
                        morceaux = []
                        for x, d in zip(a.args, defauts):
                            if x.arg in ("self", "cls"):
                                continue
                            morceaux.append(x.arg if d is None else f"{x.arg}={ast.unparse(d)}")
                        if a.vararg:
                            morceaux.append("*" + a.vararg.arg)
                        for x, d in zip(a.kwonlyargs, a.kw_defaults):
                            morceaux.append(x.arg if d is None else f"{x.arg}={ast.unparse(d)}")
                        lignes_p.append(f"Puzzle.{m.name}({', '.join(morceaux)})")
        return bloc("\n".join(lignes_p), "text")
    if genre == "PREFIXE":
        pris = json.loads(lire("Fusion/marvel-lcg-src/tools/prefixes_fanmade.json"))["prefixes"]
        return bloc(json.dumps({args[0]: pris[args[0]]}, ensure_ascii=False, indent=2), "json")
    if genre == "TEXTESFR":
        # {{TEXTESFR:prefixe|n}} : les n premieres entrees (commentaire + ligne) de textes-fr-fanmade.ts dont l'id commence par prefixe.
        prefixe, n = args[0], int(args[1])
        lignes = lire("ui-app/src/board/textes-fr-fanmade.ts").split("\n")
        sortie_f, i = [], 0
        while i < len(lignes) and len(sortie_f) < 2 * n:
            m = re.match(r"^  '(" + re.escape(prefixe) + r"[^']*)':", lignes[i])
            if m:
                if i > 0 and lignes[i - 1].lstrip().startswith("//"):
                    sortie_f.append(lignes[i - 1])
                sortie_f.append(lignes[i])
            i += 1
        return bloc("\n".join(sortie_f), "typescript")
    if genre == "CHAMP":
        # {{CHAMP:code|cle}} : le champ de victoire de data/campagnes/<code>.json dont la `cle` est donnee.
        code, cle = args[0], args[1]
        j = json.loads(lire(f"Fusion/marvel-lcg-src/data/campagnes/{code}.json"))
        listes = [s.get("victoire", []) for s in j["scenarios"]] + [j.get("victoire_commune", []), j.get("victoire_commune_expert", [])]
        for liste in listes:
            for champ in liste:
                if champ.get("cle") == cle:
                    return bloc(json.dumps(champ, ensure_ascii=False, indent=2), "json")
        raise SystemExit(f"directive CHAMP : cle introuvable dans {code} : {cle}")
    if genre == "SCENARIOJSON":
        # {{SCENARIOJSON:code|id|sans}} : l'objet scenario de data/campagnes/<code>.json (`sans` = liste de cles a omettre, sep. « , »).
        code, sid = args[0], args[1]
        omis = set(args[2].split(",")) if len(args) > 2 and args[2] else set()
        j = json.loads(lire(f"Fusion/marvel-lcg-src/data/campagnes/{code}.json"))
        for s in j["scenarios"]:
            if s["id"] == sid:
                return bloc(json.dumps({k: v for k, v in s.items() if k not in omis}, ensure_ascii=False, indent=2), "json")
        raise SystemExit(f"directive SCENARIOJSON : scenario introuvable : {code}/{sid}")
    if genre == "BLOC":
        # {{BLOC:chemin|debut|fin|langage}} : les lignes d'un fichier de code, de la premiere ligne qui CONTIENT `debut`
        # jusqu'a (exclue) la premiere ligne suivante qui CONTIENT `fin`. Les numeros de ligne changent, pas les repères.
        chemin, debut, fin = args[0], args[1], args[2]
        lignes = lire(chemin).split("\n")
        i0 = next((i for i, l in enumerate(lignes) if debut in l), None)
        if i0 is None:
            raise SystemExit(f"directive BLOC : debut introuvable dans {chemin} : {debut!r}")
        i1 = next((i for i in range(i0 + 1, len(lignes)) if fin in lignes[i]), len(lignes))
        return f"*Extrait de `{chemin}` (de « {debut.strip()} » a « {fin.strip()} »).*\n\n" \
               + bloc("\n".join(lignes[i0:i1]), langage_de(chemin, args[3] if len(args) > 3 else ""))
    if genre == "TITRES":
        # {{TITRES:chemin|debut|fin}} : la liste des titres (niveaux 3 et 4) d'un morceau de Markdown.
        chemin, debut, fin = args[0], args[1], args[2]
        lignes = lire(chemin).split("\n")
        i0 = next(i for i, l in enumerate(lignes) if l.startswith(debut))
        i1 = next((i for i in range(i0 + 1, len(lignes)) if lignes[i].startswith(fin)), len(lignes))
        sortie_t, dans = [], False
        for l in lignes[i0:i1]:
            if l.startswith("```"):
                dans = not dans
            if not dans and re.match(r"^#{3,4} ", l):
                niveau = len(l) - len(l.lstrip("#"))
                sortie_t.append("  " * (niveau - 3) + "- " + l.lstrip("# ").strip())
        return "\n".join(sortie_t) + "\n"
    if genre == "SETSINFO":
        infos = json.loads(lire("Fusion/marvel-lcg-src/data/sets_info.json"))
        cle = args[0]
        if cle not in infos:
            raise SystemExit(f"directive SETSINFO : cle inconnue : {cle}")
        return bloc(json.dumps({cle: infos[cle]}, ensure_ascii=False, indent=2), "json")
    if genre == "JSONCLE":
        # {{JSONCLE:chemin|cle}} : la valeur d'UNE cle de premier niveau d'un fichier JSON.
        valeur = json.loads(lire(args[0]))[args[1]]
        return bloc(json.dumps({args[1]: valeur}, ensure_ascii=False, indent=2), "json")
    if genre == "PREFIXES":
        pris = json.loads(lire("Fusion/marvel-lcg-src/tools/prefixes_fanmade.json"))["prefixes"]
        return "  " + ", ".join(f"`{k}`" for k in sorted(pris)) + "\n"
    if genre == "JSONCLES":
        j = json.loads(lire(args[0]))
        return ", ".join(f"`{k}`" for k in j.keys()) + "\n"
    raise SystemExit(f"directive inconnue : {genre}")


def assembler(fichiers):
    sortie = []
    for nom in fichiers:
        texte = lire(os.path.relpath(os.path.join(PARTIES, nom), RACINE))
        dedans_bloc = False
        for ligne in texte.split("\n"):
            if ligne.startswith("```"):
                dedans_bloc = not dedans_bloc
            if not dedans_bloc:
                rempl = expanser(ligne)
                if rempl is not None:
                    sortie.append(rempl.rstrip("\n"))
                    continue
            sortie.append(ligne)
        sortie.append("")
    return "\n".join(sortie)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sans-zip", action="store_true")
    args = ap.parse_args()
    fichiers = sorted(f for f in os.listdir(PARTIES) if f.endswith(".md"))
    manuel = assembler(fichiers)
    chemin = os.path.join(KIT, "KIT-CAMPAGNE-COMPLET.md")
    with io.open(chemin, "w", encoding="utf-8", newline="") as f:
        f.write(manuel)
    print(f"{chemin} : {manuel.count(chr(10)) + 1} lignes, {len(manuel.encode()) // 1024} Ko")
    if args.sans_zip:
        return
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import importlib
    zip_kit = importlib.import_module("zip_kit_campagne")
    zip_kit.construire(RACINE, KIT, ZIP)


if __name__ == "__main__":
    main()
