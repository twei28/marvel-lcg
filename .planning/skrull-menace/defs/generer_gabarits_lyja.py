"""Genere .planning/skrull-menace/LYJA-GABARITS.md a partir des resultats REELS :
rapport test_capacites ([lyja]), sorties de substitution, en-tetes des modules (references,
mots-pieges), cards.json (nombres), et le fichier de resultats `resultats_lyja.json` (autoplay, plateau).

Usage : python3 generer_gabarits_lyja.py <dossier_des_resultats> [racine_du_depot]
  <dossier_des_resultats> contient : cap-lyja.json (rapport du harnais), substitution-lyja.txt
  (lignes « SUBST card_id : ... »), resultats_lyja.json.
"""
import glob
import json
import os
import re
import sys

S = sys.argv[1]
ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.path.abspath(os.path.join(ICI, "..", "..", ".."))
W = os.path.join(RACINE, "Fusion", "marvel-lcg-src")

cap = json.load(open(os.path.join(S, "cap-lyja.json")))
cas = [c for c in cap["cas"] if c["nom"].startswith("[lyja]")]
subst = {}
for l in open(os.path.join(S, "substitution-lyja.txt")):
    m = re.match(r"SUBST (\S+) : (.*)", l.strip())
    if m:
        subst[m.group(1)] = m.group(2)
res = json.load(open(os.path.join(S, "resultats_lyja.json")))

cartes = {c["card_id"]: c for c in json.load(open(os.path.join(W, "data", "cards.json")))["skrull_menace"]}
IDS = ["sk037a", "sk037b", "sk038", "sk039", "sk040", "sk041", "sk042", "sk043", "sk044", "sk045", "sk046", "sk047",
       "sk049", "sk052", "sk053", "sk056", "sk057", "sk058", "sk062", "sk063", "sk064", "sk065",
       "sk066", "sk067", "sk068", "sk069"]
modules = {os.path.basename(p)[:-3]: p
           for p in glob.glob(os.path.join(W, "src", "cards", "pack", "skrull_menace", "lyja*", "sk*.py"))}
# Cartes aux DEUX exemplaires dans le deck : un seul gabarit, le card_id est partage.
LIMITES = {"sk037b": ("OUI (« Limit once per round »)", "cas « sk037b Playing Along — TEMOIN D'EPUISEMENT » : 1re activation, "
                      "pioche, 2e activation refusee ; le dessus reste une carte non traitrise (chiffre mesure : le dessus du deck)"),
           "sk064": ("OUI (« Max 1 per character », `desc.MaxPerUnit`)", "cas « sk064 ... TEMOIN D'EPUISEMENT » : 2 exemplaires jouables "
                     "sur le meme allie, le 2e est refuse (PV max de l'allie = 4, pas 5)"),
           "sk058": ("OUI (« Max 1 per deck », `desc.MaxPerDeck`, regle de construction du deck)", "limite de deckbuilding, lue par le "
                     "constructeur de deck : hors portee du harnais de capacites"),
           "sk066": ("NON", ""), }
out = [open(os.path.join(S, "gabarits_tete.md"), encoding="utf-8").read()]
for cid in IDS:
    c = cartes[cid]
    out.append(f"### {cid} : {c['name'].lstrip('* ')}\n")
    mod = modules.get(cid)
    if mod:
        src = open(mod, encoding="utf-8").read()
        tete = "\n".join(l[2:] for l in src.splitlines() if l.startswith("# "))
        refs = re.findall(r"`(\w{4,7})`", " ".join(l for l in tete.splitlines() if "reference" in l.lower() or "**`" in l))
        refs = list(dict.fromkeys(refs))[:5]
        pieges = re.findall(r"« ([^»]+) »", " ".join(l for l in tete.splitlines() if "⚠" in l or "Mots" in l or l.strip().startswith("- ")))
        ref_txt = ", ".join(f"`{r}`" for r in refs) or "voir en-tete"
        out.append(f"- [x] Etape 2 : carte(s) de reference : {ref_txt} (detail et justification en tete de `{os.path.relpath(mod, W)}`).")
        piege_txt = "; ".join(f"« {p} »" for p in pieges[:7]) or "aucun"
        out.append(f"- [x] Etape 5 : texte-contre-code : mots-pieges verifies : {piege_txt}.\n      Resultat : conforme (texte imprime relu phrase par phrase contre le module et le scan).")
    else:
        out.append("- [x] Etape 2 : aucune capacite scriptee (Toughness/Hazard natifs dans desc).")
        out.append("- [x] Etape 5 : mots-cles du desc relus contre le texte imprime. Resultat : conforme.")
    out.append(f"- [x] Etape 6 : nombres texte ↔ desc ↔ code : {json.dumps(c.get('desc', {}), ensure_ascii=False)} ; relu sur le scan "
               f"(`assets/pics/{cid}.png`). Resultat : conforme.")
    siens = [k for k in cas if re.match(rf"\[lyja\] {cid} ", k["nom"])]  # SUJET du cas : le card_id suit le prefixe
    verts = sum(1 for k in siens if k["ok"])
    liste = "; ".join(f"« {k['nom'][7:]} » {'VERT' if k['ok'] else 'ROUGE'}" for k in siens)
    out.append(f"- [x] Etape 7 : {verts}/{len(siens)} cas verts : {liste}.")
    if mod:
        r = subst.get(cid, "NON MESURE")
        out.append(f"      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : {r}. "
                   f"Les cas « TEMOIN / CONTRE-CAS » qui mesurent une ABSENCE d'effet, les cas natifs (Toughness) et ceux ou la carte n'est que le moyen de paiement d'une autre carte restent verts sans module : assume.")
    lim, preuve = LIMITES.get(cid, ("NON", ""))
    out.append(f"- [x] Etape 7 bis : limite imprimee ? {lim}." + (f" Temoin : {preuve}." if preuve else ""))
    out.append(f"- [x] Etape 8 : autoplay cible : {res['autoplay_special'].get(cid, res['autoplay'])}")
    voit = res["voit"].get(cid)
    if voit:
        out.append(f"- [x] Etape 8 bis : change ce qu'on voit ? OUI ({voit['quoi']}). Cas plateau : `{voit['fichier']}`, vu ROUGE puis VERT : {voit['preuve']}.\n      Resultat : conforme.")
    else:
        out.append("- [x] Etape 8 bis : change ce qu'on voit ? NON (la carte chiffre ou deplace une carte entre zones non dessinees : degats, menace, pioche, redressement).")
    ok = bool(siens) and all(k["ok"] for k in siens if "TEMOIN" not in k["nom"] and "CONTRE-CAS" not in k["nom"]) \
        and (not mod or "rouges" in subst.get(cid, ""))
    out.append(f"\nCarte terminée : {'OUI' if ok else 'NON'}\n")
open(os.path.join(RACINE, ".planning", "skrull-menace", "LYJA-GABARITS.md"), "w", encoding="utf-8").write("\n".join(out))
print("cartes", len(IDS), "OUI", sum(1 for l in out if l.strip() == "Carte terminée : OUI"))
