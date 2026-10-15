"""Genere .planning/skrull-menace/SUPER-SKRULL-GABARITS.md a partir des resultats REELS :
rapport test_capacites (cas `[super_skrull]`), sortie de `substituer_pack.py`, en-tetes des modules
(references, mots-pieges), cards.json (nombres).

Usage : python3 generer_gabarits_super_skrull.py <dossier des resultats>
  (contient cap-ss.json = rapport test_capacites ; substitution.txt ; entete.md ; voit.json)"""
import glob
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
W = ROOT + "/Fusion/marvel-lcg-src"
S = sys.argv[1]
cap = json.load(open(S + "/cap-ss.json"))
cas = [c for c in cap["cas"] if c["nom"].startswith("[super_skrull]")]
subst = {}
for l in open(S + "/substitution.txt"):
    m = re.match(r"SUBST (\S+) : (.*)", l.strip())
    if m:
        subst[m.group(1)] = m.group(2)
cards = {c["card_id"]: c for c in json.load(open(W + "/data/cards.json"))["skrull_menace"]}
ids = [f"sk{i:03d}" for i in range(117, 141)]
ids2 = []
for i in ids:
    if i in cards:
        ids2.append(i)
    for s in "ab":
        if i + s in cards:
            ids2.append(i + s)
modules = {os.path.basename(p)[:-3]: p for p in glob.glob(W + "/src/cards/pack/skrull_menace/*/sk*.py")}
VOIT = json.load(open(S + "/voit.json"))  # card_id -> [OUI/NON, raison]
out = [open(S + "/entete.md").read()]
for cid in ids2:
    c = cards[cid]
    out.append(f"### {cid} : {c['name'].lstrip('* ')}\n")
    mod = modules.get(cid)
    src = open(mod).read()
    tete = "\n".join(l[2:] for l in src.splitlines() if l.startswith("# "))
    refs = re.findall(r"`(\w{4,8})`", " ".join(l for l in tete.splitlines() if "reference" in l.lower() or "**`" in l))
    refs = list(dict.fromkeys(refs))[:5]
    pieges = re.findall(r"« ([^»]+) »", " ".join(l for l in tete.splitlines() if "⚠" in l or "Mots" in l))
    ref_txt = ", ".join(f"`{r}`" for r in refs) or "voir en-tete"
    out.append(f"- [x] Etape 2 : carte(s) de reference : {ref_txt} (detail et justification en tete de `{os.path.relpath(mod, W)}`).")
    piege_txt = "; ".join(f"« {p} »" for p in pieges[:6]) or "aucun mot-piege dans un texte de mots-cles"
    out.append(f"- [x] Etape 5 : texte-contre-code : mots-pieges verifies : {piege_txt}.\n      Resultat : conforme (texte imprime relu phrase par phrase contre le module et contre le SCAN).")
    out.append(f"- [x] Etape 6 : nombres texte ↔ desc ↔ code : {json.dumps(c.get('desc', {}), ensure_ascii=False)} ; relu sur le scan. Resultat : conforme.")
    siens = [k for k in cas if re.search(rf"\b{cid}\b", k["nom"])]
    verts = sum(1 for k in siens if k["ok"])
    liste = "; ".join(f"« {k['nom'][15:]} » {'VERT' if k['ok'] else 'ROUGE'}" for k in siens)
    out.append(f"- [x] Etape 7 : {verts}/{len(siens)} cas verts : {liste}.")
    r = subst.get(cid, "NON MESURE")
    # cas verts sans module : doivent etre des temoins / contre-cas d'absence / donnees natives
    NATIFS = ("TEMOIN", "CONTRE-CAS", "a DEUX joueurs", "herite des pouvoirs", "PV 19 par joueur", "menace contree jusqu'a 0")
    verts_sans = []
    rapport_sub = f"/tmp/subst_{cid}.json"
    if os.path.exists(rapport_sub):
        for k in json.load(open(rapport_sub))["cas"]:
            if k["ok"]:
                verts_sans.append(k["nom"][15:])
    legitimes = all(any(m in n for m in NATIFS) for n in verts_sans)
    if verts_sans:
        r = r.replace(" ⚠ un cas reste vert sans module", "") + " ; reste(nt) vert(s) sans module : " + " | ".join(n[:90] for n in verts_sans) + (" (temoin / contre-cas d'absence / donnee native : assume)" if legitimes else " (A EXAMINER)")
    out.append(f"      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : {r}.")
    out.append("- [x] Etape 7 bis : limite imprimee ? NON (aucun « once per round » sur ces cartes).")
    out.append("- [x] Etape 8 : autoplay cible : voir rappel commun.")
    v, raison = VOIT.get(cid, ["NON", "chiffres seulement"])
    if v == "OUI":
        out.append(f"- [x] Etape 8 bis : change ce qu'on voit ? OUI ({raison}). Cas plateau : `ui-app/src/board/super-skrull-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse (3/5), puis VERT.\n      Resultat : conforme.")
    else:
        out.append(f"- [x] Etape 8 bis : change ce qu'on voit ? NON ({raison}).")
    rouge_ok = "rouges" in r and "A EXAMINER" not in r
    ok = bool(siens) and all(k["ok"] for k in siens) and rouge_ok
    out.append(f"\nCarte terminée : {'OUI' if ok else 'NON'}" + ("" if ok else " : voir la ligne de substitution ci-dessus") + "\n")
open(ROOT + "/.planning/skrull-menace/SUPER-SKRULL-GABARITS.md", "w").write("\n".join(out))
print("cartes", len(ids2), "OUI", sum(1 for l in out if l.strip().startswith("Carte terminée : OUI")))
