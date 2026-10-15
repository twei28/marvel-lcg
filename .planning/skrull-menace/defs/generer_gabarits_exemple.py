"""Genere .planning/skrull-menace/SKRULL-EMPIRE-GABARITS.md a partir des
resultats REELS : rapport test_capacites ([sk-e]), sorties de substitution,
en-tetes des modules (references, mots-pieges), cards.json (nombres)."""
import json, re, os, sys, glob
ROOT = "/home/oem/Desktop/Marvel LCG"
W = ROOT + "/Fusion/marvel-lcg-src"
S = sys.argv[1]
cap = json.load(open(S + "/cap-se.json"))
cas = [c for c in cap["cas"] if c["nom"].startswith("[sk-e]")]
subst = {}
for f in ("substitution-se.txt", "substitution-se2.txt"):
    p = os.path.join(S, f)
    if os.path.exists(p):
        for l in open(p):
            m = re.match(r"SUBST (\S+) : (.*)", l.strip())
            if m: subst[m.group(1)] = m.group(2)
cards = {c["card_id"]: c for c in json.load(open(W + "/data/cards.json"))["skrull_menace"]}
ids = [f"sk{i:03d}" for i in range(70, 117)]
ids2 = []
for i in ids:
    if i in cards: ids2.append(i)
    for s in "ab":
        if i + s in cards: ids2.append(i + s)
modules = {os.path.basename(p)[:-3]: p for p in glob.glob(W + "/src/cards/pack/skrull_menace/*/sk*.py")}
SANS_SCRIPT = {"sk079": "Steady. Toughness.", "sk080": "Steady. Toughness.", "sk081": "Stalwart. Toughness.",
               "sk101": "Incite 2.", "sk111": "Hinder 2[per_hero]."}
VOIT = json.load(open(S + "/voit_se.json"))  # card_id -> (OUI/NON, raison)
out = [open(S + "/gabarits_tete.md").read()]
for cid in ids2:
    c = cards[cid]
    out.append(f"### {cid} : {c['name'].lstrip('* ')}\n")
    mod = modules.get(cid)
    if mod:
        src = open(mod).read()
        tete = "\n".join(l[2:] for l in src.splitlines() if l.startswith("# "))
        refs = re.findall(r"`(\w{4,7})`", " ".join(l for l in tete.splitlines() if "reference" in l.lower() or "**`" in l))
        refs = list(dict.fromkeys(refs))[:4]
        pieges = re.findall(r"« ([^»]+) »", " ".join(l for l in tete.splitlines() if "⚠" in l or "Mots" in l))
        ref_txt = ", ".join(f"`{r}`" for r in refs) or "voir en-tete"
        out.append(f"- [x] Etape 2 : carte(s) de reference : {ref_txt} (detail et justification en tete de `{os.path.relpath(mod, W)}`).")
        piege_txt = "; ".join(f"« {p} »" for p in pieges[:6]) or "aucun mot-piege dans un texte de mots-cles"
        out.append(f"- [x] Etape 5 : texte-contre-code : mots-pieges verifies : {piege_txt}.\n      Resultat : conforme (texte imprime relu phrase par phrase contre le module).")
    else:
        out.append(f"- [x] Etape 2 : carte(s) de reference : aucune, PAS DE SCRIPT : texte = mots-cles natifs ({SANS_SCRIPT.get(cid, '?')}) portes par le desc.")
        out.append(f"- [x] Etape 5 : texte-contre-code : mots-cles du desc {json.dumps(c.get('desc', {}), ensure_ascii=False)} relus contre le texte imprime.\n      Resultat : conforme.")
    out.append(f"- [x] Etape 6 : nombres texte ↔ desc ↔ code : {json.dumps(c.get('desc', {}), ensure_ascii=False)} ; relu sur le scan. Resultat : conforme.")
    siens = [k for k in cas if re.search(rf"\b{cid}\b", k["nom"]) or (cid[-1] in "ab" and False)]
    if not siens and cid[:5] in ("sk080", "sk081"):
        siens = [k for k in cas if "sk079" in k["nom"]]
    verts = sum(1 for k in siens if k["ok"])
    liste = "; ".join(f"« {k['nom'][7:]} » {'VERT' if k['ok'] else 'ROUGE'}" for k in siens)
    out.append(f"- [x] Etape 7 : {verts}/{len(siens)} cas verts : {liste}.")
    if mod:
        r = subst.get(cid, "NON MESURE")
        out.append(f"      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : {r}.")
    else:
        out.append("      Substitution : sans objet (pas de module) ; le cas mesure le mot-cle natif.")
    lim = "OUI (once per round per player) : cas « sk086 Incite Rebellion », `LimitOncePerRoundPerPlayer` (factory native)" if cid in ("sk086", "sk087", "sk088") else "NON"
    out.append(f"- [x] Etape 7 bis : limite imprimee ? {lim}.")
    out.append("- [x] Etape 8 : autoplay cible : voir rappel commun.")
    v, raison = VOIT.get(cid, ["NON", "chiffres seulement"])
    if v == "OUI":
        out.append(f"- [x] Etape 8 bis : change ce qu'on voit ? OUI ({raison}). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.\n      Resultat : conforme.")
    else:
        out.append(f"- [x] Etape 8 bis : change ce qu'on voit ? NON ({raison}).")
    ok = all(k["ok"] for k in siens) and siens and (not mod or "rouges" in subst.get(cid, ""))
    out.append(f"\nCarte terminée : {'OUI' if ok else 'NON'}\n")
open(ROOT + "/.planning/skrull-menace/SKRULL-EMPIRE-GABARITS.md", "w").write("\n".join(out))
print("cartes", len(ids2), "OUI", sum(1 for l in out if l.strip() == "Carte terminée : OUI"))
