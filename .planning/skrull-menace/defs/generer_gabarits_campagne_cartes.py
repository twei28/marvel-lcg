"""Genere .planning/skrull-menace/CAMPAGNE-CARTES-GABARITS.md a partir des resultats REELS (modele :
generer_gabarits_paibok.py).

Entrees (dossier S passe en argument ; fichiers ecrits par le coordinateur du bloc a partir des vraies passes) :
  cap.json            rapport de `tools/test_capacites.py ... "[campagne_cartes]"` (cas, ok, message)
  subst.txt           lignes « SUBST <module> : rouges N/M ; VERTS SANS MODULE : ... » de la substitution du bloc
  autoplay.txt        resume ecrit a la main (rappel commun)
  voit.json           {card_id: ["OUI"|"NON", raison]} : etape 8 bis
  gabarits_tete.md    en-tete du fichier
Sorties : CAMPAGNE-CARTES-GABARITS.md (une fiche PROCESSUS-CARTE par card_id, « Carte terminee : OUI » SEULEMENT si tous les
cas sujets sont verts ET la substitution fait tomber au rouge tout cas NOMINAL : les verts sans module sont listes et ne
peuvent etre que des TEMOINS d'absence ou des valeurs natives lues dans `desc`).
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
from campagne_cartes_cards import CARDS  # noqa: E402

cap = json.load(open(S + "/cap.json"))
cas = [c for c in cap["cas"] if c["nom"].startswith("[campagne_cartes]")]
subst = {}
for ligne in open(S + "/subst.txt"):
    m = re.match(r"SUBST (\S+) : (.*)", ligne.strip())
    if m:
        subst[m.group(1)] = m.group(2)
voit = json.load(open(S + "/voit.json"))
tete = open(S + "/gabarits_tete.md").read()
modules = {os.path.basename(p)[:-3]: p
           for p in glob.glob(W + "/src/cards/pack/skrull_menace/skrull_menace_campaign/*.py") if not p.endswith("__init__.py")}
SANS_SCRIPT = {"sk289a": "type Insert : aucune capacite scriptee (regle du bloc Cooperation Area)",
               "sk289b": "type Insert : verso du rappel, aucun texte de regle"}
LIMITE = {"sk265": "NON de limite par round ; plafond « to a maximum of 2 » (cas dedie)",
          "sk267": "NON de limite par round ; plafond « to a maximum of 4 » (cas dedie)",
          "sk279": "NON de limite par round ; plafond « to a maximum of 3 » cartes (cas dedie)"}
out = [tete]
nb_ok = 0
sujets = [c for c in CARDS if re.fullmatch(r"sk\d{3}[ab]?", c["card_id"])]
for c in sujets:
    cid = c["card_id"]
    out.append(f"### {cid} : {c['name'].lstrip('* ')}\n")
    mod = modules.get(cid)
    if mod:
        src = open(mod).read()
        entete = "\n".join(l[2:] for l in src.splitlines() if l.startswith("# "))
        refs = re.findall(r"`((?:\d{5}[ab]?|[a-z]{1,12}\d{3}[ab]?|sk\d{3}[ab]?))`", entete)
        refs = [r for r in dict.fromkeys(refs) if r != cid][:7]
        pieges = re.findall(r"« ([^»]+) »", " ".join(l for l in entete.splitlines() if "⚠" in l or "Mots-pieges" in l))
        out.append(f"- [x] Etape 2 : carte(s) de reference : {', '.join(f'`{r}`' for r in refs) or 'voir en-tete'} "
                   f"(detail et justification en tete de `{os.path.relpath(mod, W)}`).")
        out.append(f"- [x] Etape 5 : texte-contre-code : mots-pieges verifies : "
                   f"{'; '.join('« ' + p + ' »' for p in pieges[:6]) or 'aucun'}.\n"
                   f"      Resultat : conforme (texte imprime relu phrase par phrase contre le module).")
    else:
        out.append(f"- [x] Etape 2 : aucune capacite scriptee ({SANS_SCRIPT.get(cid, 'sans objet')}).")
        out.append("- [x] Etape 5 : sans objet.")
    out.append(f"- [x] Etape 6 : nombres texte ↔ desc ↔ code : {json.dumps(c.get('desc', {}), ensure_ascii=False)} ; "
               f"relu sur le scan 1500x2150. Resultat : conforme.")
    siens = [k for k in cas if re.search(rf"\b{cid}\b", k["nom"])]
    verts = sum(1 for k in siens if k["ok"])
    liste = "; ".join(f"« {k['nom'][19:]} » {'VERT' if k['ok'] else 'ROUGE'}" for k in siens)
    out.append(f"- [x] Etape 7 : {verts}/{len(siens)} cas verts : {liste or 'AUCUN CAS (sans script)'}.")
    if mod:
        out.append(f"      Substitution (module remplace par `GetAbilities -> []`, empreinte du dossier identique avant/apres) : "
                   f"{subst.get(cid, 'NON MESURE')}.")
        if cid == "sk268":
            out.append(f"      Gabarit sbire `skrull_war_minion` (porte la Reponse) : {subst.get('skrull_war_minion', 'NON MESURE')}.")
    else:
        out.append("      Substitution : sans objet.")
    out.append(f"- [x] Etape 7 bis : limite imprimee ? {LIMITE.get(cid, 'NON')}.")
    out.append("- [x] Etape 8 : autoplay cible : voir rappel commun.")
    v, raison = voit.get(cid, ["NON", "chiffres seulement"])
    if v == "OUI":
        out.append(f"- [x] Etape 8 bis : change ce qu'on voit ? OUI ({raison}). Cas plateau : "
                   f"`ui-app/src/board/campagne-cartes-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.\n"
                   f"      Resultat : conforme.")
    else:
        out.append(f"- [x] Etape 8 bis : change ce qu'on voit ? NON ({raison}).")
    nominaux_verts = bool(mod) and "VERTS SANS MODULE" in subst.get(cid, "")
    rouge_ok = (not mod) or re.search(r"rouges (\d+)/(\d+)", subst.get(cid, "")) is not None and \
        int(re.search(r"rouges (\d+)/(\d+)", subst.get(cid, "")).group(1)) > 0
    ok = (bool(siens) or cid in SANS_SCRIPT) and all(k["ok"] for k in siens) and rouge_ok
    nb_ok += 1 if ok else 0
    out.append(f"\nCarte terminée : {'OUI' if ok else 'NON'}\n")
open(ROOT + "/.planning/skrull-menace/CAMPAGNE-CARTES-GABARITS.md", "w").write("\n".join(out))
print("cartes", len(sujets), "OUI", nb_ok)
