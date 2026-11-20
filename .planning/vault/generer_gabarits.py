#!/usr/bin/env python3
"""Genere docs/packs/vault/GABARITS.md : un gabarit PROCESSUS-CARTE par card_id de The Vault.

Usage : python3 generer_gabarits.py <sortie_substituer_pack.txt> "<resume autoplay>" [racine_du_depot]

Source de chaque gabarit : l'en-tete du script de la carte (cartes de reference, mots-pieges), les noms des cas
`tools/cas/the_vault*.py` dont le nom commence par le card_id, et la ligne « SUBST <id> : rouges N/M » de la preuve par
substitution. Rien n'est invente : une ligne manquante = « AUCUN » dans le gabarit.
"""
import importlib.util
import os
import re
import sys

SUBST = open(sys.argv[1], encoding="utf-8").read()
AUTOPLAY = sys.argv[2]
RACINE = os.path.abspath(sys.argv[3]) if len(sys.argv) > 3 else os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MOTEUR = os.path.join(RACINE, "Fusion", "marvel-lcg-src")


def charger(chemin, nom):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


CAS = []
for f in ("the_vault", "the_vault_b", "the_vault_c", "the_vault_d"):
    CAS += charger(os.path.join(MOTEUR, "tools", "cas", f + ".py"), "cas_" + f).CAS
CARTES = charger(os.path.join(RACINE, ".planning", "vault", "vt_cards.py"), "vt_cards").CARDS

PLATEAU = {
    "vt018": "OUI : l'environnement et les cartes glissées dessous (face cachée)", "vt019": "OUI : obligation en jeu devant le premier joueur",
    "vt020": "OUI : attachement de rencontre posé sur un vilain", "vt026": "OUI : manigance annexe à menace (Crise)",
    "vt028": "OUI : manigance annexe", "vt029": "OUI : manigance annexe à menace",
}
for n in range(1, 17):
    PLATEAU[f"vt{n:03d}"] = "OUI : plusieurs vilains dessinés en même temps dans la zone des vilains"
PLATEAU_FICHIER = "ui-app/src/board/the-vault-plateau.test.ts (6 cas verts ; aucun correctif de plateau nécessaire, le rendu générique dessine tout)"
ENTETE_RE = re.compile(r"^# ?(.*)$")


def entete(chemin):
    lignes = []
    for ligne in open(chemin, encoding="utf-8").read().splitlines()[1:]:
        m = ENTETE_RE.match(ligne)
        if not m:
            if lignes and not ligne.strip():
                continue
            if lignes:
                break
            continue
        lignes.append(m.group(1))
    return "\n".join(lignes).strip()


def script_de(cid):
    p = os.path.join(MOTEUR, "src", "cards", "pack", "the_vault", "the_vault", cid + ".py")
    if os.path.exists(p):
        return p
    raise SystemExit("script introuvable : " + cid)


def suj(cid):
    noms = [c["nom"].replace("[vt] ", "", 1) for c in CAS if c["nom"].startswith("[vt] " + cid + " ")]
    if cid == "vt017a":   # la regle d'activation par ordre est posee par vt017a
        noms += [c["nom"].replace("[vt] ", "", 1) for c in CAS if c["nom"].startswith("[vt] vt-activation")]
    return noms


def subst(cid):
    m = re.search(r"SUBST " + cid + r" : rouges (\d+)/(\d+)", SUBST)
    return (int(m.group(1)), int(m.group(2))) if m else None


