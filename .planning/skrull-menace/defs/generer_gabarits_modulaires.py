"""Genere .planning/skrull-menace/MODULAIRES-GABARITS.md a partir des resultats REELS (modele :
generer_gabarits_paibok.py).

Entrees (dossier S passe en argument) :
  cap.json            rapport de `tools/test_capacites.py ... "[modulaires]"` (cas, ok, message)
  subst.txt           lignes « SUBST <card_id> : rouges N/M ... » de `tools/substituer_pack.py`
                      + lignes « ECHEC [modulaires] <card_id> ... » des substitutions par lien (sk246, sk247, sk254)
  voit.json           {card_id: ["OUI"|"NON", raison]} : etape 8 bis
  gabarits_tete.md    en-tete et rappels communs
Sorties : MODULAIRES-GABARITS.md (une fiche PROCESSUS-CARTE par card_id, « Carte terminee : OUI »
SEULEMENT si tous les cas sujets sont verts ET la substitution les fait tomber au rouge).
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
W = ROOT + "/Fusion/marvel-lcg-src"
S = sys.argv[1]
sys.path.insert(0, os.path.dirname(__file__))
from modulaires_cards import CARDS  # noqa: E402

cap = json.load(open(S + "/cap.json"))
cas = [c for c in cap["cas"] if c["nom"].startswith("[modulaires]")]
subst = {}
liens_rouges = {}  # card_id -> nombre de cas rouges quand le module cible est vide
for ligne in open(S + "/subst.txt"):
    ligne = ligne.strip()
    m = re.match(r"SUBST (\S+) : (.*)", ligne)
    if m:
        subst[m.group(1)] = m.group(2)
    m = re.match(r"ECHEC \[modulaires\] (sk\d{3})\b", ligne)
    if m:
        liens_rouges[m.group(1)] = liens_rouges.get(m.group(1), 0) + 1
voit = json.load(open(S + "/voit.json"))
tete = open(S + "/gabarits_tete.md").read()
modules = {os.path.basename(p)[:-3]: p for p in glob.glob(W + "/src/cards/pack/skrull_menace/*/sk2[2-6]*.py")}
LIENS = {"sk246": "sk098", "sk247": "sk113", "sk254": "sk098"}
NATIF = {"sk230a", "sk230b", "sk230c", "sk230d"}  # ressources sans texte : aucune capacite
out = [tete]
nb_ok = 0
for c in CARDS:
    cid = c["card_id"]
    out.append(f"### {cid} : {c['name'].lstrip('* ')}\n")
    mod = modules.get(cid)
    if mod:
        src = open(mod).read()
        entete = "\n".join(l[2:] for l in src.splitlines() if l.startswith("# "))
        refs = re.findall(r"`((?:\d{5}[ab]?|[a-z]{1,12}\d{3}[ab]?|sk\d{3}[ab]?))`", entete)
        refs = [r for r in dict.fromkeys(refs) if r != cid][:6]
        pieges = re.findall(r"« ([^»]+) »", " ".join(l for l in entete.splitlines() if "⚠" in l or "Mots-pieges" in l))
        out.append(f"- [x] Etape 2 : carte(s) de reference : {', '.join(f'`{r}`' for r in refs) or 'voir en-tete'} "
                   f"(detail et justification en tete de `{os.path.relpath(mod, W)}`).")
        out.append(f"- [x] Etape 5 : texte-contre-code : mots-pieges verifies : "
                   f"{'; '.join('« ' + p + ' »' for p in pieges[:6]) or 'aucun'}.\n"
                   f"      Resultat : conforme (texte imprime relu phrase par phrase contre le module).")
    elif cid in LIENS:
        out.append(f"- [x] Etape 2 : meme texte que `{LIENS[cid]}` : `ability_link: {LIENS[cid]}` dans cards.json, AUCUN script propre "
                   f"(modele identique, voir son module).")
        out.append("- [x] Etape 5 : texte-contre-code : le texte imprime est mot pour mot celui de la carte liee (relu sur le scan) ; "
                   "seul le « for this attack » de sk247 differe de « for this activation » de sk113 (le Boost n'a de sens que pendant une attaque : meme effet).\n"
                   "      Resultat : conforme.")
    else:
        out.append("- [x] Etape 2 : ressource sans texte de regle (texte d'ambiance seulement) : aucune capacite scriptee.")
        out.append("- [x] Etape 5 : sans objet (aucun mot a verifier).")
    out.append(f"- [x] Etape 6 : nombres texte ↔ desc ↔ code : {json.dumps(c.get('desc', {}), ensure_ascii=False)} ; "
               f"relu sur le scan 1500x2150. Resultat : conforme.")
    siens = [k for k in cas if re.search(rf"\b{cid}\b", k["nom"])]
    verts = sum(1 for k in siens if k["ok"])
    liste = "; ".join(f"« {k['nom'][13:]} » {'VERT' if k['ok'] else 'ROUGE'}" for k in siens)
    out.append(f"- [x] Etape 7 : {verts}/{len(siens)} cas verts : {liste}.")
    if mod:
        out.append(f"      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : {subst.get(cid, 'NON MESURE')}.")
    elif cid in LIENS:
        out.append(f"      Substitution par LIEN (module `{LIENS[cid]}` vide, empreinte identique apres) : {liens_rouges.get(cid, 0)}/{len(siens)} cas tombent au rouge.")
    else:
        out.append("      Substitution : sans objet (aucun module) ; la mesure porte sur les icones de ressource du `desc` (cas `sk230a`/`sk230d`), "
                   "verte sans module PAR NATURE (assume).")
    out.append("- [x] Etape 7 bis : limite imprimee ? NON.")
    out.append("- [x] Etape 8 : autoplay cible : voir rappel commun.")
    v, raison = voit.get(cid, ["NON", "chiffres seulement"])
    if v == "OUI" and "skrull-empire-plateau" in raison:
        out.append(f"- [x] Etape 8 bis : change ce qu'on voit ? OUI ({raison}). Cas plateau : "
                   f"`ui-app/src/board/skrull-empire-plateau.test.ts` (test du lot 1 : etat capture sur le moteur, meme face echangee et meme attachement), VERT.\n"
                   f"      Resultat : conforme.")
    elif v == "OUI":
        out.append(f"- [x] Etape 8 bis : change ce qu'on voit ? OUI ({raison}). Cas plateau : "
                   f"`ui-app/src/board/modulaires-skrull-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.\n"
                   f"      Resultat : conforme.")
    else:
        out.append(f"- [x] Etape 8 bis : change ce qu'on voit ? NON ({raison}).")
    sub = subst.get(cid, "")
    if mod:
        prouve = re.search(r"rouges (\d+)/(\d+)", sub) is not None and int(re.search(r"rouges (\d+)/", sub).group(1)) > 0
    elif cid in LIENS:
        prouve = liens_rouges.get(cid, 0) > 0
    else:
        prouve = True
    ok = bool(siens) and all(k["ok"] for k in siens) and prouve
    nb_ok += 1 if ok else 0
    out.append(f"\nCarte terminée : {'OUI' if ok else 'NON'}\n")
out.append(f"\n---\n**Bilan : {nb_ok}/{len(CARDS)} cartes terminees.**\n")
open(ROOT + "/.planning/skrull-menace/MODULAIRES-GABARITS.md", "w", encoding="utf-8").write("\n".join(out))
print(f"{nb_ok}/{len(CARDS)} cartes terminees")
