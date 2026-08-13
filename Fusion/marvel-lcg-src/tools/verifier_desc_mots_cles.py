"""Le `desc` d'une carte dit-il ce que son TEXTE annonce ?

    python3.10 tools/verifier_desc_mots_cles.py <pack> [pack ...]

POURQUOI CET OUTIL EXISTE
-------------------------
Une carte qui dit « Uses (3 tactic counters) » n'entre en jeu avec ses compteurs
que si son `desc` porte `"Uses": "3,tactic"`. Le moteur ne lit PAS le texte : il
lit le desc (`RegisterAttribute`, has_uses.py). Sans ce champ, la carte se
construit, s'affiche, se joue — et son action reste GRISEE POUR TOUJOURS, parce
que le cout « retirer 1 compteur » ne peut jamais etre paye.

Rien ne signalait cela : ni `test_cards`, ni `test_generate_cards`, ni la sonde
de capacites, ni `verifier_noms_modules`. Seul un joueur devant la carte le voit.
C'est arrive a Merc Squad (dt008) et a 48 autres cartes de l'aspect Determination
le 13/08/2026.

CE QU'IL FAIT
-------------
Il relit chaque carte du pack et compare son texte a son desc, sur les mots-cles
que le moteur attend dans le desc : Uses, Toughness, Restricted, Retaliate,
MaxPerDeck, MaxPerUnit, Setup, Victory, Permanent, Alliance, Villainous,
Requirement. Les motifs sont ceux des cartes OFFICIELLES, apprises du jeu.
"""
import json
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# UN ATTRIBUT DE `desc` N'EXISTE QUE POUR CERTAINS TYPES DE CARTE, parce qu'il
# vient d'une classe du moteur dont tous les types n'heritent pas : `Uses` est
# sur Upgrade/Support/Attachment/Obligation/Environment, `Villainous` sur Minion.
# Le declarer ailleurs ne fait pas que rater sa cible : la carte NE SE GENERE
# PLUS (KeyError). Ces cas-la sont donc signales A PART : ils se traitent dans le
# module de la carte, jamais dans son desc.
TYPES_PAR_ATTRIBUT = {
    "Uses":        {"Upgrade", "Support", "Attachment", "Obligation", "Environment"},
    "Villainous":  {"Minion"},
    "Restricted":  {"Upgrade"},
    "MaxPerUnit":  {"Upgrade", "Support", "Attachment"},
    "MaxPerDeck":  {"Event", "Resource", "Upgrade", "Support", "Ally"},
    "Alliance":    {"Event"},
}

REGLES = [
    (r"Uses \((\d+) (\w+) counters?\)",     lambda m: ("Uses", "%s,%s" % (m.group(1), m.group(2)))),
    (r"(?m)^Toughness\.",                    lambda m: ("Toughness", None)),
    (r"(?m)^Restricted\.",                   lambda m: ("Restricted", None)),
    (r"Retaliate (\d)",                      lambda m: ("Retaliate", m.group(1))),
    (r"Max (\d+) per deck",                  lambda m: ("MaxPerDeck", m.group(1))),
    (r"Max (\d+)[A-Za-z ]* per player",      lambda m: ("MaxPerUnit", m.group(1))),
    (r"Max (\d+) per (?:ally|enemy|minion)", lambda m: ("MaxPerUnit", m.group(1))),
    (r"(?m)^Setup\.",                        lambda m: ("Setup", None)),
    (r"Victory (\d+)",                       lambda m: ("Victory", m.group(1))),
    (r"Permanent\.",                         lambda m: ("Permanent", None)),
    (r"(?m)^Alliance\.",                     lambda m: ("Alliance", None)),
    (r"(?m)^Villainous\.",                   lambda m: ("Villainous", None)),
    (r"Requirement \(\[(\w+)\]",             lambda m: ("Requirement", None)),
]


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    packs = sys.argv[1:]

    cartes = json.load(open(os.path.join(RACINE, "data", "cards.json"), encoding="utf-8"))
    ecarts = []
    sans_porte = []
    lues = 0
    for pack in packs:
        for carte in cartes.get(pack, []):
            lues += 1
            texte = (carte.get("text") or "").replace("<b>", "").replace("</b>", "")
            desc = carte.get("desc") or {}
            for motif, produit in REGLES:
                trouve = re.search(motif, texte)
                if not trouve:
                    continue
                cle, valeur = produit(trouve)
                types = TYPES_PAR_ATTRIBUT.get(cle)
                if types is not None and carte.get("type") not in types:
                    sans_porte.append(
                        "%s %-26s porte %s, que le moteur ne connait pas pour un %s"
                        % (carte["card_id"], carte.get("name", "")[:26], cle,
                           carte.get("type")))
                    continue
                if cle not in desc:
                    ecarts.append("%s %-26s le texte annonce %s, le desc ne le porte pas"
                                  % (carte["card_id"], carte.get("name", "")[:26], cle))
                elif valeur is not None and desc[cle] != valeur:
                    ecarts.append("%s %-26s %s vaut %r, le texte dit %r"
                                  % (carte["card_id"], carte.get("name", "")[:26],
                                     cle, desc[cle], valeur))

    if sans_porte:
        print("Sans porte dans le moteur (a assumer dans le module, pas dans le desc) :")
        print("\n".join("  " + x for x in sans_porte))
        print()
    if ecarts:
        print("\n".join(ecarts))
        print("\n%d ecart(s) sur %d carte(s) lue(s)." % (len(ecarts), lues))
        return 1
    print("OK : les %d cartes de %s ont un desc conforme a leur texte."
          % (lues, ", ".join(packs)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