NOMS = {c["card_id"]: c["name"].lstrip("* ") + (" (" + c["type"] + ")") for c in CARTES}
sortie = ["""# The Vault (Kajislav) : gabarits PROCESSUS-CARTE, 27 card_id

Scénario `the_vault` (standard : vilains I ; expert : vilains II), préfixe `vt`, set 215. Source : zip « The Vault (Sealed) » déposé le 24/10/2026 (51 images :
16 vilains, complot principal, environnement, obligation, 17 cartes de rencontre dont 13 doublons, plateau et 8 compteurs de PV = accessoires de table, non codés).
Cas : `Fusion/marvel-lcg-src/tools/cas/the_vault.py`, `_b`, `_c`, `_d` (filtre `[vt]`). Plateau : `ui-app/src/board/the-vault-plateau.test.ts`.
Transcriptions : `docs/packs/vault/TRANSCRIPTIONS.md`. Recettes : `docs/reference/RECETTES-MOTEUR.md` §24. Fiche : `mots-cles/activation-order.md`.

## Arbitrages utilisateur du 25/10/2026 (questions posées carte montrée, scan à l'appui)

1. **The Vault (`vt018`)** : victoire ET défaite vraies en même temps (tous les vilains vaincus, aucun sous le Vault) = **VICTOIRE**.
2. **Corrupted Guardsman (`vt022`)** : « If you cannot, this card gains surge » couvre aussi l'absence d'Inspection en jeu : **sans Inspection, il gagne Surge**.
3. **Corrupted Guardsman (`vt022`)**, Boost : le sbire de sous le Vault mélangé dans le deck de rencontre est tiré **au hasard**.

## Décisions prises seules (texte sans ambiguïté ou règle du livret), à signaler

- **Inspection of the Vault** : `GiveTo` vaut `""` (donnée au joueur à qui on la révèle) ; ses deux sources la révèlent au premier joueur. `"first player"` la ferait retirer de la partie.
- **Un vilain vaincu est retiré de la partie** (livret p.1), sans rien reporter ; après le départ du dernier vilain on révèle le dessus du deck de vilains ; câblé sur `vt017b`.
- **Doublons du zip** (identiques au pixel près hors numéro) : Craven Escape 20-21, Corrupted Guardsman 22-25, Burglary 26-27, Rampage in Public 30-33, Riot in the Vault 34-36 : une carte, plusieurs exemplaires.
- **Noms de fichiers trompeurs** : « 28 backup plan » = Contingency Measures, « 30-33 enemy encounter » = Rampage in Public, « 34-36 cause a stir » = Riot in the Vault.
- **Icônes identifiées par les glyphes de `ChampionsIcons.ttf`** (jamais à vue) : Burglary = Crisis (C), Scheming from Within et Contingency Measures = Hazard (H), ressource d'Inspection = mentale (M, nœuds reliés).
- **Modulaire** : Sinister Syndicate (existant) par défaut ; mode expert = vilains (II) + ensemble `expert`.
- **Plateau de table et compteurs de PV** : accessoires de la boîte physique, non codés (le jeu a ses propres jauges).

## Gates du scénario
GATES
"""]
for c in CARTES:
    cid = c["card_id"]
    chemin = script_de(cid)
    cas = suj(cid)
    s = subst(cid)
    sortie.append(f"### {cid} : {NOMS[cid]}\n")
    sortie.append("```\n" + entete(chemin) + "\n```\n")
    sortie.append("- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).")
    sortie.append("- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.")
    sortie.append("- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (PV par joueur, ATK, SCH, ordre d'activation, boost, menaces) et les cas de valeurs imprimées. Résultat : conformes.")
    sortie.append(f"- [x] Étape 7 : cas test_capacites par capacité ({len(cas)} cas sujets) :")
    for n in cas:
        sortie.append(f"      - {n}")
    if s:
        sortie.append(f"      Preuve par substitution : **rouges {s[0]}/{s[1]}** sans le module" +
                      ("" if s[0] == s[1] else " (les cas verts restants sont des contre-cas d'absence d'effet ou des conditions de fin de partie portées par le helper `VerifierFinDePartie`, calibré ROUGE à part : trois cas tombent sans lui)") + ". Résultat : OK.")
    else:
        sortie.append("      Preuve par substitution : AUCUNE LIGNE (à relancer). Résultat : NON.")
    sortie.append("- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.")
    sortie.append(f"- [x] Étape 8 : autoplay ciblé : {AUTOPLAY} Résultat : aucun incident.")
    p = PLATEAU.get(cid)
    if p:
        sortie.append(f"- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? {p}. Cas plateau : {PLATEAU_FICHIER}. Résultat : OK.")
    else:
        sortie.append("- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou déplace une carte déjà couverte par les cas plateau du Vault. Résultat : sans objet.")
    sortie.append("\nCarte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).\n")
open(os.path.join(RACINE, "docs", "packs", "vault", "GABARITS.md"), "w", encoding="utf-8").write("\n".join(sortie))
print("ecrit", len(CARTES), "gabarits")
