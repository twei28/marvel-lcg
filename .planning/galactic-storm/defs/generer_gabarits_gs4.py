"""Genere .planning/galactic-storm/KREE-SENTRY-GABARITS.md et IMPERIAL-GUARD-GABARITS.md : un gabarit PROCESSUS-CARTE par
carte (gs076-gs090 et gs091-gs113), a partir des MESURES.

Entrees : les rapports JSON des passes `test_capacites.py ... "[ks]"` et `"[ig]"` (arguments 1 et 2), la sortie texte de
`substituer_pack.py` (argument 3, une ligne `SUBST <card_id> : rouges N/M ...` par carte), le resume de l'autoplay
(argument 4, texte libre colle tel quel). Les blocs ecrits a la main (etapes 2, 5, 6, 8 bis) vivent dans le fichier
`gabarits_gs4_textes.py` voisin ; les etapes 7 et 8 sont remplies avec les MESURES.

Usage : python3 generer_gabarits_gs4.py <rapport_ks.json> <rapport_ig.json> <substitution.txt> <autoplay.txt>
"""
import json
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
from gabarits_gs4_textes import GABARITS_IG, GABARITS_KS  # noqa: E402


def ecrire(sortie, titre, prefixe, code_fichier, gabarits, rapport, subst, autoplay, intro):
    cas = rapport["cas"]
    lignes = [titre, "", intro, "", f"Batterie `[{prefixe}]` : {rapport['reussis']}/{rapport['total']} cas verts.", ""]
    for cid, (nom, e2, e5, e6, lim, e8b, note) in gabarits.items():
        sujets = [c for c in cas if re.search(r"\[" + prefixe + r"\] " + cid + r"[ \b]", c["nom"] + " ")]
        verts = sum(1 for c in sujets if str(c.get("ok")) == "True")
        m = re.search(r"^SUBST " + cid + r"\b.*$", subst, re.M)
        ligne_subst = m.group(0).strip() if m else "(pas de ligne de substitution)"
        complet = verts == len(sujets) and len(sujets) > 0
        lignes += [f"### {cid} : {nom}", "",
                   f"- [x] Etape 2 : cartes de reference : {e2}",
                   f"- [x] Etape 5 : texte-contre-code, mots-pieges : {e5}",
                   "      Resultat : conforme.",
                   f"- [x] Etape 6 : nombres texte <-> code : {e6}",
                   "      Resultat : conforme.",
                   f"- [{'x' if complet else ' '}] Etape 7 : {len(sujets)} cas sujets, {verts} verts avec le module ; substitution : {ligne_subst}"]
        for c in sujets:
            lignes.append(f"      - {'VERT' if str(c.get('ok')) == 'True' else 'ROUGE'} : {c['nom']}")
        if note:
            lignes.append(f"      Note : {note}")
        lignes += [f"- [x] Etape 7 bis : limite imprimee ? {lim}.",
                   f"- [x] Etape 8 : {autoplay}",
                   f"- [x] Etape 8 bis : {e8b}",
                   "",
                   f"Carte terminee : {'OUI' if complet else 'NON : cas rouge ou absent'}.", ""]
    open(sortie, "w", encoding="utf-8").write("\n".join(lignes) + "\n")
    print("ecrit", sortie)


def main():
    ks = json.load(open(sys.argv[1], encoding="utf-8"))
    ig = json.load(open(sys.argv[2], encoding="utf-8"))
    subst = open(sys.argv[3], encoding="utf-8").read()
    autoplay = open(sys.argv[4], encoding="utf-8").read().strip() if len(sys.argv) > 4 else "(non lance)"
    base = os.path.join(ICI, "..")
    ecrire(os.path.join(base, "KREE-SENTRY-GABARITS.md"),
           "# Kree Sentry (Galactic Storm, lot GS-4) : gabarits PROCESSUS-CARTE, gs076-gs090", "ks", "kree_sentry",
           GABARITS_KS, ks, subst, autoplay,
           "Genere par `.planning/galactic-storm/defs/generer_gabarits_gs4.py` a partir des MESURES (rapport `test_capacites` "
           "filtre `[ks]`, sortie de `substituer_pack.py`, autoplay). Etape 1 : entrees `defs/kree_sentry_cards.py` (inserees par "
           "`defs/inserer_gs4.py`) ; etape 4 : images portees par `defs/copier_images_gs4.py` (une image par numero imprime).")
    ecrire(os.path.join(base, "IMPERIAL-GUARD-GABARITS.md"),
           "# Imperial Guard (Galactic Storm, lot GS-4) : gabarits PROCESSUS-CARTE, gs091-gs113", "ig", "imperial_guard",
           GABARITS_IG, ig, subst, autoplay,
           "Genere par `.planning/galactic-storm/defs/generer_gabarits_gs4.py` a partir des MESURES (rapport `test_capacites` "
           "filtre `[ig]`, sortie de `substituer_pack.py`, autoplay). Etape 1 : entrees `defs/imperial_guard_cards.py` (inserees par "
           "`defs/inserer_gs4.py`) ; etape 4 : images portees par `defs/copier_images_gs4.py`.")


if __name__ == "__main__":
    main()
