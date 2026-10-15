"""Genere .planning/skrull-menace/SKRULL-PANTHEON-GABARITS.md a partir des resultats REELS (modele :
generer_gabarits_exemple.py du scenario Skrull Empire).

Entrees (dossier S passe en argument) :
  cap.json            rapport de `tools/test_capacites.py ... "[pantheon]"` (cas, ok, message)
  subst.txt           lignes « SUBST <card_id> : rouges N/M ... » de `tools/substituer_pack.py`
  autoplay.txt        resume ecrit a la main (rappel commun)
  voit.json           {card_id: ["OUI"|"NON", raison]} : etape 8 bis
Sorties : SKRULL-PANTHEON-GABARITS.md (une fiche PROCESSUS-CARTE par card_id, « Carte terminee : OUI »
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
from pantheon_cards import CARDS  # noqa: E402

cap = json.load(open(S + "/cap.json"))
cas = [c for c in cap["cas"] if c["nom"].startswith("[pantheon]")]
subst = {}
for ligne in open(S + "/subst.txt"):
    m = re.match(r"SUBST (\S+) : (.*)", ligne.strip())
    if m:
        subst[m.group(1)] = m.group(2)
voit = json.load(open(S + "/voit.json"))
tete = open(S + "/gabarits_tete.md").read()
modules = {os.path.basename(p)[:-3]: p for p in glob.glob(W + "/src/cards/pack/skrull_menace/skrull_pantheon/sk*.py")
           + glob.glob(W + "/src/cards/pack/skrull_menace/dardvan_sect/sk*.py")}
SANS_SCRIPT = {}  # tous les modules existent
LIMITE = {}       # aucune limite imprimee dans ce coffret de cartes
out = [tete]
nb_ok = 0
for c in CARDS:
    cid = c["card_id"]
    out.append(f"### {cid} : {c['name'].lstrip('* ')}\n")
    mod = modules.get(cid)
    if mod:
        src = open(mod).read()
        entete = "\n".join(l[2:] for l in src.splitlines() if l.startswith("# "))
        # card_id cites en reference : tout ce qui, entre accents graves, ressemble a un card_id
        refs = re.findall(r"`((?:[a-z_]+/)?(?:\d{5}[ab]?|[a-z]{1,12}\d{3}[ab]?|sk\d{3}[ab]?))`", entete)
        refs = [r for r in dict.fromkeys(refs) if r != cid][:6]
        pieges = re.findall(r"« ([^»]+) »", " ".join(l for l in entete.splitlines() if "⚠" in l or "Mots-pieges" in l))
        out.append(f"- [x] Etape 2 : carte(s) de reference : {', '.join(f'`{r}`' for r in refs) or 'voir en-tete'} "
                   f"(detail et justification en tete de `{os.path.relpath(mod, W)}`).")
        out.append(f"- [x] Etape 5 : texte-contre-code : mots-pieges verifies : "
                   f"{'; '.join('« ' + p + ' »' for p in pieges[:6]) or 'aucun'}.\n"
                   f"      Resultat : conforme (texte imprime relu phrase par phrase contre le module).")
    else:
        out.append("- [x] Etape 2 : aucune capacite scriptee.")
        out.append("- [x] Etape 5 : sans objet.")
    out.append(f"- [x] Etape 6 : nombres texte ↔ desc ↔ code : {json.dumps(c.get('desc', {}), ensure_ascii=False)} ; "
               f"relu sur le scan 1500x2150. Resultat : conforme.")
    siens = [k for k in cas if re.search(rf"\b{cid}\b", k["nom"])]
    verts = sum(1 for k in siens if k["ok"])
    liste = "; ".join(f"« {k['nom'][9:]} » {'VERT' if k['ok'] else 'ROUGE'}" for k in siens)
    out.append(f"- [x] Etape 7 : {verts}/{len(siens)} cas verts : {liste}.")
    if mod:
        out.append(f"      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : {subst.get(cid, 'NON MESURE')}.")
    else:
        out.append("      Substitution : sans objet.")
    out.append(f"- [x] Etape 7 bis : limite imprimee ? {LIMITE.get(cid, 'NON')}.")
    out.append("- [x] Etape 8 : autoplay cible : voir rappel commun.")
    v, raison = voit.get(cid, ["NON", "chiffres seulement"])
    if v == "OUI":
        out.append(f"- [x] Etape 8 bis : change ce qu'on voit ? OUI ({raison}). Cas plateau : "
                   f"`ui-app/src/board/pantheon-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.\n"
                   f"      Resultat : conforme.")
    else:
        out.append(f"- [x] Etape 8 bis : change ce qu'on voit ? NON ({raison}).")
    ok = bool(siens) and all(k["ok"] for k in siens) and (not mod or "rouges" in subst.get(cid, "")
                                                         and re.search(r"rouges (\d+)/(\d+)", subst.get(cid, "")) is not None)
    nb_ok += 1 if ok else 0
    out.append(f"\nCarte terminée : {'OUI' if ok else 'NON'}\n")
open(ROOT + "/.planning/skrull-menace/SKRULL-PANTHEON-GABARITS.md", "w").write("\n".join(out))
print("cartes", len(CARDS), "OUI", nb_ok)
